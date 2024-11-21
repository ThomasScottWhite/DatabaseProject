from __future__ import annotations

import time
import uuid
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import select

from api import db, utils

DEFAULT_AUTH_LIFETIME = 7201


class _AuthResult:
    """Class that is returned by each `Auth` function.

    If the instance is "truthy," the specified action is authorized; otherwise,
    it is unauthorized for several potential reasons.

    This class primarily exists to differentiate between the types of failures
    authorization can encounter and respond appropriately.
    """

    def __init__(
        self,
        authorized: bool,
        error_code: int = status.HTTP_403_FORBIDDEN,
        detail: Any = None,
    ):
        self._authorized = authorized
        self._code = error_code
        self._detail = detail

    def raise_for_http(self):
        if not self._authorized:
            raise HTTPException(self._code, self._detail)

    def __bool__(self):
        return self._authorized


AUTHORIZED = _AuthResult(True)
FORBIDDEN = _AuthResult(
    False,
    status.HTTP_403_FORBIDDEN,
    "You do not have the correct permissions to access this resource.",
)
UNAUTHORIZED = _AuthResult(
    False, status.HTTP_401_UNAUTHORIZED, "Your credentials are invalid."
)
EXPIRED = _AuthResult(
    False,
    status.HTTP_401_UNAUTHORIZED,
    "Your authorization has expired. Please reauthenticate.",
)


class Auth:

    _auths: dict[str, Auth] = {}

    @classmethod
    def get_auth(cls, token: str) -> Auth:
        """Fetches a registered `Auth` object by token.

        Args:
            token (str): The token to fetch by.

        Returns:
            Auth: The `Auth` object, or the `NoAuth()` sentinel if `token`
                doesn't correspond with anything.
        """
        return cls._auths.get(token, NoAuth())

    def __init__(
        self,
        token: str,
        email: str,
        global_admin: bool = False,
        chapter: int | None = None,
        chapter_admin: bool = False,
        expires_in: int = DEFAULT_AUTH_LIFETIME,
    ):

        self._token = token
        self._email = email
        self._chapter = chapter
        self._global_admin = global_admin
        self._chapter_admin = chapter_admin
        self._expires = int(time.time()) + expires_in

    @property
    def expired(self) -> bool:
        return self._expires <= time.time()

    @property
    def token(self) -> str:
        return self._token

    @property
    def email(self) -> str:
        return self._email

    @property
    def chapter(self) -> int | None:
        return self._chapter

    @property
    def global_admin(self) -> bool:
        return self._global_admin

    @property
    def chapter_admin(self) -> bool:
        return self._chapter_admin

    def register_self(self):
        self._auths[self._token] = self

    def unregister_self(self):
        del self._auths[self._token]

    def logged_in(self) -> _AuthResult:
        """Returns whether this auth certifies that a user is logged in.

        Only `NoAuth` returns anything except `AUTHORIZED`.

        Returns:
            _AuthResult: `AUTHORIZED`, unless this `Auth` is `NoAuth`.
        """
        return AUTHORIZED

    def is_chapter_admin(self, chapter: int) -> _AuthResult:
        """Returns whether this auth validates a user for chapter admin priviledges for the provided chapter.

        Args:
            chapter (int): The chapter to be access at the administrator level.
        """
        if self.expired:
            self.unregister_self()
            return EXPIRED

        if self._global_admin or (self._chapter == chapter and self._chapter_admin):
            return AUTHORIZED

        return FORBIDDEN

    def has_chapter_access(self, chapter: int) -> _AuthResult:
        """Returns whether this auth validates a user for member priviledges of a chapter.

        Args:
            chapter (int): The chatper to be accessed at the member level.
        """
        if self.expired:
            self.unregister_self()
            return EXPIRED

        if self._global_admin or self._chapter == chapter:
            return AUTHORIZED

        return FORBIDDEN

    def is_user(self, email: str) -> _AuthResult:
        """Returns whether this auth validates full control of the provided user.

        Args:
            email (str): The email of the user to authorize access to.
        """
        if self.expired:
            self.unregister_self()
            return EXPIRED

        if self._global_admin or self._email == email:
            return AUTHORIZED

        return FORBIDDEN

    def is_global_admin(self) -> _AuthResult:
        """Returns whether this auth grants full administrative priviledges."""
        if self.expired:
            self.unregister_self()
            return EXPIRED

        return AUTHORIZED if self._global_admin else FORBIDDEN


class NoAuth(Auth):

    __instance: NoAuth | None = None

    def __new__(cls, *args, **kwargs) -> NoAuth:
        if not cls.__instance:
            cls.__instance = super(NoAuth, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        super().__init__("", "")

    def _sentinel(self, *args, **kwargs) -> _AuthResult:
        return UNAUTHORIZED

    logged_in = is_global_admin = is_user = has_chapter_access = is_chapter_admin = (
        _sentinel
    )


@utils.export
def authenticate(
    email: str, password: str, expires_in: int = DEFAULT_AUTH_LIFETIME
) -> Auth | None:
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

    with db.get_connection() as conn:
        # validate credentials in the database and fetch relevant info
        user = db.tb.user.c  # alias for table columns
        result = conn.execute(
            select(
                user.is_admin,
                db.tb.member.c.chapter_id,
                db.tb.member.c.is_chapter_admin,
            )
            .select_from(db.tb.user)
            .join(db.tb.member, isouter=True)
            .where(user.email == email, user.password == password)
        ).one_or_none()

        # register login if successful
        if result is not None:
            token = str(uuid.uuid4())
            auth_obj = Auth(
                token,
                email,
                result[0],
                result[1],
                result[2] or False,
                expires_in=expires_in,
            )
            auth_obj.register_self()

            return auth_obj


get = Auth.get_auth
utils.export(get)
