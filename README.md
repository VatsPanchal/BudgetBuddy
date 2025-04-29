# Budget Buddy

A full-stack web application for managing personal budgets and expenses. Built with Vue.js for the frontend and FastAPI for the backend.

## Features

- User authentication (register, login, password reset)
- Budget setup and management
- Expense tracking by categories
- Visual budget summaries
- Dark mode support
- Responsive design

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn

## Project Structure

```
budget-buddy/
├── backend/              # FastAPI backend
│   ├── database/        # Database setup and models
│   ├── routes/          # API endpoints
│   ├── models/          # SQLAlchemy models
│   └── alembic/         # Database migrations
└── frontend/            # Vue.js frontend
    ├── src/
    │   ├── components/  # Vue components
    │   ├── assets/      # Static assets
    │   └── App.vue      # Main application component
    └── package.json     # Frontend dependencies
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:

   ```bash
   cd budget-buddy/backend
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   - Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Run database migrations:

   ```bash
   alembic upgrade head
   ```

6. Start the backend server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

### Frontend Setup

1. Navigate to the frontend directory:

   ```bash
   cd budget-buddy/frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run serve
   ```

## Running the Application

1. Start the backend server (from the backend directory):

   ```bash
   uvicorn main:app --reload --port 8000
   ```

2. Start the frontend server (from the frontend directory):

   ```bash
   npm run serve
   ```

3. Open your browser and navigate to:
   ```
   http://localhost:8080
   ```

## API Documentation

Once the backend server is running, you can access the API documentation at:

```
http://localhost:8000/docs
```

## Available Scripts

### Frontend

- `npm run serve` - Start development server
- `npm run build` - Build for production
- `npm run lint` - Lint and fix files

### Backend

- `alembic upgrade head` - Run database migrations
- `alembic revision --autogenerate -m "description"` - Create new migration

## Environment Variables

The backend uses the following environment variables:

- `SECRET_KEY` - JWT secret key (default: "your-secret-key-here")

## Database

The application uses SQLite for development. The database file is created automatically at `budget_buddy.db` in the backend directory.

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Submit a pull request

## License

This project is licensed under the MIT License.

## Quick Start (One-Click Setup)

For users who want to run the project quickly without manual setup, we provide automated scripts:

### Windows

1. Double-click `run_project.bat`
2. The script will:
   - Check for required software (Python and Node.js)
   - Set up the Python virtual environment
   - Install all dependencies
   - Start both the backend and frontend servers
   - Open the application in your default browser

### macOS/Linux

1. Open a terminal in the project directory
2. Make the script executable:
   ```bash
   chmod +x run_project.sh
   ```
3. Run the script:
   ```bash
   ./run_project.sh
   ```
4. The script will:
   - Check for required software
   - Set up the environment
   - Install dependencies
   - Start the servers
   - Provide the application URL

Note: The first run might take a few minutes as it installs all dependencies.
