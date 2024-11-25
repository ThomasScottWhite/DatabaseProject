from __future__ import annotations

import logging
from typing import Annotated, Any, Sequence

from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import Connection, Row

from api import auth, db, models

router = APIRouter(prefix="/organization", tags=["organization"])

logger = logging.getLogger(__name__)


def _get_org_chapters(conn: Connection, org_name: str) -> Sequence[Row[Any]]:
    """Returns all chapters belonging to an organization.

    Args:
        conn (Connection): The database connection to use.
        org_name (str): The name of the organization.
    """
    query = db.tb.chapter.select().where(db.tb.chapter.c.org_name == org_name)
    return conn.execute(query).all()


@router.get("")
def get_all_organizations() -> list[models.Organization]:
    """Returns a list of all organizations in the database.

    This does not require authentication to use.
    """
    with db.get_connection() as conn:
        result = conn.execute(db.tb.organization.select()).all()
    return result


@router.post("", status_code=status.HTTP_204_NO_CONTENT)
def create_organization(
    specification: models.Organization,
    authorization: Annotated[str | None, Header()] = None,
):
    """Creates an organization based on the provided specifications.

    Args:
        specification (models.Organization): The fields of the organization to create.
        authorization (Annotated[str  |  None, Header, optional): The auth token used to authorize this action.
            Defaults to None.

    Raises:
        HTTPException: 401, 403; if the user does not have permission to perform this action.
    """
    auth.get(authorization).is_global_admin().raise_for_http()

    with db.begin() as conn:

        query = db.tb.organization.insert().values(specification.model_dump())
        conn.execute(query)


@router.get("/{org_name}")
def get_specific_organization(
    org_name: str,
    include_chapters: bool = False,
) -> models.OrganizationWithChapters | models.Organization:
    """Returns a specific organization, optionally with all chapters belonging to it.

    Args:
        org_name (str): The name of the desired organization.
        include_chapters (bool, optional): Whether to include chapters with the result.
            Defaults to False.

    Raises:
        HTTPException: 404; if the provided organization does not exist.
    """

    with db.get_connection() as conn:

        org_query = db.tb.organization.select().where(
            db.tb.organization.c.name == org_name
        )
        result = conn.execute(org_query).one_or_none()

        if result is None:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, "Specified organization does not exist."
            )

        result = dict(result._mapping)

        if include_chapters:
            result["chapters"] = _get_org_chapters(conn, org_name)

    return result


@router.get("/{org_name}/chapters")
def get_organization_chapters(org_name: str) -> list[models.Chapter]:
    """Returns a list of chapters belonging to the provided organization.

    Args:
        org_name (str): The name of the organization for which to retreive chapters.
    """
    with db.get_connection() as conn:
        result = _get_org_chapters(conn, org_name)

    return result


@router.delete("/{org_name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_organization(
    org_name: str,
    authorization: Annotated[str | None, Header()] = None,
):
    """Deletes the specified organization.

    Note: this will remove all related chapters, members, and bills.

    Args:
        org_name (str): The name of the organization to remove.
        authorization (Annotated[str  |  None, Header, optional): The auth token used to authorize this action.
            Defaults to None.

    Raises:
        HTTPException: 401, 403; if the user does not have permission to perform this action.
    """
    auth.get(authorization).is_global_admin().raise_for_http()

    with db.begin() as conn:
        query = (
            db.tb.organization.delete()
            .returning(*db.tb.organization.c)
            .where(db.tb.organization.c.name == org_name)
        )
        result = conn.execute(query).one_or_none()

        if result is None:
            raise HTTPException(status.HTTP_304_NOT_MODIFIED, "Nothing was deleted.")


class OrganizationUpdateRequest(BaseModel):
    name: str = None
    greek_letters: str = None
    type: str = None


@router.patch("/{org_name}")
def update_organization(
    org_name: str,
    updates: OrganizationUpdateRequest,
    authorization: Annotated[str | None, Header()] = None,
) -> models.Organization:
    """Partially updates an organization based on the provided `updates`.

    Args:
        org_name (str): The name of the organization to update.
        updates (OrganizationUpdateRequest): The changes to make (exclude fields to leave them unmodified).
        authorization (Annotated[str  |  None, Header, optional): The auth token used to authorize this action.
            Defaults to None.

    Raises:
        HTTPException: 304; if no modifications are made.
        HTTPException: 401, 403; if the user does not have permission to perform this action.

    Returns:
        models.Organization: The modified organiation in its entirety as now reflected in the database.
    """
    auth.get(authorization).is_global_admin().raise_for_http()

    with db.begin() as conn:

        query = (
            db.tb.organization.update()
            .returning(*db.tb.organization.c)
            .where(db.tb.organization.c.name == org_name)
            .values(**updates.model_dump(exclude_unset=True))
        )
        result = conn.execute(query).one_or_none()

        if result is None:
            raise HTTPException(status.HTTP_304_NOT_MODIFIED)

    return result
