from fastapi import APIRouter, Depends
from datetime import datetime
from starlette.responses import Response
from app.database.conn import db
from app.database.schema import Users
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/")
async def index(session: Session = Depends(db.session),):
    current_time = datetime.utcnow()
    return Response(f"Notification API (UTC: {current_time.strftime('%Y.%m.%d %H:%M:%S')})")

# @router.get("/")
# async def index():
#     """
#     ELB 상태 체크용 API
#     :return:
#     """
#     current_time = datetime.utcnow()
#     return Response(f"Notification API (UTC: {current_time.strftime('%Y.%m.%d %H:%M:%S')})")

