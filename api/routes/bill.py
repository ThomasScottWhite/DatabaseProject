from __future__ import annotations

import datetime
import logging
import uuid
from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel, field_validator
from sqlalchemy import Connection, select

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


class UpdateBillRequest(BaseModel):
    amount: float = None
    amount_paid: float = None
    desc: str = None
    due_date: datetime.datetime = None
    issue_date: datetime.date = None


@router.patch("/id/{bill_id}")
def update_bill(
    bill_id: uuid.UUID,
    updates: UpdateBillRequest,
    authorization: Annotated[str | None, Header()] = None,
) -> models.Bill:
    auth_checker = auth.get(authorization)
    auth_checker.logged_in().raise_for_http()

    with db.begin() as conn:
        chapter_id = _get_chapter_id_from_bill_id(conn, bill_id)
        auth_checker.is_chapter_admin(chapter_id).raise_for_http()

        query = (
            db.tb.bill.update()
            .returning(*db.tb.bill.c)
            .values(**updates.model_dump(exclude_unset=True))
            .where(db.tb.bill.c.bill_id == str(bill_id))
        )
        result = conn.execute(query).one_or_none()

        if result is None:
            raise HTTPException(status.HTTP_304_NOT_MODIFIED)

    return result


@router.delete("/id/{bill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bill(
    bill_id: uuid.UUID,
    authorization: Annotated[str | None, Header()] = None,
):
    auth_checker = auth.get(authorization)
    auth_checker.logged_in().raise_for_http()

    with db.begin() as conn:
        chapter_id = _get_chapter_id_from_bill_id(conn, bill_id)
        auth_checker.is_chapter_admin(chapter_id).raise_for_http()

        query = db.tb.bill.delete().where(db.tb.bill.c.bill_id == str(bill_id))
        conn.execute(query)


class PaymentRequest(BaseModel):
    payment_amount: int

    @field_validator("payment_amount")
    @classmethod
    def name_must_contain_space(cls, v: int) -> int:
        if v < 0:
            raise ValueError("cannot pay negative amount.")
        return v


@router.post("/pay/{bill_id}")
def pay_bill(
    bill_id: uuid.UUID,
    payment: PaymentRequest,
    authorization: Annotated[str | None, Header()] = None,
) -> models.InternalBill:
    auth_checker = auth.get(authorization)
    auth_checker.logged_in().raise_for_http()

    with db.begin() as conn:
        email_query = select(db.tb.internal_bill.c.member_email).where(
            db.tb.internal_bill.c.bill_id == str(bill_id)
        )
        email_result = conn.execute(email_query).one_or_none()

        if email_query is None:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                "Specified bill does not exist or is not an internal bill.",
            )

        auth_checker.is_user(email_result[0]).raise_for_http()

        update_query = (
            db.tb.bill.update()
            .returning(*db.tb.bill.c)
            .values(amount_paid=db.tb.bill.c.amount_paid + payment.payment_amount)
            .where(db.tb.bill.c.bill_id == str(bill_id))
        )
        result = conn.execute(update_query).one_or_none()

        if result is None:
            raise HTTPException(status.HTTP_304_NOT_MODIFIED)

    return dict(**result._mapping, member_email=email_result[0])


@router.post("/internal", status_code=status.HTTP_201_CREATED)
async def make_internal_bill(
    specification: CreateInternalBillRequest,
    authorization: Annotated[str | None, Header()] = None,
) -> models.InternalBill:
    """Creates an internal bill.

    Args:
        specification (CreateInternalBillRequest): The fields of the new bill.
        authorization (Annotated[str  |  None, Header, optional): The auth token used to authorize this action.
            Defaults to None.

    Raises:
        HTTPException: 401, 403; if the user does not have permission to perform this action.

    Returns:
        models.InternalBill: The created bill.
    """
    auth.get(authorization).is_chapter_admin(specification.chapter_id).raise_for_http()

    with db.get_connection() as conn:

        bill_UUID = uuid.uuid4()

        query = (
            db.tb.bill.insert()
            .returning(*db.tb.bill.c)
            .values(
                chapter_id=specification.chapter_id,
                bill_id=bill_UUID,
                amount=specification.amount,
                desc=specification.desc,
                due_date=specification.due_date,
                is_external=False,
            )
        )
        result = conn.execute(query).one()

        query = db.tb.internal_bill.insert().values(
            bill_id=bill_UUID, member_email=specification.member_email
        )
        conn.execute(query)

        conn.commit()

    return dict(**result._mapping, member_email=specification.member_email)


class CreateExternalBillRequest(CreateBillRequest):
    chapter_contact: str
    payor_name: str
    p_billing_address: str
    p_email: str
    p_phone_num: str


@router.post("/external", status_code=status.HTTP_201_CREATED)
async def make_external_bill(
    specification: CreateExternalBillRequest,
    authorization: Annotated[str | None, Header()] = None,
) -> models.ExternalBill:
    """Creates a new external bill.

    Args:
        specification (CreateExternalBillRequest): The fields of the new bill.
        authorization (Annotated[str  |  None, Header, optional): The auth token used to authorize this action.
            Defaults to None.

    Raises:
        HTTPException: 401, 403; if the user does not have permission to perform this action.

    Returns:
        models.ExternalBill: The created bill.
    """
    auth.get(authorization).is_chapter_admin(specification.chapter_id).raise_for_http()

    with db.get_connection() as conn:

        bill_UUID = uuid.uuid4()

        query = (
            db.tb.bill.insert()
            .returning(*db.tb.bill.c)
            .values(
                chapter_id=specification.chapter_id,
                bill_id=bill_UUID,
                amount=specification.amount,
                desc=specification.desc,
                due_date=specification.due_date,
                is_external=True,
            )
        )
        bill_result = conn.execute(query).one()

        query = (
            db.tb.external_bill.insert()
            .returning(*[c for c in db.tb.external_bill.c if c.name != "bill_id"])
            .values(
                bill_id=bill_UUID,
                chapter_contact=specification.chapter_contact,
                payor_name=specification.payor_name,
                p_billing_address=specification.p_billing_address,
                p_email=specification.p_email,
                p_phone_num=specification.p_phone_num,
            )
        )
        external_result = conn.execute(query).one()

        conn.commit()

    return dict(**bill_result._mapping, **external_result._mapping)
