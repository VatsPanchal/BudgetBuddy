from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List, Dict
import json
from pydantic import BaseModel
import matplotlib.pyplot as plt
import io
import base64
import numpy as np
import colorsys
from datetime import datetime

from database.db_setup import get_db
from models.budget import Budget
from models.expense import Expense
from models.user import User

router = APIRouter()

class BudgetSetup(BaseModel):
    income: float
    savings_goal: float
    categories: Dict[str, float]

class ExpenseCreate(BaseModel):
    category: str
    amount: float
    description: str

class ExpenseResponse(BaseModel):
    id: int
    category: str
    amount_spent: float
    description: str
    created_at: datetime

@router.post("/setup")
async def setup_budget(
    budget_data: BudgetSetup,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    username = authorization.split(" ")[1]
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Validate total allocation
    total_allocated = sum(budget_data.categories.values())
    if total_allocated + budget_data.savings_goal > budget_data.income:
        raise HTTPException(status_code=400, detail="Total allocation exceeds income")

    # Create or update budget
    budget = db.query(Budget).filter(Budget.user_id == user.id).first()
    if budget:
        budget.income = budget_data.income
        budget.savings_goal = budget_data.savings_goal
        budget.categories = json.dumps(budget_data.categories)
    else:
        budget = Budget(
            user_id=user.id,
            income=budget_data.income,
            savings_goal=budget_data.savings_goal,
            categories=json.dumps(budget_data.categories)
        )
        db.add(budget)
    
    db.commit()
    return {"message": "Budget setup successful"}

@router.post("/expense")
async def add_expense(
    expense_data: ExpenseCreate,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    username = authorization.split(" ")[1]
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    budget = db.query(Budget).filter(Budget.user_id == user.id).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")

    categories = json.loads(budget.categories)
    if expense_data.category not in categories:
        raise HTTPException(status_code=400, detail="Invalid category")

    # Get current expenses for this category
    current_expenses = db.query(Expense).filter(
        Expense.user_id == user.id,
        Expense.category == expense_data.category
    ).all()
    
    # Calculate total spent in this category
    total_spent = sum(exp.amount_spent for exp in current_expenses)
    
    # Check if adding this expense would exceed the category budget
    category_budget = categories[expense_data.category]
    if total_spent + expense_data.amount > category_budget:
        remaining = category_budget - total_spent
        raise HTTPException(
            status_code=400,
            detail=f"Cannot add expense: would exceed {expense_data.category} budget. Remaining budget: ${remaining:.2f}"
        )

    # Create new expense
    expense = Expense(
        user_id=user.id,
        category=expense_data.category,
        amount_spent=expense_data.amount,
        description=expense_data.description
    )
    db.add(expense)
    db.commit()

    return {"message": "Expense added successfully"}

@router.get("/summary")
async def get_budget_summary(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    username = authorization.split(" ")[1]
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    budget = db.query(Budget).filter(Budget.user_id == user.id).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")

    # Get all expenses
    expenses = db.query(Expense).filter(Expense.user_id == user.id).all()
    
    # Calculate category totals
    category_totals = {}
    categories = json.loads(budget.categories)
    for category in categories:
        category_totals[category] = sum(
            exp.amount_spent for exp in expenses if exp.category == category
        )

    return {
        "income": budget.income,
        "savings_goal": budget.savings_goal,
        "categories": categories,
        "expenses": category_totals,
        "remaining": budget.income - sum(category_totals.values()) - budget.savings_goal
    }

@router.get("/chart")
async def get_budget_chart(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    try:
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid authorization header")
        
        username = authorization.split(" ")[1]
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        budget = db.query(Budget).filter(Budget.user_id == user.id).first()
        if not budget:
            raise HTTPException(status_code=404, detail="Budget not found")

        # Get expenses
        expenses = db.query(Expense).filter(Expense.user_id == user.id).all()
        
        # Calculate category totals
        categories = json.loads(budget.categories)
        category_data = []
        total_budget = sum(categories.values())
        
        if total_budget == 0:
            raise HTTPException(status_code=400, detail="No budget allocated")
        
        # First pass: collect all categories with budget
        for category in categories:
            if categories[category] > 0:  # Only include categories with budget
                assigned = categories[category]
                spent = sum(exp.amount_spent for exp in expenses if exp.category == category)
                spent_percentage = min(100, (spent / assigned) * 100)  # Cap at 100%
                
                category_data.append({
                    "category": category,
                    "assigned": assigned,
                    "spent": spent,
                    "spent_percentage": spent_percentage
                })

        if not category_data:
            raise HTTPException(status_code=400, detail="No budget categories found")

        # Create nested pie chart
        plt.figure(figsize=(12, 8))
        plt.style.use('default')  # Use default style
        
        # Set background color to white
        plt.rcParams['figure.facecolor'] = 'white'
        plt.rcParams['axes.facecolor'] = 'white'
        
        # Sort categories by assigned budget for consistent colors
        category_data.sort(key=lambda x: x["assigned"], reverse=True)
        
        # Create color palette with different shades
        base_colors = plt.cm.tab20(np.linspace(0, 1, len(category_data)))
        outer_colors = base_colors
        inner_colors = []
        
        for color in base_colors:
            # Create a lighter shade for the inner ring
            h, s, v = colorsys.rgb_to_hsv(color[0], color[1], color[2])
            lighter_color = colorsys.hsv_to_rgb(h, s * 0.8, min(1, v * 1.2))  # Decrease saturation, increase value
            inner_colors.append(lighter_color)
        
        # Outer ring - Budget allocation
        outer_values = [d["assigned"] for d in category_data]
        outer_labels = [f"{d['category']}\n${d['assigned']:.2f}" for d in category_data]
        
        # Inner ring - Spending progress
        inner_values = []
        inner_colors_expanded = []
        inner_labels = []
        
        for i, d in enumerate(category_data):
            # Add the spent portion
            spent_value = d["assigned"] * (d["spent_percentage"] / 100)
            inner_values.append(spent_value)
            inner_colors_expanded.append(inner_colors[i])
            inner_labels.append(f"{d['spent_percentage']:.1f}%")
            
            # Add the remaining portion
            remaining_value = d["assigned"] - spent_value
            if remaining_value > 0:
                inner_values.append(remaining_value)
                inner_colors_expanded.append((1, 1, 1, 1))  # White for remaining
                inner_labels.append("")
        
        # Plot outer ring with enhanced styling
        outer_pie = plt.pie(
            outer_values,
            labels=outer_labels,
            colors=outer_colors,
            startangle=90,
            wedgeprops={
                'width': 0.5,
                'edgecolor': 'black',
                'linewidth': 1.5,
                'antialiased': True
            },
            pctdistance=0.85,
            labeldistance=1.1,
            textprops={
                'fontsize': 9,
                'fontweight': 'bold'
            }
        )
        
        # Plot inner ring with enhanced styling
        inner_pie = plt.pie(
            inner_values,
            radius=0.5,
            colors=inner_colors_expanded,
            wedgeprops={
                'width': 0.5,
                'edgecolor': 'black',
                'linewidth': 1.5,
                'antialiased': True
            },
            startangle=90
        )
        
        # Add percentage labels to inner ring with enhanced styling
        label_index = 0
        for i, (wedge, label) in enumerate(zip(inner_pie[0], inner_labels)):
            if label and wedge.theta2 - wedge.theta1 > 0:
                ang = (wedge.theta2 - wedge.theta1)/2. + wedge.theta1
                y = np.sin(np.deg2rad(ang))
                x = np.cos(np.deg2rad(ang))
                horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
                connectionstyle = f"angle,angleA=0,angleB={ang}"
                plt.annotate(
                    label,
                    xy=(x, y),
                    xytext=(1.35*np.sign(x), 1.4*y),
                    horizontalalignment=horizontalalignment,
                    verticalalignment='center',
                    fontsize=9,
                    fontweight='bold',
                    arrowprops=dict(
                        arrowstyle="-",
                        connectionstyle=connectionstyle,
                        color='black',
                        linewidth=1
                    )
                )
                label_index += 1
        
        plt.axis('equal')
        plt.title('Budget Allocation and Spending Progress', 
                 pad=20, 
                 fontsize=14, 
                 fontweight='bold')
        
        # Add legend with enhanced styling
        legend_labels = [
            f"{d['category']}: ${d['spent']:.2f} / ${d['assigned']:.2f} ({d['spent_percentage']:.1f}%)"
            for d in category_data
        ]
        plt.legend(
            outer_pie[0],
            legend_labels,
            loc="center left",
            bbox_to_anchor=(1, 0.5),
            fontsize=9,
            frameon=True,
            framealpha=0.9,
            edgecolor='black'
        )
        
        # Add a subtle background grid
        plt.grid(True, alpha=0.3)
        
        # Save plot to bytes with higher quality
        buf = io.BytesIO()
        plt.savefig(buf, 
                   format='png', 
                   bbox_inches='tight', 
                   dpi=150,  # Increased DPI for better quality
                   facecolor='white',
                   edgecolor='black')
        plt.close()
        buf.seek(0)
        
        # Convert to base64
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        
        return {"image": image_base64}
    except Exception as e:
        print(f"Error generating chart: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating chart: {str(e)}")

@router.get("/expenses")
async def get_expenses(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    username = authorization.split(" ")[1]
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    expenses = db.query(Expense).filter(Expense.user_id == user.id).order_by(Expense.created_at.desc()).all()
    
    return [
        {
            "id": expense.id,
            "category": expense.category,
            "amount_spent": expense.amount_spent,
            "description": expense.description,
            "created_at": expense.created_at
        }
        for expense in expenses
    ]

@router.delete("/expense/{expense_id}")
async def delete_expense(
    expense_id: int,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    username = authorization.split(" ")[1]
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == user.id
    ).first()
    
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(expense)
    db.commit()
    
    return {"message": "Expense deleted successfully"}

@router.post("/update")
async def update_budget(
    budget_data: BudgetSetup,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    username = authorization.split(" ")[1]
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get current budget and expenses
    budget = db.query(Budget).filter(Budget.user_id == user.id).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")

    expenses = db.query(Expense).filter(Expense.user_id == user.id).all()
    current_categories = json.loads(budget.categories)
    
    # Calculate current spending per category
    current_spending = {}
    for expense in expenses:
        current_spending[expense.category] = current_spending.get(expense.category, 0) + expense.amount_spent

    # Validate that no category's budget is reduced below current spending
    for category, new_amount in budget_data.categories.items():
        if category in current_spending and new_amount < current_spending[category]:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot reduce {category} budget below current spending of ${current_spending[category]:.2f}"
            )

    # Validate total allocation
    total_allocated = sum(budget_data.categories.values())
    if total_allocated + budget_data.savings_goal > budget_data.income:
        raise HTTPException(status_code=400, detail="Total allocation exceeds income")

    # Update budget
    budget.income = budget_data.income
    budget.savings_goal = budget_data.savings_goal
    budget.categories = json.dumps(budget_data.categories)
    
    db.commit()
    return {"message": "Budget updated successfully"} 