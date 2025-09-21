from enum import Enum
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum as SQLEnum
from datetime import datetime

from app.db.db import Base


class ReportStatus(str, Enum):
    success = "success"
    error = "error"


class ReportLog(Base):
    __tablename__ = 'report_log'

    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    request_datetime = Column(DateTime, default=datetime.today())
    status = Column(SQLEnum(ReportStatus), nullable=False)
    error_message = Column(String, nullable=True)