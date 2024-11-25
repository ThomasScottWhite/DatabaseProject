import datetime
import logging
from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select

from api import auth, db, models

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/user", tags=["user"])


class MemberInfo(BaseModel):
    chapter_id: int
    fname: str
    lname: str
    dob: datetime.date
    phone_num: str
    is_chapter_admin: bool | None = None


class User(models.HasEmail):
    password: str


class LoginRequest(User):
    expires_in: int = auth.DEFAULT_AUTH_LIFETIME


class LoginResponse(BaseModel):
    message: str
    chapter_id: int | None
    email: str
    auth_token: str
    is_chapter_admin: bool
    is_site_admin: bool


@router.post("/login")
def login(req: LoginRequest) -> LoginResponse:
    """Logs in a user to the application, granting them an authentication token registered
    with the `api.auth` module.

    Args:
        req (LoginRequest): The email and password of the user to log in as.

    Raises:
        HTTPException: 401; If the provided credentials are invalid.

    Returns:
        LoginResponse: The auth token along with basic user info the fronend should keep
            track of.
    """

    logger.info(f"Logging in user {req.email}")
    authorization = db.authenticate(**dict(req))

    if authorization is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, "Provided credentials are invalid."
        )

    return LoginResponse(
        message="Login successful!",
        chapter_id=authorization.chapter,
        email=authorization.email,
        auth_token=authorization.token,
        is_chapter_admin=authorization.chapter_admin,
        is_site_admin=authorization.global_admin,
    )


@router.post("/logout")
def logout(authorization: Annotated[str | None, Header()] = None) -> dict[str, str]:
    """Logs out a user from the application, unregistering them from the `api.auth` module.

    Args:
        authorization (Annotated[str  |  None, Header, optional): The auth token of the user to log out.
            Defaults to None.

    Raises:
        HTTPException: 401, 403; if the user does not have permission to perform this action.

    Returns:
        dict[str, str]: Sucess message.
    """
    authentication = auth.get(authorization)

    authentication.logged_in().raise_for_http()

    authentication.unregister_self()

    return {"message": "Successfully logged out."}


class CreateUserRequest(User):
    is_admin: bool | None = None
    organization_info: MemberInfo | None = None


@router.post("", status_code=status.HTTP_201_CREATED)
def create_user(
    user: CreateUserRequest, authorization: Annotated[str | None, Header()] = None
) -> dict[str, str]:
    """Creates a new user, optionally creating a corresponding chapter member along with it.

    Args:
        user (CreateUserRequest): The user information.
        authorization (Annotated[str  |  None, Header, optional): An auth token (only needed if providing any
            admin permissions on user creation).

    Raises:
        HTTPException: 409; if a user with the provided email already exists
        HTTPException: 401, 403; if the user does not have permission to perform this action.

    Returns:
        dict[str, str]: A confirmation message of success.
    """
    auth_checker = auth.get(authorization)

    with db.get_connection() as conn:

        # check for conflicts
        exists = conn.execute(
            select(1).select_from(db.tb.user).where(db.tb.user.c.email == user.email)
        ).one_or_none()

        if exists is not None:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                f"User with email '{user.email}' already exists.",
            )

        # create new user
        user_values = {"email": user.email, "password": user.password}

        if user.is_admin is not None:
            auth_checker.is_global_admin().raise_for_http()
            user_values["is_admin"] = user.is_admin

        user_insert = db.tb.user.insert().values(user_values)
        conn.execute(user_insert)

        # create member if needed
        if user.organization_info is not None:
            db.create_member(
                conn,
                auth_checker,
                models.CreateMemberRequest(
                    **user.organization_info.model_dump(), email=user.email
                ),
            )

        conn.commit()

    return {"message": "User created!"}


@router.delete("/{user_email}")
def delete_user(user_email: str, authorization: Annotated[str | None, Header()] = None):
    """Deletes the specified user.

    Args:
        user_email (str): _description_
        authorization (Annotated[str  |  None, Header, optional): _description_. Defaults to None.

    Raises:
        HTTPException: 401, 403; if the user does not have permission to perform this action.
    """
    auth_checker = auth.get(authorization)
    auth_checker.is_user(user_email).raise_for_http()

    with db.begin() as conn:
        conn.execute(db.tb.user.delete().where(db.tb.user.c.email == user_email))

        # if the user deletes their own account, invalidate their auth token
        if auth_checker.email == user_email:
            auth_checker.unregister_self()


class UpdateUserRequest(BaseModel):
    password: str | None = None
    is_admin: bool | None = None


@router.patch("/{user_email}")
def update_user(
    user_email: str,
    req: UpdateUserRequest,
    authorization: Annotated[str | None, Header()] = None,
):
    """Update a user's information.

    Args:
        user_email (str): The email of the user to modify.
        req (UpdateUserRequest): The fields to modify.
        authorization (Annotated[str  |  None, Header, optional): The authorization needed to perform this action.
            Defaults to None.

    Raises:
        HTTPException: 400; if both 'password' and 'is_admin' are not provided.
        HTTPException: 401, 403; if the user does not have permission to perform this action.
    """
    if req.password is None and req.is_admin is None:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Must provide 'password', 'is_admin', or both in request body.",
        )

    auth_checker = auth.get(authorization)
    query = db.tb.user.update().where(db.tb.user.c.email == user_email)
    update_clause = dict()
    unregister_auth = False

    if req.is_admin is not None:
        auth_checker.is_global_admin().raise_for_http()
        update_clause["is_admin"] = req.is_admin

    if req.password is not None:
        auth_checker.is_user(user_email).raise_for_http()
        update_clause["password"] = req.password
        unregister_auth = True

    with db.begin() as conn:
        conn.execute(query.values(**update_clause))

    # delay logout to after change goes through
    if unregister_auth:
        auth_checker.unregister_self()


class UserResponse(BaseModel):
    email: str
    is_admin: bool


@router.get("/{user_email}")
def get_user(
    user_email: str, authorization: Annotated[str | None, Header()] = None
) -> UserResponse:
    """Fetch basic user information on a user.

    Args:
        user_email (str): _description_
        authorization (Annotated[str  |  None, Header, optional): The authorization needed to perform this action.
            Defaults to None.

    Raises:
        HTTPException: 404; if the specified user does not exist.
        HTTPException: 401, 403; if the user does not have permission to perform this action.

    Returns:
        UserResponse: The details of the user (excluding their password, of course)
    """
    auth.get(authorization).logged_in().raise_for_http()

    with db.get_connection() as conn:
        user = db.tb.user.c
        query = select(user.email, user.is_admin).where(user.email == user_email)

        result = conn.execute(query).one_or_none()

        if result is None:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, "Requested user does not exist."
            )

        return UserResponse(email=result[0], is_admin=result[1])
