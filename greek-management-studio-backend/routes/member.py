from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from db import get_db  # Absolute import instead of ..
from models.member import Member  # Absolute import

router = APIRouter()

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


@router.get("/members/{chapter_id}", response_model=List[MemberSchema])
def get_members_by_chapter(chapter_id: int, db: Session = Depends(get_db)):
    members = db.query(Member).filter(Member.chapter_id == chapter_id).all()
    if not members:
        raise HTTPException(status_code=404, detail="Members not found")
    return members
