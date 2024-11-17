from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


@app.post("/login")
async def login():
    return {"message": "Login successful"}


class LoginRequest(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True


class LoginResponse(BaseModel):
    message: str
    organization_id: str
    account_id: str

    class Config:
        orm_mode = True


# Route for LoginRequest
@app.post("/login")
async def login(request: LoginRequest):
    # Simulated login logic
    response = LoginResponse(
        message="Login successful", organization_id="1", account_id="1"
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
async def create_account(request: CreateAccountRequest):

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
async def create_organization(request: CreateOrganizationRequest):

    return {"message": "Organization created successfully"}


class HomePageRequest(BaseModel):
    organization_id: str

    class Config:
        orm_mode = True


class MemberModel(BaseModel):
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


# Route for HomePageRequest
@app.get("/homepage")
async def homepage(request: HomePageRequest):

    response = HomePageResponse(
        organization_name="Frat Incorperated",
        members=[
            MemberModel(name="John Doe", role="President", email="gamer@gmail.com")
        ],
    )
    return response


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


class ViewMyBillsRequest(BaseModel):
    bills: list[BillModel]
    organization_id: str
    member_id: str

    class Config:
        orm_mode = True


# Route for MakeBillRequest
@app.post("/make-bill")
async def make_bill(request: MakeBillRequest):
    bill = {
        "bill_name": request.bill_name,
        "invoicee_id": request.invoicee_id,
        "amount": request.amount,
        "organization_id": request.organization_id,
    }
    return {"message": "Bill created successfully"}


# Route for ViewOutgoingBillRequest
@app.get("/outgoing-bills")
async def view_outgoing_bills(request: ViewOutgoingBillRequest):

    response = ViewOutgoingBillRequest(
        bills=[
            BillModel(
                invoicee_name="John Doe",
                invoicee_id="1",
                bill_name="Rent",
                amount="1000",
                date="2021-10-10",
            )
        ],
        organization_id="1",
    )
    return response


@app.get("/my-bills")
async def view_my_bills(request: ViewMyBillsRequest):

    response = ViewOutgoingBillRequest(
        bills=[
            BillModel(
                invoicee_name="John Doe",
                invoicee_id="1",
                bill_name="Rent",
                amount="1000",
                date="2021-10-10",
            )
        ],
        organization_id="1",
    )
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)