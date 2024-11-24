from __future__ import annotations

import logging
from datetime import date
from typing import Annotated, Any, Sequence

from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import Connection, Row, select

from api import auth, db, models

router = APIRouter(prefix="/school", tags=["school"])

logger = logging.getLogger(__name__)


def _get_school_chapters(conn: Connection, school_name: str) -> Sequence[Row[Any]]:
    """Returns all chapters belonging to a school.

    Args:
        conn (Connection): The database connection to use.
        school_name (str): The name of the school.
    """
    query = db.tb.chapter.select().where(db.tb.chapter.c.school_name == school_name)
    return conn.execute(query).all()


@router.get("")
def get_all_schools() -> list[models.School]:
    """Returns a list of all schools in the database.

    This does not require authentication to use.
    """
    with db.get_connection() as conn:
        result = conn.execute(db.tb.school.select()).all()
    return result


@router.post("", status_code=status.HTTP_204_NO_CONTENT)
def create_school(
    specification: models.School,
    authorization: Annotated[str | None, Header()] = None,
):
    """Creates a school based on the provided specifications.

    Args:
        specification (models.School): The fields of the school to create.
        authorization (Annotated[str  |  None, Header, optional): The auth token used to authorize this action.
            Defaults to None.

    Raises:
        HTTPException: 401, 403; if the user does not have permission to perform this action.
    """
    auth.get(authorization).is_global_admin().raise_for_http()

    with db.begin() as conn:

        query = db.tb.school.insert().values(specification.model_dump())
        conn.execute(query)


@router.get("/{school_name}")
def get_specific_school(
    school_name: str,
    include_chapters: bool = False,
) -> models.SchoolWithChapters | models.School:
    """Returns a specific school, optionally with all chapters belonging to it.

    Args:
        school_name (str): The name of the desired school.
        include_chapters (bool, optional): Whether to include chapters with the result.
            Defaults to False.

    Raises:
        HTTPException: 404; if the provided school does not exist.
    """

    with db.get_connection() as conn:

        org_query = db.tb.school.select().where(db.tb.school.c.name == school_name)
        result = conn.execute(org_query).one_or_none()

        if result is None:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, "Specified school does not exist."
            )

        result = dict(result._mapping)

        if include_chapters:
            result["chapters"] = _get_school_chapters(conn, school_name)

    return result


@router.get("/{school_name}/chapters")
def get_school_chapters(school_name: str) -> list[models.Chapter]:
    """Returns a list of chapters belonging to the provided school.

    Args:
        school_name (str): The name of the school for which to retreive chapters.
    """
    with db.get_connection() as conn:
        result = _get_school_chapters(conn, school_name)

    return result


@router.delete("/{school_name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_school(
    school_name: str,
    authorization: Annotated[str | None, Header()] = None,
):
    """Deletes the specified school.

    Note: this will remove all related chapters, members, and bills.

    Args:
        school_name (str): The name of the school to remove.
        authorization (Annotated[str  |  None, Header, optional): The auth token used to authorize this action.
            Defaults to None.

    Raises:
        HTTPException: 304; if nothing was deleted.
        HTTPException: 401, 403; if the user does not have permission to perform this action.
    """
    auth.get(authorization).is_global_admin().raise_for_http()

    with db.begin() as conn:
        query = (
            db.tb.school.delete()
            .returning(*db.tb.school.c)
            .where(db.tb.school.c.name == school_name)
        )
        result = conn.execute(query).one_or_none()

        if result is None:
            raise HTTPException(status.HTTP_304_NOT_MODIFIED, "Nothing was deleted.")


class SchoolUpdateRequest(BaseModel):
    name: str = None
    billing_address: str = None


@router.patch("/{school_name}")
def update_school(
    school_name: str,
    updates: SchoolUpdateRequest,
    authorization: Annotated[str | None, Header()] = None,
) -> models.School:
    """Partially updates a school based on the provided `updates`.

    Args:
        school_name (str): The name of the school to update.
        updates (SchoolUpdateRequest): The changes to make (exclude fields to leave them unmodified).
        authorization (Annotated[str  |  None, Header, optional): The auth token used to authorize this action.
            Defaults to None.

    Raises:
        HTTPException: 304; if no modifications are made.
        HTTPException: 401, 403; if the user does not have permission to perform this action.

    Returns:
        models.School: The modified school in its entirety as now reflected in the database.
    """
    auth.get(authorization).is_global_admin().raise_for_http()

    with db.begin() as conn:

        query = (
            db.tb.school.update()
            .returning(*db.tb.school.c)
            .where(db.tb.school.c.name == school_name)
            .values(**updates.model_dump(exclude_unset=True))
        )
        result = conn.execute(query).one_or_none()

        if result is None:
            raise HTTPException(status.HTTP_304_NOT_MODIFIED)

    return result
