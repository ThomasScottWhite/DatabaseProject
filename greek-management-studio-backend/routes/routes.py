from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Sample data stores
organizations = {}
accounts = {}
bills = []


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


# Route for LoginRequest
@app.post("/login")
async def login(request: LoginRequest):
    # Simulated login logic
    if request.username in accounts and accounts[request.username] == request.password:
        return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid credentials")


# Route for CreateAccountRequest
@app.post("/create-account")
async def create_account(request: CreateAccountRequest):
    if request.username in accounts:
        raise HTTPException(status_code=400, detail="Account already exists")
    accounts[request.username] = request.password
    return {"message": "Account created successfully"}


# Route for CreateOrganizationRequest
@app.post("/create-organization")
async def create_organization(request: CreateOrganizationRequest):
    if request.organization_name in organizations:
        raise HTTPException(status_code=400, detail="Organization already exists")
    organizations[request.organization_name] = {
        "description": request.description,
        "email": request.email,
        "password": request.password,
        "members": [],
    }
    return {"message": "Organization created successfully"}


# Route for HomePageRequest
@app.get("/homepage")
async def homepage(request: HomePageRequest):
    org = organizations.get(request.organization_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    response = HomePageResponse(
        organization_name=request.organization_id,
        members=[
            MemberSnippet(
                name=member["name"], role=member["role"], email=member["email"]
            )
            for member in org["members"]
        ],
    )
    return response


# Route for MakeBillRequest
@app.post("/make-bill")
async def make_bill(request: MakeBillRequest):
    bill = {
        "bill_name": request.bill_name,
        "invoicee_id": request.invoicee_id,
        "amount": request.amount,
        "organization_id": request.organization_id,
    }
    bills.append(bill)
    return {"message": "Bill created successfully", "bill": bill}


# Route for ViewOutgoingBillRequest
@app.get("/outgoing-bills")
async def view_outgoing_bills(request: ViewOutgoingBillRequest):
    filtered_bills = [
        bill for bill in bills if bill["organization_id"] == request.organization_id
    ]
    return {"bills": filtered_bills}
