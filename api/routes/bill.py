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


class CreateBillRequest(BaseModel):
    chapter_id: int
    amount: float
    desc: str = ""
    due_date: datetime.datetime


class CreateInternalBillRequest(CreateBillRequest):
    member_email: str


@router.post("/internal", status_code=status.HTTP_201_CREATED)
async def make_bill(
    specification: CreateInternalBillRequest,
    authorization: Annotated[str | None, Header()] = None,
) -> dict[str, str]:
    """Creates an internal bill.

    Args:
        specification (CreateInternalBillRequest): The fields of the new bill.
        authorization (Annotated[str  |  None, Header, optional): The auth token used to authorize this action.
            Defaults to None.

    Raises:
        HTTPException: 401, 403; if the user does not have permission to perform this action.

    Returns:
        dict[str, str]: A confirmation message saying that the bill was created.
    """
    auth.get(authorization).is_chapter_admin(specification.chapter_id).raise_for_http()

    with db.get_connection() as conn:

        bill_UUID = uuid.uuid4()

        query = db.tb.bill.insert().values(
            chapter_id=specification.chapter_id,
            bill_id=bill_UUID,
            amount=specification.amount,
            desc=specification.desc,
            due_date=specification.due_date,
            is_external=False,
        )
        conn.execute(query)

        query = db.tb.internal_bill.insert().values(
            bill_id=bill_UUID, member_email=specification.member_email
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


class CreateExternalBillRequest(CreateBillRequest):
    chapter_contact: str
    payor_name: str
    p_billing_address: str
    p_email: str
    p_phone_nume: str


@router.post("/external", status_code=status.HTTP_201_CREATED)
async def make_bill(
    specification: CreateExternalBillRequest,
    authorization: Annotated[str | None, Header()] = None,
) -> dict[str, str]:
    """Creates a new external bill.

    Args:
        specification (CreateExternalBillRequest): The fields of the new bill.
        authorization (Annotated[str  |  None, Header, optional): The auth token used to authorize this action.
            Defaults to None.

    Raises:
        HTTPException: 401, 403; if the user does not have permission to perform this action.

    Returns:
        dict[str, str]: A confirmation message saying that the bill was created.
    """
    auth.get(authorization).is_chapter_admin(specification.chapter_id).raise_for_http()

    with db.get_connection() as conn:

        bill_UUID = uuid.uuid4()

        query = db.tb.bill.insert().values(
            chapter_id=specification.chapter_id,
            bill_id=bill_UUID,
            amount=specification.amount,
            desc=specification.desc,
            due_date=specification.due_date,
            is_external=True,
        )
        conn.execute(query)

        query = db.tb.external_bill.insert().values(
            bill_id=bill_UUID,
            chapter_contact=specification.chapter_contact,
            payor_name=specification.payor_name,
            p_billing_address=specification.p_bill_address,
            p_email=specification.p_email,
            p_phone_num=specification.p_phone,
        )
        conn.execute(query)

        conn.commit()

    return {"message": "Bill created successfully"}
