from sqlmodel import SQLModel, Session, create_engine
from config import get_settings

settings = get_settings()

# create_engine using the env var
database_url =f"postgresql://{settings.db_username}:{settings.db_password}@db:5432/{settings.db_name}"
engine = create_engine(database_url, echo=False)

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session