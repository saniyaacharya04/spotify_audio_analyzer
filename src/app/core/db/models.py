from sqlalchemy import Column, Integer, String, Date
from src.app.core.db.session import Base

class ApiUsage(Base):
    __tablename__ = "api_usage"

    id = Column(Integer, primary_key=True)
    api_key = Column(String, index=True)
    date = Column(Date, index=True)
    count = Column(Integer, default=0)
