from __future__ import annotations

import logging
from datetime import date
from typing import Annotated, Any, Sequence

from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import Connection, Row, select

from api import auth, db, models

router = APIRouter(prefix="/chapter", tags=["chapter"])

logger = logging.getLogger(__name__)


_CHAPTER_NOT_EXISTS = HTTPException(
    status.HTTP_404_NOT_FOUND, "Specified chapter does not exist."
)


def _get_chapter_members(conn: Connection, chapter_id: int) -> Sequence[Row[Any]]:
    """Returns the members of the specified chapter.

    Args:
        conn (Connection): The database connection with which to perform the query.
        chapter_id (int): The ID of the chapter from which to pull members.
    """

    return conn.execute(
        db.tb.member.select().where(db.tb.member.c.chapter_id == chapter_id)
    ).all()


@router.get("")
def get_all_chapters(
    authorization: Annotated[str | None, Header()] = None
) -> list[models.Chapter]:
    """Returns a list of all chapters. Use `/organization/{org_name}?include_chapters=true` to get all chapters for
    an organization.

    Args:
        authorization (Annotated[str  |  None, Header, optional): The auth token used to authorize this action.
            Defaults to None.

    Raises:
        HTTPException: 401, 403; if the user does not have permission to perform this action.

    Returns:
        list[models.Chapter]: A list of Chapters with their corresponding organization info.
    """
    auth.get(authorization).logged_in().raise_for_http()

    with db.get_connection() as conn:
        query = db.tb.chapter.select()

        result = conn.execute(query).all()

    return result


@router.get("/{chapter_id}")
def get_specific_chapter(
    chapter_id: int,
    include_members: bool = False,
    authorization: Annotated[str | None, Header()] = None,
) -> models.ChapterWithDetailsAndMembers | models.ChapterWithDetails:
    """_summary_

    Args:
        chapter_id (int): The ID of the chapter to fetch.
        include_members (bool, optional): Whether to include a list of all chapter members in the result.
            Defaults to False.
        authorization (Annotated[str  |  None, Header, optional): The auth token used to authorize this action.
            Defaults to None.

    Raises:
        HTTPException: 404; if the specified chapter does not exist.
        HTTPException: 401, 403; if the user does not have permission to perform this action.

    Returns:
        models.ChapterWithOrgAndMembers | models.ChapterWithOrg: _description_
    """

    # authenticate
    auth_checker = auth.get(authorization)
    if include_members:
        auth_checker.has_chapter_access(chapter_id).raise_for_http()
    else:
        auth_checker.logged_in().raise_for_http()

    # fetch data
    with db.get_connection() as conn:
        chapter_query = (
            select(
                *db.tb.chapter.c,
                db.tb.organization.c.greek_letters,
                db.tb.organization.c.type,
                db.tb.school.c.billing_address.label("sba"),
                db.tb.school.c.name.label("sname"),
            )
            .select_from(db.tb.chapter)
            .join(db.tb.organization)
            .join(db.tb.school)
            .where(db.tb.chapter.c.id == chapter_id)
        )

        result = conn.execute(chapter_query).one_or_none()

        if result is None:
            raise _CHAPTER_NOT_EXISTS

        result = dict(result._mapping)

        result["school"] = models.School(
            name=result.pop("sname"), billing_address=result.pop("sba")
        )
        result["organization"] = models.Organization(
            name=result["org_name"],
            greek_letters=result.pop("greek_letters"),
            type=result.pop("type"),
        )

        logger.debug(result)

        if include_members:
            result["members"] = [
                dict(row._mapping) for row in _get_chapter_members(conn, chapter_id)
            ]

    return (
        models.ChapterWithDetailsAndMembers
        if include_members
        else models.ChapterWithDetails
    )(**result)


@router.delete("/{chapter_id}")
def delete_chapter(
    chapter_id: int, authorization: Annotated[str | None, Header()] = None
):
    """Deletes the specified chapter.

    Args:
        chapter_id (int): The ID of the chapter to delete.
        authorization (Annotated[str  |  None, Header, optional): The auth token used to authorize this action.
            Defaults to None.

    Raises:
        HTTPException: 401, 403; if the user does not have permission to perform this action.
    """
    auth.get(authorization).is_chapter_admin(chapter_id).raise_for_http()

    with db.begin() as conn:
        query = db.tb.chapter.delete().where(db.tb.chapter.c.chapter_id == chapter_id)
        conn.execute(query)


class CreateChapter(BaseModel):
    name: str
    billing_address: str
    org_name: str
    school_name: str


@router.post("")
def create_chapter(
    info: CreateChapter, authorization: Annotated[str | None, Header()] = None
) -> models.Chapter:
    """Creates a chapter.

    Args:
        info (CreateChapter): The specifications of the new chapter.
        authorization (Annotated[str  |  None, Header, optional): The auth token used to authorize this action.
            Defaults to None.

    Raises:
        HTTPException: 401, 403; if the user does not have permission to perform this action.

    Returns:
        models.Chapter: The created chapter.
    """
    auth.get(authorization).logged_in().raise_for_http()

    with db.begin() as conn:

        query = (
            db.tb.chapter.insert().returning(*db.tb.chapter.c).values(info.model_dump())
        )

        result = conn.execute(query).one()

    return result


class UpdateChapter(BaseModel):
    name: str = None
    billing_address: str = None
    org_name: str = None
    school_name: str = None


@router.patch("/{chapter_id}")
def update_chapter(
    chapter_id: int,
    updates: UpdateChapter,
    authorization: Annotated[str | None, Header()] = None,
) -> models.Chapter:
    """Partially updates an existing chapter.

    Args:
        chapter_id (int): The chapter to update.
        updates (UpdateChapter): The fields to update. Any fields that are not provided will not be updated.
        authorization (Annotated[str  |  None, Header, optional): The auth token used to authorize this action.
            Defaults to None.

    Raises:
        HTTPException: 404; if the specified chapter does not exist.
        HTTPException: 401, 403; if the user does not have permission to perform this action.

    Returns:
        models.Chapter: The modified chapter's updated information in its entirety.
    """
    auth.get(authorization).is_chapter_admin(chapter_id).raise_for_http()

    with db.begin() as conn:

        query = (
            db.tb.chapter.update()
            .returning(*db.tb.chapter.c)
            .values(**updates.model_dump(exclude_unset=True))
            .where(db.tb.chapter.c.id == chapter_id)
        )

        result = conn.execute(query).one_or_none()

        if result is None:
            raise _CHAPTER_NOT_EXISTS

    return result


@router.get("/{chapter_id}/members")
def get_chapter_members(
    chapter_id: int, authorization: Annotated[str | None, Header()] = None
) -> list[models.Member]:
    """Returns a list of a specific chapter's members.

    Args:
        chapter_id (int): The ID of the chapter to fetch members for.
        authorization (Annotated[str  |  None, Header, optional): The auth token used to authorize this action.
            Defaults to None.

    Raises:
        HTTPException: 401, 403; if the user does not have permission to perform this action.

    Returns:
        list[models.Member]: The list of members.
    """
    auth.get(authorization).has_chapter_access(chapter_id).raise_for_http()

    with db.get_connection() as conn:
        result = _get_chapter_members(conn, chapter_id)

    return result


@router.get("/{chapter_id}/bills")
def get_chapter_members(
    chapter_id: int, authorization: Annotated[str | None, Header()] = None
) -> list[models.InternalBill | models.ExternalBill]:
    """Returns a list of all outgoing bills made by the specified chapter.

    Args:
        chapter_id (int): The chatper from which to fetch bills.
        authorization (Annotated[str  |  None, Header, optional): The auth token used to authorize this action.
            Defaults to None.

    Raises:
        HTTPException: 401, 403; if the user does not have permission to perform this action.
    """
    auth.get(authorization).is_chapter_admin(chapter_id).raise_for_http()

    with db.get_connection() as conn:
        internal_query = (
            select(*db.tb.bill.c, db.tb.internal_bill.c.member_email)
            .select_from(db.tb.bill)
            .join(db.tb.internal_bill)
            .where(db.tb.bill.c.chapter_id == chapter_id)
        )
        external_query = (
            select(
                *db.tb.bill.c,
                *[c for c in db.tb.external_bill.c if c.name != "bill_id"],
            )
            .select_from(db.tb.bill)
            .join(db.tb.external_bill)
            .where(db.tb.bill.c.chapter_id == chapter_id)
        )

        internal_bills = conn.execute(internal_query).all()
        external_bills = conn.execute(external_query).all()

    return [*internal_bills, *external_bills]
