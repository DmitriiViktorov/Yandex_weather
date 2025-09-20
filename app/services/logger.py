from datetime import datetime

from .db import SessionLocal
from app.models import ReportLog
from contextlib import contextmanager


@contextmanager
def get_db_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def log_report_to_db(
        city: str,
        lat: float,
        lon: float,
        status: str,
        error_message: str = None,
):
    with get_db_session() as session:
        log = ReportLog(
            city=city,
            lat=lat,
            lon=lon,
            request_datetime=datetime.now(),
            status=status,
            error_message=error_message,
        )
        session.add(log)

