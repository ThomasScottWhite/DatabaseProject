from __future__ import annotations

import logging
from typing import Annotated, Any, Sequence

from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import Connection, Insert, Row, select

from api import auth, db, models

router = APIRouter(prefix="/payment_info", tags=["payment_info"])

logger = logging.getLogger(__name__)


class CreatePaymentInfoRequest(BaseModel):
    member_email: str
    nickname: str


class CreateBankAccountRequest(CreatePaymentInfoRequest):
    account_num: int
    routing_num: int


class CreateCardRequest(CreatePaymentInfoRequest):
    card_num: int
    security_code: int
    exp_date: str
    name: str


@router.post("")
def create_payment_info(
    specification: CreateBankAccountRequest | CreateCardRequest,
    authorization: Annotated[str | None, Header()] = None,
) -> models.BankAccount | models.Card:
    auth.get(authorization).is_user(specification.member_email).raise_for_http()

    with db.get_connection() as conn:

        spec_dict = specification.model_dump(exclude_unset=True)

        info_query = (
            db.tb.payment_info.insert()
            .returning(db.tb.payment_info.c.payment_id)
            .values(
                member_email=spec_dict.pop("member_email"),
                nickname=spec_dict.pop("nickname", None),
            )
        )

        (created_id,) = conn.execute(info_query).one()

        spec_dict["payment_id"] = created_id

        query: Insert
        if isinstance(specification, CreateBankAccountRequest):
            query = (
                db.tb.bank_account.insert()
                .returning(*db.tb.bank_account.c)
                .values(spec_dict)
            )
        else:
            query = db.tb.card.insert().returning(*db.tb.card.c).values(spec_dict)

        created = conn.execute(query).one()
        conn.commit()

    return dict(
        member_email=specification.member_email,
        nickname=specification.nickname,
        **created._mapping,
    )


# TODO: update, delete
