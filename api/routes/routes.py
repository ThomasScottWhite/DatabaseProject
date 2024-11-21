from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Define allowed origins
origins = [
    "http://localhost:3000",  # Your frontend URL
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,  # Allow cookies and credentials
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


class LoginRequest(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True


class LoginResponse(BaseModel):
    message: str
    organization_id: str
    email: str
    auth_token: str
    is_admin: bool

    class Config:
        orm_mode = True


# Route for LoginRequest
@app.post("/login")
async def login(request: LoginRequest):

    response = LoginResponse(
        message="Login successful",
        organization_id="1",
        email="gamer@gmail.com",
        auth_token="1234",
        is_admin=True,
    )

    return response


class CreateAccountRequest(BaseModel):
    username: str
    password: str
    organization_id: str

    class Config:
        orm_mode = True


# Route for CreateAccountRequest
@app.post("/create-account")
async def create_account(request: CreateAccountRequest, raw_request: Request):
    auth_token = raw_request.headers.get("Authorization")
    if not auth_token:
        raise HTTPException(status_code=401, detail="Authorization token missing")

    return {"message": "Account created successfully"}


class CreateOrganizationRequest(BaseModel):
    organization_name: str
    description: str
    email: str
    password: str

    class Config:
        orm_mode = True


# Route for CreateOrganizationRequest
@app.post("/create-organization")
async def create_organization(request: CreateOrganizationRequest, raw_request: Request):
    auth_token = raw_request.headers.get("Authorization")
    if not auth_token:
        raise HTTPException(status_code=401, detail="Authorization token missing")

    return {"message": "Organization created successfully"}


class HomePageRequest(BaseModel):
    organization_id: str

    class Config:
        orm_mode = True


class MemberModel(BaseModel):
    id: int
    name: str
    role: str
    email: str

    class Config:
        orm_mode = True


class HomePageResponse(BaseModel):
    organization_name: str
    members: list[MemberModel]

    class Config:
        orm_mode = True


@app.get("/homepage")
async def homepage(request: Request):  # request: HomePageRequest
    auth_token = request.headers.get("Authorization")
    if not auth_token:
        raise HTTPException(status_code=401, detail="Authorization token missing")

    response = HomePageResponse(
        organization_name="Frat Incorperated",
        members=[
            MemberModel(
                id=1, name="John Doe", role="President", email="gamer@gmail.com"
            )
        ],
    )
    return response


class MakeBillRequest(BaseModel):
    bill_name: str
    invoicee_id: str
    due_date: str
    amount: float

    class Config:
        orm_mode = True


# Route for MakeBillRequest
@app.post("/make-bill")
async def make_bill(request: MakeBillRequest, raw_request: Request):
    auth_token = raw_request.headers.get("Authorization")
    if not auth_token:
        raise HTTPException(status_code=401, detail="Authorization token missing")

    bill = {
        "bill_name": request.bill_name,
        "invoicee_id": request.invoicee_id,
        "amount": request.amount,
        "due_date": request.due_date,
    }
    return {"message": "Bill created successfully"}


class MakeExternalBillRequest(BaseModel):
    bill_name: str
    chapter_contact: str
    payer_name: str
    payer_bill_address: str
    payer_email: str
    payer_phone: str
    due_date: str
    amount: float

    class Config:
        orm_mode = True


@app.post("/make-external-bill")
async def make_bill(request: MakeExternalBillRequest, raw_request: Request):
    auth_token = raw_request.headers.get("Authorization")
    if not auth_token:
        raise HTTPException(status_code=401, detail="Authorization token missing")

    bill = {
        "bill_name": request.bill_name,
        "invoicee_id": request.invoicee_id,
        "amount": request.amount,
    }
    return {"message": "Bill created successfully"}


class BillModel(BaseModel):
    invoicee_name: str
    invoicee_id: str
    bill_id: int
    bill_name: str
    amount: str
    date: str
    paid: bool

    class Config:
        orm_mode = True


class ViewOutgoingBillRequest(BaseModel):
    bills: list[BillModel]
    organization_id: str

    class Config:
        orm_mode = True


# Route for ViewOutgoingBillRequest
@app.get("/outgoing-bills")
async def view_outgoing_bills(request: Request):  # request: ViewOutgoingBillRequest
    auth_token = request.headers.get("Authorization")
    if not auth_token:
        raise HTTPException(status_code=401, detail="Authorization token missing")

    response = ViewOutgoingBillRequest(
        bills=[
            BillModel(
                invoicee_name="John Doe",
                invoicee_id="1",
                bill_id=1,
                bill_name="Rent",
                amount="1000",
                date="2021-10-10",
                paid=False,
            )
        ],
        organization_id="1",
    )
    return response


class ViewMyBillsRequest(BaseModel):
    bills: list[BillModel]

    class Config:
        orm_mode = True


@app.get("/my-bills")
async def view_my_bills(request: Request):
    auth_token = request.headers.get("Authorization")
    if not auth_token:
        raise HTTPException(status_code=401, detail="Authorization token missing")

    response = ViewMyBillsRequest(
        bills=[
            BillModel(
                invoicee_name="John Doe",
                invoicee_id="1",
                bill_id=1,
                bill_name="Rent",
                amount="1000",
                date="2021-10-10",
                paid=False,
            )
        ],
        organization_id="1",
    )
    return response


class paymentRequest(BaseModel):
    bill_id: int
    amount: float
    card_number: str
    ccv: str

    class Config:
        orm_mode = True


@app.post("/payment")
async def login(request: paymentRequest):

    response = {
        "message": "Payment successful",
    }
    return response

class editUserRequest(BaseModel):
    id: int
    name: str
    role: str
    email: str

    class Config:
        orm_mode = True


@app.post("/edit-user")
async def login(request: editUserRequest):

    response = {
        "message": "Edited User Successfully",
    }
    return response

class editBillRequest(BaseModel):
    invoicee_name: str
    invoicee_id: str
    bill_id: int
    bill_name: str
    amount: str
    date: str
    paid: bool

    class Config:
        orm_mode = True


@app.post("/edit-bill")
async def editBill(request: editBillRequest):

    response = {
        "message": "Payment successful",
    }
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6969)
