import datetime
from typing import Type

from pydantic import BaseModel, Field, create_model


class HasEmail(BaseModel):
    email: str

    # TODO: add email validation to ensure email is a valid email


class PublicUser(HasEmail):
    is_admin: bool


class User(PublicUser):
    password: str


class Member(HasEmail):
    chapter_id: int
    fname: str
    lname: str
    dob: datetime.date | None = None
    member_id: int | None = None
    member_status: str | None = None
    is_chapter_admin: bool | None = None
    phone_num: str | None = None


class MemberWithSiteAdmin(Member):
    is_site_admin: bool


class Chapter(BaseModel):
    name: str
    billing_address: str
    org_name: str
    school_name: str
    id: int


class ChapterWithOrg(Chapter):
    greek_letters: str
    type: str


class ChapterWithOrgAndMembers(ChapterWithOrg):
    members: list[Member]


class School(BaseModel):
    name: str
    billing_address: str


class Organization(BaseModel):
    name: str
    greek_letters: str
    type: str
