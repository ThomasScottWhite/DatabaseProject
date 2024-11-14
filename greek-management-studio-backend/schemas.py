from pydantic import BaseModel
from typing import Optional
from datetime import date

class MemberSchema(BaseModel):
    chapter_id: int
    email: str
    fname: str
    lname: str
    dob: Optional[date] = None
    member_id: Optional[int] = None
    member_status: Optional[str] = None
    is_chapter_admin: Optional[bool] = None
    phone_num: Optional[str] = None

    class Config:
        orm_mode = True
