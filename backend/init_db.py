from database.db_setup import Base, engine

# Create all tables
Base.metadata.create_all(bind=engine)

print("✅ Database initialized successfully!")