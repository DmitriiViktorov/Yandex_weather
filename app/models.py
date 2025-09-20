from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from .services.db import Base

class ReportLog(Base):
    __tablename__ = 'report_log'

    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    request_datetime = Column(DateTime, default=datetime.utcnow)
    status = Column(String, nullable=False)
    error_message = Column(String, nullable=True)