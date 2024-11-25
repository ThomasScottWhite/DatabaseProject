from __future__ import annotations

import logging
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import Connection, select

from api import auth, db, models
from fastapi import Request



from sqlalchemy.dialects.postgresql import UUID
import uuid



logger = logging.getLogger(__name__)

router = APIRouter(prefix="")
#router = APIRouter(prefix="/bills")



class MakeBillRequest(BaseModel):
    invoicee_name: str
    invoicee_id: str
    bill_name: str
    amount: str
    date: str
    paid: str


@router.post("/make-bill")
async def make_bill(info: MakeBillRequest, raw_request: Request):
    #auth_token = raw_request.headers.get("Authorization")

    #auth.get(auth_token).is_chapter_admin(info.chapter_id).raise_for_http()

    with db.get_connection() as conn:

        bill_UUID = uuid.uuid4()

        query = db.tb.bill.insert().values(chapter_id=info.invoicee_id, bill_id=bill_UUID, amount=info.amount, amount_paid=0, desc=info.bill_name, due_date=info.date, issue_date=date.today(), is_external=0)
        conn.execute(query)

        query = db.tb.internal_bill.insert().values(bill_id=bill_UUID, member_email=info.invoicee_name)
        conn.execute(query)

        conn.commit()

    # make the bill

    return {"message": "Bill created successfully"}

class MakeExternalBillRequest(BaseModel):
    bill_name: str
    chapter_contact: str
    payer_name: str
    payer_bill_address: str
    payer_email: str
    payer_phone: str
    due_date: str
    amount: float

    invoicee_id: str
    date: str


@router.post("/make-external-bill")
async def make_bill(request: MakeExternalBillRequest, raw_request: Request):
    auth_token = raw_request.headers.get("Authorization")
    if not auth_token:
        raise HTTPException(status_code=401, detail="Authorization token missing")

    with db.get_connection() as conn:

        bill_UUID = uuid.uuid4()

        query = db.tb.bill.insert().values(chapter_id=request.invoicee_id, bill_id=bill_UUID, amount=request.amount, amount_paid=0, desc=request.bill_name, due_date=request.date, issue_date=date.today(), is_external=0)
        conn.execute(query)

        query = db.tb.external_bill.insert().values(bill_id=bill_UUID, chapter_contact=request.chapter_contact, payor_name=request.payer_name, p_billing_address=request.payer_bill_address, p_email=request.payer_email, p_phone_num=request.payer_phone)
        conn.execute(query)

        conn.commit()

    return {"message": "Bill created successfully"}


"""
class ViewOutgoingBillRequest(BaseModel):
    bills: list[BillModel]
    organization_id: str


# Route for ViewOutgoingBillRequest
@router.get("/outgoing-bills")
async def view_outgoing_bills(request: Request):  # request: ViewOutgoingBillRequest
    auth_token = request.headers.get("Authorization")
    if not auth_token:
        raise HTTPException(status_code=401, detail="Authorization token missing")

    response = ViewOutgoingBillRequest(
        bills=[
            BillModel(
                invoicee_name="John Doe",
                invoicee_id="1",
                bill_id=1,
                bill_name="Rent",
                amount="1000",
                date="2021-10-10",
                paid=False,
            )
        ],
        organization_id="1",
    )
    return response
"""