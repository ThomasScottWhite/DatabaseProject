import logging

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from api import auth, db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/bills")


class MakeBillRequest(BaseModel):
    bill_name: str
    invoicee_id: str
    amount: float
    chapter_id: int

    class Config:
        orm_mode = True


@router.post("/create")
async def make_bill(info: MakeBillRequest, raw_request: Request):
    auth_token = raw_request.headers.get("Authorization")

    auth.get(auth_token).is_chapter_admin(info.chapter_id).raise_for_http()

    query = f"SELECT * FROM bills WHERE bill_name = '{info.bill_name}'"

    # make the bill

    return {"message": "Bill created successfully"}
