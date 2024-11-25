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

router = APIRouter(prefix="/bill", tags=["bill"])


def _get_chapter_id_from_bill_id(conn: Connection, bill_id: str | uuid.UUID) -> int:
    query = select(db.tb.bill.c.chapter_id).where(db.tb.bill.c.bill_id == str(bill_id))
    result = conn.execute(query).one_or_none()

    if result is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Specified bill does not exist.")

    return result[0]


class MakeBillRequest(BaseModel):
    invoicee_name: str
    invoicee_id: int
    bill_name: str
    amount: float
    date: datetime.date


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
            amount_paid=0,
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


class UpdateBillRequest(BaseModel):
    amount: float = None
    amount_paid: float = None
    desc: str = None
    due_date: datetime.datetime = None
    issue_date: datetime.date = None


@router.patch("/internal/{bill_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_internal_bill(
    bill_id: uuid.UUID,
    updates: UpdateBillRequest,
    authorization: Annotated[str | None, Header()] = None,
):
    auth_checker = auth.get(authorization)
    auth_checker.logged_in().raise_for_http()

    with db.begin() as conn:
        chapter_id = _get_chapter_id_from_bill_id(conn, bill_id)
        auth_checker.is_chapter_admin(chapter_id).raise_for_http()

        query = (
            db.tb.bill.update()
            .values(**updates.model_dump(exclude_unset=True))
            .where(db.tb.bill.c.bill_id == str(bill_id))
        )
        conn.execute(query)


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
