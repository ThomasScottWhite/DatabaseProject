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


class CreateMemberRequest(HasEmail):
    chapter_id: int
    fname: str
    lname: str
    dob: datetime.date
    phone_num: str
    member_status: str | None = None
    is_chapter_admin: bool | None = None


class MemberWithSiteAdmin(Member):
    is_site_admin: bool


class School(BaseModel):
    name: str
    billing_address: str


class Organization(BaseModel):
    name: str
    greek_letters: str
    type: str


class Chapter(BaseModel):
    name: str
    billing_address: str
    org_name: str
    school_name: str
    id: int


class ChapterWithDetails(Chapter):
    organization: Organization
    school: School


class ChapterWithDetailsAndMembers(ChapterWithDetails):
    members: list[Member]
