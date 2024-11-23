from __future__ import annotations

import logging
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select

from api import auth, db, models

router = APIRouter(prefix="/organization", tags=["organization"])

logger = logging.getLogger(__name__)
