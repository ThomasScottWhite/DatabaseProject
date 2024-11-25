import datetime

from pydantic import BaseModel


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
    school: School
    organization: Organization


class ChapterWithDetailsAndMembers(ChapterWithDetails):
    members: list[Member]


class OrganizationWithChapters(Organization):
    chapters: list[Chapter]


class SchoolWithChapters(School):
    chapters: list[Chapter]


class PaymentInfo(BaseModel):
    member_email: str
    payment_id: int
    nickname: str | None


class BankAccount(PaymentInfo):
    account_num: int
    routing_num: int


class Card(PaymentInfo):
    card_num: int
    security_code: int
    exp_date: str
    name: str
