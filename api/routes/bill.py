import logging

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from api import auth, db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/bills")


class MakeBillRequest(BaseModel):
    invoicee_name: str
    invoicee_id: str
    bill_name: str
    amount: str
    date: str
    paid: str

    class Config:
        orm_mode = True


#@router.post("/create")
#async def make_bill(info: MakeBillRequest, raw_request: Request):
#    auth_token = raw_request.headers.get("Authorization")
#
#    auth.get(auth_token).is_chapter_admin(info.chapter_id).raise_for_http()
#
#    with db.get_connection() as conn:
#
#        query = db.tb.bill.insert().values(chapter_id=info.invoicee_id, amount=info.amount, amount_paid=0, desc=info.bill_name, due_date=info.date, issue_date="2024-01-01", is_external=0)
#
#        (tempBillID,) = conn.execute(query).one()
#
        #if (info.is_external == FALSE):
        #   query = db.tb.internal_bill.insert().values(bill_id=tempBillID[0], member_email=info.invoicee_id)
        #
        #else:
        #   query = db.tb.external_bill.insert().values(bill_id=tempBillID[0], chapter_contact=FIXME, payor_name=FIXME, p_billing_address=FIXME, p_mail=FIXME, p_phone_num=FIXME)
        #
        #conn.execute(query).one()

    # make the bill

#    return {"message": "Bill created successfully"}
