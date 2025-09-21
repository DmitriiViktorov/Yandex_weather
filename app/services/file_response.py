import io
import datetime
from urllib.parse import quote
from fastapi.responses import StreamingResponse
from openpyxl import Workbook


def excel_to_streaming_response(wb: Workbook, city: str) -> StreamingResponse:
    """
    Принимает объект Workbook и название города,
    возвращает StreamingResponse для отправки пользователю.
    """
    try:
        stream = io.BytesIO()
        wb.save(stream)
        stream.seek(0)

        filename = f"Прогноз_{city}_{datetime.date.today()}.xlsx"
        filename_encoded = quote(filename)

        headers = {
            "Content-Disposition": f"attachment; filename*=UTF-8''{filename_encoded}"
        }
    except Exception as e:
        raise ValueError(f"Не удалось сохранить Excel файл: {str(e)}")

    return StreamingResponse(
        stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers
    )