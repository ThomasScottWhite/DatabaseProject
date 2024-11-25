import datetime
import logging
import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import Connection, Row, select

from api import auth, models
from api.utils import export

from . import engine
from .tables import tables as tb


@export
def create_member(
    conn: Connection, auth_checker: auth.Auth, specification: models.CreateMemberRequest
) -> Row[Any]:
    info_dict = specification.model_dump(exclude_unset=True)

    if specification.is_chapter_admin is None:
        info_dict.pop("is_chapter_admin", None)
    else:
        auth_checker.is_chapter_admin(specification.chapter_id).raise_for_http()

    member_insert = tb.member.insert().returning(*tb.member.c).values(info_dict)
    return conn.execute(member_insert).one()


@export
def authenticate(
    email: str, password: str, expires_in: int = auth.DEFAULT_AUTH_LIFETIME
) -> auth.Auth | None:
    """Generates an authentication token for the provided `(email, password)` pair.

    If the `(email, password)` pair is missing from the database,
    `None` is returned instead.

    Args:
        email (str): The email of the user.
        password (str): The password of the user.
        expires_in (int, optional): The number of seconds after which
            the generated token with expire. Defaults to `DEFAULT_AUTH_LIFETIME`.

    Returns:
        The `Auth` if the `(email, password)` pair is valid, `None` otherwise.
    """

    with engine.get_connection() as conn:
        # validate credentials in the database and fetch relevant info
        user = tb.user.c  # alias for table columns
        result = conn.execute(
            select(
                user.is_admin,
                tb.member.c.chapter_id,
                tb.member.c.is_chapter_admin,
            )
            .select_from(tb.user)
            .join(tb.member, isouter=True)
            .where(user.email == email, user.password == password)
        ).one_or_none()

        # register login if successful
        if result is not None:
            token = str(uuid.uuid4())
            auth_obj = auth.Auth(
                token,
                email,
                result[0],
                result[1],
                result[2] or False,
                expires_in=expires_in,
            )
            auth_obj.register_self()

            return auth_obj
