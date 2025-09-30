from typing import Annotated
from sqlmodel import SQLModel, create_engine, Session
from fastapi import Depends, FastAPI

# Configuración para MySQL
mysql_user = "root"  
mysql_password = ""  
mysql_host = "127.0.0.1"  
mysql_port = "3306"  
mysql_db = "feel_your_emotions" 
mysql_url = f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}"

engine = create_engine(mysql_url)

def create_all_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

def get_session():
    with Session(engine) as session:
        yield session

session_dependency = Annotated[Session, Depends(get_session)]