# this file is used to set up the database connection and hands out sessions to whoever asks.

from sqlmodel import Session, create_engine
from app.config import settings

# the engine is the actual pool of connections to the postgreSQL
engine = create_engine(settings.DATABASE_URL, echo=False)


# a session is one conversation with the database that endpoints get once per request
def get_session():
    with Session(engine) as session:
        yield session