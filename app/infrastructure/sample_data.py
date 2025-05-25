from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.infrastructure.database.models import BlogModel, CommentModel, TagModel


def load_sample_data(db: Session):
    """
    Load sample data into the database
    """
    # Create tags
    tags = {
        "python": TagModel(name="Python"),
        "fastapi": TagModel(name="FastAPI"),
        "sqlalchemy": TagModel(name="SQLAlchemy"),
        "web": TagModel(name="Web Development"),
        "api": TagModel(name="API"),
        "clean-architecture": TagModel(name="Clean Architecture")
    }
    
    for tag in tags.values():
        db.add(tag)
    
    # Create blogs
    blogs = [
        BlogModel(
            title="Getting Started with FastAPI",
            author="John Doe",
            date=datetime.now() - timedelta(days=7),
            content="""
            # Getting Started with FastAPI

            FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.

            ## Key Features

            - Fast: Very high performance, on par with NodeJS and Go.
            - Easy: Designed to be easy to use and learn. Less time reading docs.
            - Short: Minimize code duplication. Multiple features from each parameter declaration.
            - Robust: Get production-ready code. With automatic interactive documentation.
            - Standards-based: Based on (and fully compatible with) the open standards for APIs: OpenAPI and JSON Schema.
            
            ## Installation
            
            ```bash
            pip install fastapi
            pip install uvicorn
            ```
            
            ## A Simple Example
            
            ```python
            from fastapi import FastAPI
            
            app = FastAPI()
            
            @app.get("/")
            def read_root():
                return {"Hello": "World"}
            
            @app.get("/items/{item_id}")
            def read_item(item_id: int, q: str = None):
                return {"item_id": item_id, "q": q}
            ```
            
            Run the server with: `uvicorn main:app --reload`
            """,
            excerpt="FastAPI is a modern, fast web framework for building APIs with Python 3.7+ based on standard Python type hints.",
            category="Web Development",
            tags=[tags["fastapi"], tags["python"], tags["api"], tags["web"]]
        ),
        BlogModel(
            title="Clean Architecture in Python",
            author="Jane Smith",
            date=datetime.now() - timedelta(days=3),
            content="""
            # Clean Architecture in Python
            
            Clean Architecture is a software design philosophy that separates the concerns of a software system into different layers, making it more maintainable and testable.
            
            ## Principles of Clean Architecture
            
            1. **Independence of frameworks**: The architecture doesn't depend on the existence of some library or framework.
            2. **Testability**: The business rules can be tested without the UI, database, web server, or any external element.
            3. **Independence of UI**: The UI can change easily, without changing the rest of the system.
            4. **Independence of database**: You can swap out Oracle or SQL Server for MongoDB, BigTable, or something else.
            5. **Independence of any external agency**: Your business rules don't know anything about the outside world.
            
            ## Implementing Clean Architecture in Python
            
            In Python, Clean Architecture can be implemented using a layered approach:
            
            1. **Domain Layer**: Contains the business logic and rules.
            2. **Use Case Layer**: Contains application-specific business rules.
            3. **Interface Adapter Layer**: Contains adapters that convert data between the use cases and external agencies.
            4. **Framework & Driver Layer**: Contains frameworks and tools like the database, the web framework, etc.
            
            ## Example
            
            ```python
            # Domain Layer
            class User:
                def __init__(self, user_id, name, email):
                    self.user_id = user_id
                    self.name = name
                    self.email = email
            
            # Use Case Layer
            class UserRepository:
                def get_user(self, user_id):
                    pass
                    
                def save_user(self, user):
                    pass
            
            class UserInteractor:
                def __init__(self, user_repository):
                    self.user_repository = user_repository
                    
                def get_user(self, user_id):
                    return self.user_repository.get_user(user_id)
                    
                def save_user(self, user):
                    self.user_repository.save_user(user)
            
            # Interface Adapter Layer
            class SqlAlchemyUserRepository(UserRepository):
                def get_user(self, user_id):
                    # Implementation using SQLAlchemy
                    pass
                    
                def save_user(self, user):
                    # Implementation using SQLAlchemy
                    pass
            
            # Framework & Driver Layer
            from fastapi import FastAPI, Depends
            
            app = FastAPI()
            
            def get_user_interactor():
                return UserInteractor(SqlAlchemyUserRepository())
            
            @app.get("/users/{user_id}")
            def read_user(user_id: int, interactor = Depends(get_user_interactor)):
                user = interactor.get_user(user_id)
                return user
            ```
            """,
            excerpt="Clean Architecture is a software design philosophy that separates the concerns of a software system into different layers.",
            category="Software Architecture",
            tags=[tags["python"], tags["clean-architecture"]]
        ),
        BlogModel(
            title="Working with SQLAlchemy and FastAPI",
            author="Bob Johnson",
            date=datetime.now() - timedelta(days=1),
            content="""
            # Working with SQLAlchemy and FastAPI
            
            SQLAlchemy is a powerful SQL toolkit and Object-Relational Mapping (ORM) library for Python. When combined with FastAPI, it provides a robust solution for building database-driven APIs.
            
            ## Setting Up SQLAlchemy with FastAPI
            
            First, install the necessary packages:
            
            ```bash
            pip install fastapi sqlalchemy
            ```
            
            ### Database Configuration
            
            Create a file for database configuration:
            
            ```python
            # db.py
            from sqlalchemy import create_engine
            from sqlalchemy.ext.declarative import declarative_base
            from sqlalchemy.orm import sessionmaker
            
            SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
            
            engine = create_engine(
                SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
            )
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            
            Base = declarative_base()
            ```
            
            ### Define Models
            
            Create your SQLAlchemy models:
            
            ```python
            # models.py
            from sqlalchemy import Column, Integer, String
            from .db import Base
            
            class User(Base):
                __tablename__ = "users"
                
                id = Column(Integer, primary_key=True, index=True)
                name = Column(String, index=True)
                email = Column(String, unique=True, index=True)
            ```
            
            ### Create Database Tables
            
            Create the database tables:
            
            ```python
            from .db import engine
            from . import models
            
            models.Base.metadata.create_all(bind=engine)
            ```
            
            ### Dependency for Database Session
            
            Create a dependency for the database session:
            
            ```python
            # dependencies.py
            from .db import SessionLocal
            
            def get_db():
                db = SessionLocal()
                try:
                    yield db
                finally:
                    db.close()
            ```
            
            ### Create FastAPI Endpoints
            
            Use the database session in your FastAPI endpoints:
            
            ```python
            # main.py
            from fastapi import FastAPI, Depends
            from sqlalchemy.orm import Session
            from . import models
            from .dependencies import get_db
            
            app = FastAPI()
            
            @app.get("/users/")
            def read_users(db: Session = Depends(get_db)):
                users = db.query(models.User).all()
                return users
            
            @app.post("/users/")
            def create_user(name: str, email: str, db: Session = Depends(get_db)):
                user = models.User(name=name, email=email)
                db.add(user)
                db.commit()
                db.refresh(user)
                return user
            ```
            
            ## Conclusion
            
            Using SQLAlchemy with FastAPI allows you to build powerful, database-driven APIs with clean code and strong typing.
            """,
            excerpt="Learn how to integrate SQLAlchemy with FastAPI for robust database-driven APIs.",
            category="Database",
            tags=[tags["sqlalchemy"], tags["fastapi"], tags["python"], tags["api"]]
        )
    ]
    
    for blog in blogs:
        db.add(blog)
    
    # Create comments
    comments = [
        CommentModel(
            post_id=1,
            name="Alice",
            message="Great introduction to FastAPI! I've been using it for a few months and it's really improved my workflow.",
            created_at=datetime.now() - timedelta(days=6, hours=3)
        ),
        CommentModel(
            post_id=1,
            name="Charlie",
            message="How does FastAPI compare to Flask? I've been using Flask for a while but I'm considering switching.",
            created_at=datetime.now() - timedelta(days=6, hours=1)
        ),
        CommentModel(
            post_id=1,
            name="John Doe",
            message="@Charlie FastAPI is generally faster and has better type checking with Pydantic. It's a great choice if you're building APIs.",
            created_at=datetime.now() - timedelta(days=5, hours=23)
        ),
        CommentModel(
            post_id=2,
            name="David",
            message="Nice explanation of Clean Architecture. I'm trying to implement it in my current project.",
            created_at=datetime.now() - timedelta(days=2, hours=12)
        ),
        CommentModel(
            post_id=3,
            name="Eve",
            message="Thanks for the tutorial. I was struggling with integrating SQLAlchemy and FastAPI.",
            created_at=datetime.now() - timedelta(hours=12)
        ),
        CommentModel(
            post_id=3,
            name="Frank",
            message="Do you have any tips for optimizing SQLAlchemy queries with FastAPI?",
            created_at=datetime.now() - timedelta(hours=8)
        )
    ]
    
    for comment in comments:
        db.add(comment)
    
    # Commit all changes
    db.commit()
