from sqlalchemy import Column, Integer, String
from database.db.database import Base


class Club(Base):
    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True, index=True)
    clubName = Column(String, nullable=False)
    clubNameShort = Column(String)
