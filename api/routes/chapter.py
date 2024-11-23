from __future__ import annotations

import logging
from datetime import date
from typing import Annotated, Any, Sequence

from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import Connection, Row, Select, select

from api import auth, db, models

# from api.db import get_db  # Absolute import instead of ..

router = APIRouter(prefix="/chapter")

logger = logging.getLogger(__name__)


def _get_chapter_members(conn: Connection, chapter_id: int) -> Sequence[Row[Any]]:
    return conn.execute(
        db.tb.member.select().where(db.tb.member.c.chapter_id == chapter_id)
    ).all()


@router.get("")
def get_all_chapters(
    org_name: str | None = None, authorization: Annotated[str | None, Header()] = None
) -> list[models.Chapter]:
    auth.get(authorization).logged_in().raise_for_http()

    with db.get_connection() as conn:

        query = db.tb.chapter.select()

        if org_name is not None:
            query = query.where(db.tb.chapter.c.org_name == org_name)

        result = conn.execute(query).all()

    return result


@router.get("/{chapter_id}")
def get_specific_chapter(
    chapter_id: int,
    include_members: bool = False,
    authorization: Annotated[str | None, Header()] = None,
) -> models.ChapterWithOrgAndMembers | models.ChapterWithOrg:

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


@router.get("/{chapter_id}/members")
def get_chapter_members(
    chapter_id: int, authorization: Annotated[str | None, Header()] = None
) -> list[models.Member]:
    auth.get(authorization).has_chapter_access(chapter_id).raise_for_http()

    with db.get_connection() as conn:
        result = _get_chapter_members(conn, chapter_id)

    return result
