from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from constants import DATABASE_URL

# Create the engine
engine = create_engine(DATABASE_URL, echo=False)

# Create a base class
Base = declarative_base()

# Create a session factory
SessionLocal = sessionmaker(bind=engine)


# Function to get a session
def get_session():
    return SessionLocal()
