from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ReportLog, ReportStatus


async def log_report_to_db(
        session: AsyncSession,
        city: str,
        lat: float,
        lon: float,
        status: ReportStatus,
        error_message: str = None,
):
    log = ReportLog(
        city=city,
        lat=lat,
        lon=lon,
        request_datetime=datetime.utcnow(),
        status=status,
        error_message=error_message,
    )
    session.add(log)
    await session.commit()

