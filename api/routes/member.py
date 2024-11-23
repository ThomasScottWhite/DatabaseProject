from __future__ import annotations

import logging
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import Connection, select

from api import auth, db, models

router = APIRouter(prefix="/member", tags=["member"])

logger = logging.getLogger(__name__)

_MEMBER_NOT_EXISTS = HTTPException(
    status.HTTP_404_NOT_FOUND, "Specified member does not exist."
)


def _get_chapter_id_from_member_email(conn: Connection, member_email: str) -> int:
    """Returns the chapter ID corresponding to the provided email, if applicable; else
    raises an HTTP 404 exception.

    Args:
        conn (Connection): The database connection with which to query the database.
        member_email (str): The email to for which to aquire the corresponding chapter ID.

    Raises:
        HTTPException: 404; if there is no Member with email `member_email`.
    """
    result = conn.execute(
        select(db.tb.member.c.chapter_id).where(db.tb.member.c.email == member_email)
    ).one_or_none()

    if result is None:
        raise _MEMBER_NOT_EXISTS

    return result[0]


@router.get("")
def get_all_members(
    authorization: Annotated[str | None, Header()] = None
) -> list[models.Member]:
    """Returns a list of all members in the database.

    Args:
        authorization (Annotated[str  |  None, Header, optional): The auth token used to authorize this action.
            Defaults to None.

    Raises:
        HTTPException: 401, 403; if the user does not have permission to perform this action.
    """
    auth.get(authorization).is_global_admin().raise_for_http()

    with db.get_connection() as conn:

        query = db.tb.member.select()
        result = conn.execute(query).all()

    return result


@router.post("")
def create_member(
    specification: models.CreateMemberRequest,
    authorization: Annotated[str | None, Header()] = None,
) -> models.Member:
    """Creates a new member.

    Note: specification.email must correspond to an existing user that is not already already a
    member of a chapter.

    Args:
        specification (models.CreateMemberRequest): The specification of the member to create.
        authorization (Annotated[str  |  None, Header, optional): The auth token used to authorize this action.
            Defaults to None.

    Raises:
        HTTPException: 401, 403; if the user does not have permission to perform this action.

    Returns:
        models.Member: The newly created member as it appears in the database.
    """
    auth_checker = auth.get(authorization)
    (
        auth_checker.is_user(specification.email)
        or auth_checker.is_chapter_admin(specification.chapter_id)
    ).raise_for_http()

    with db.begin() as conn:
        result = db.create_member(conn, auth_checker, specification)

    return result


@router.get("/{member_email}")
def get_specific_member(
    member_email: str, authorization: Annotated[str | None, Header()] = None
) -> models.MemberWithSiteAdmin:
    """Returns the details for a specific member.

    Args:
        member_email (str): _description_
        authorization (Annotated[str  |  None, Header, optional): The auth token used to authorize this action.
            Defaults to None.

    Raises:
        HTTPException: 404; if the specified member does not exist.
        HTTPException: 401, 403; if the user does not have permission to perform this action.
    """

    auth_checker = auth.get(authorization)

    # check if user is logged in to prevent DB querying early
    auth_checker.logged_in().raise_for_http()

    with db.get_connection() as conn:

        query = (
            select(*db.tb.member.c, db.tb.user.c.is_admin.label("is_site_admin"))
            .select_from(db.tb.member)
            .join(db.tb.user)
            .where(db.tb.member.c.email == member_email)
        )

        result = conn.execute(query).one_or_none()

    if result is None:
        raise _MEMBER_NOT_EXISTS

    auth_checker.has_chapter_access(result._mapping["chapter_id"]).raise_for_http()

    return result


@router.delete("/{member_email}", status_code=status.HTTP_204_NO_CONTENT)
def delete_member(
    member_email: str,
    authorization: Annotated[str | None, Header()] = None,
):
    """Deletes an member; that is, removes a user from as a member of a chapter.

    Args:
        member_email (str): The email of the member to remove.
        authorization (Annotated[str  |  None, Header, optional): The auth token used to authorize this action.
            Defaults to None.

    Raises:
        HTTPException: 401, 403; if the user does not have permission to perform this action.
    """

    auth_checker = auth.get(authorization)

    if not auth_checker.is_user(member_email):
        auth_checker.logged_in().raise_for_http()

        with db.get_connection() as conn:
            chapter_id = _get_chapter_id_from_member_email(conn, member_email)

        auth_checker.is_chapter_admin(chapter_id).raise_for_http()

    with db.begin() as conn:
        query = db.tb.member.delete().where(db.tb.member.c.email == member_email)
        conn.execute(query)


# TODO: allow None in type hint where applicable
class MemberUpdateRequest(BaseModel):
    chapter_id: int = None
    email: str = None
    fname: str = None
    lname: str = None
    dob: date = None
    member_id: int = None
    member_status: str = None
    is_chapter_admin: bool = None
    phone_num: str = None


@router.patch("/{member_email}")
def update_member(
    member_email: str,
    updates: MemberUpdateRequest,
    authorization: Annotated[str | None, Header()] = None,
) -> models.Member:
    """Partially updates a member according to the values provided in `updates`.

    Note: depending on what is modified, different permissions are needed. For
    instance, you must be a global admin to modify email, chapter admin of the
    member's chapter to modified is_chapter_admin, and the user (or chapter admin)
    to modify all other fields.

    Args:
        member_email (str): The email of the member to change.
        updates (MemberUpdateRequest): The values to modify.
        authorization (Annotated[str  |  None, Header, optional): The auth token used to authorize this action.
            Defaults to None.

    Raises:
        HTTPException: 304; if the request goes through but nothing is modified.
        HTTPException: 404; if the specified member does not exist.
        HTTPException: 401, 403; if the user does not have permission to perform this action.

    Returns:
        models.Member: The member specified by `member_email` with the changes applied.
    """

    auth_checker = auth.get(authorization)
    auth_checker.logged_in().raise_for_http()

    with db.get_connection() as conn:
        member_chapter_id = _get_chapter_id_from_member_email(conn, member_email)

    # exclude_unset is important; we only want data manually set
    update_dict = updates.model_dump(exclude_unset=True)

    if "email" in update_dict:
        # these require global admin because it wouldn't make sense
        auth_checker.is_global_admin().raise_for_http()
    elif "is_chapter_admin" in update_dict:
        # only chapter admins can change this value
        # note that we don't need to do the user check since if the code runs
        #   past this point, we know they are a chapter admin
        auth_checker.is_chapter_admin(member_chapter_id).raise_for_http()
    else:
        (
            auth_checker.is_user(member_email)
            or auth_checker.is_chapter_admin(member_chapter_id)
        ).raise_for_http()

    with db.get_connection() as conn:

        update_query = (
            db.tb.member.update()
            .values(update_dict)
            .where(db.tb.member.c.email == member_email)
            .returning(*db.tb.member.c)
        )

        result = conn.execute(update_query).one_or_none()
        conn.commit()

    if result is None:
        raise HTTPException(status.HTTP_304_NOT_MODIFIED, "Nothing was changed.")

    return result
