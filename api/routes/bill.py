from __future__ import annotations

import datetime
import logging
import uuid
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, Request, status
from pydantic import BaseModel
from sqlalchemy import Connection, select
from sqlalchemy.dialects.postgresql import UUID

from api import auth, db, models

logger = logging.getLogger(__name__)

router = APIRouter(prefix="bill", tags=["bill"])
# router = APIRouter(prefix="/bills")


class MakeBillRequest(BaseModel):
    invoicee_name: str
    invoicee_id: int
    bill_name: str
    amount: float
    date: datetime.date
    paid: float = 0


@router.post("/internal")
async def make_bill(
    info: MakeBillRequest, authorization: Annotated[str | None, Header()] = None
) -> dict[str, str]:
    """Creates an internal bill.

    Args:
        info (MakeBillRequest): The fields of the new bill.
        authorization (Annotated[str  |  None, Header, optional): The auth token used to authorize this action.
            Defaults to None.

    Raises:
        HTTPException: 401, 403; if the user does not have permission to perform this action.

    Returns:
        dict[str, str]: A confirmation message saying that the bill was created.
    """
    auth.get(authorization).is_chapter_admin(info.invoicee_id).raise_for_http()

    with db.get_connection() as conn:

        bill_UUID = uuid.uuid4()

        query = db.tb.bill.insert().values(
            chapter_id=info.invoicee_id,
            bill_id=bill_UUID,
            amount=info.amount,
            amount_paid=info.paid,
            desc=info.bill_name,
            due_date=info.date,
            issue_date=date.today(),
            is_external=0,
        )
        conn.execute(query)

        query = db.tb.internal_bill.insert().values(
            bill_id=bill_UUID, member_email=info.invoicee_name
        )
        conn.execute(query)

        conn.commit()

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

    invoicee_id: int
    date: str


@router.post("/external")
async def make_bill(
    request: MakeExternalBillRequest,
    authorization: Annotated[str | None, Header()] = None,
) -> dict[str, str]:
    """Creates a new external bill.

    Args:
        request (MakeExternalBillRequest): The fields of the new bill.
        authorization (Annotated[str  |  None, Header, optional): The auth token used to authorize this action.
            Defaults to None.

    Raises:
        HTTPException: 401, 403; if the user does not have permission to perform this action.

    Returns:
        dict[str, str]: A confirmation message saying that the bill was created.
    """
    auth.get(authorization).is_chapter_admin(request.invoicee_id).raise_for_http()

    with db.get_connection() as conn:

        bill_UUID = uuid.uuid4()

        query = db.tb.bill.insert().values(
            chapter_id=request.invoicee_id,
            bill_id=bill_UUID,
            amount=request.amount,
            amount_paid=0,
            desc=request.bill_name,
            due_date=request.date,
            issue_date=date.today(),
            is_external=0,
        )
        conn.execute(query)

        query = db.tb.external_bill.insert().values(
            bill_id=bill_UUID,
            chapter_contact=request.chapter_contact,
            payor_name=request.payer_name,
            p_billing_address=request.payer_bill_address,
            p_email=request.payer_email,
            p_phone_num=request.payer_phone,
        )
        conn.execute(query)

        conn.commit()

    return {"message": "Bill created successfully"}
