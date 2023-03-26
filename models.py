from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = "states"
    user_id = Column("user_id", Integer, primary_key=True)
    text = Column("text", String)
    language_src = Column("language_src", String)
    language_dest = Column("language_dest", String)

    def __init__(self, user_id, text=None, language_src=None, language_dest=None):
        self.user_id = user_id
        self.text = text
        self.language_dest = language_dest
        self.language_src = language_src


engine = create_engine("sqlite:///users.db", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
