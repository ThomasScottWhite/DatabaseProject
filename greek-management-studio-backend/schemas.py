from pydantic import BaseModel
from typing import Optional
from datetime import date


class LoginRequest(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True


class CreateAccountRequest(BaseModel):
    username: str
    password: str
    organization_id: str

    class Config:
        orm_mode = True


class CreateOrganizationRequest(BaseModel):
    organization_name: str
    description: str
    email: str
    password: str

    class Config:
        orm_mode = True


class HomePageRequest(BaseModel):
    organization_id: str

    class Config:
        orm_mode = True


class MemberSnippet(BaseModel):
    name: str
    role: str
    email: str

    class Config:
        orm_mode = True


class HomePageResponse(BaseModel):
    organization_name: str
    members: list[MemberSnippet]

    class Config:
        orm_mode = True


class MakeBillRequest(BaseModel):
    bill_name: str
    invoicee_id: str
    amount: float
    organization_id: str

    class Config:
        orm_mode = True


class BillModel(BaseModel):
    invoicee_name: str
    invoicee_id: str
    bill_name: str
    amount: str
    date: str

    class Config:
        orm_mode = True


class ViewOutgoingBillRequest(BaseModel):
    bills: list[BillModel]
    organization_id: str

    class Config:
        orm_mode = True


class ViewOutgoingBillRequest(BaseModel):
    bills: list[BillModel]
    organization_id: str
    member_id: str

    class Config:
        orm_mode = True
