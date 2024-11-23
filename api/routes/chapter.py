from __future__ import annotations

import logging
from datetime import date
from typing import Annotated, Any, Final, Sequence

from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import Connection, Row, Select, select

from api import auth, db, models

router = APIRouter(prefix="/chapter", tags=["chapter"])

logger = logging.getLogger(__name__)


def _get_chapter_members(conn: Connection, chapter_id: int) -> Sequence[Row[Any]]:
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
        query = db.tb.select()

        result = conn.execute(query).all()

    return result


@router.get("/{chapter_id}")
def get_specific_chapter(
    chapter_id: int,
    include_members: bool = False,
    authorization: Annotated[str | None, Header()] = None,
) -> models.ChapterWithOrgAndMembers | models.ChapterWithOrg:
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
            )
            .select_from(db.tb.chapter)
            .join(db.tb.organization)
            .where(db.tb.chapter.c.id == chapter_id)
        )

        result = conn.execute(chapter_query).one_or_none()

        if result is None:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, "Specified chapter does not exist"
            )

        result = dict(result._mapping)

        logger.debug(result)

        if include_members:
            result["members"] = [
                dict(row._mapping) for row in _get_chapter_members(conn, chapter_id)
            ]

    return (
        models.ChapterWithOrgAndMembers if include_members else models.ChapterWithOrg
    )(**result)


@router.delete("/{chapter_id}")
def get_specific_chapter(
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

    with db.get_engine().begin() as conn:
        query = db.tb.chapter.delete().where(db.tb.chapter.c.chapter_id == chapter_id)
        conn.execute(query)


@router.post("/{chapter_id}")
def get_specific_chapter(
    chapter_id: int, authorization: Annotated[str | None, Header()] = None
):
    pass


@router.patch("/{chapter_id}")
def get_specific_chapter(
    chapter_id: int, authorization: Annotated[str | None, Header()] = None
):
    pass


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
