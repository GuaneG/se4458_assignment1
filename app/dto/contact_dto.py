from typing import Literal

from pydantic import BaseModel, EmailStr, Field

SortField = Literal["name", "created_at"]
SortOrder = Literal["asc", "desc"]

class ContactBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=50, examples=["Alan"])
    last_name: str = Field(min_length=1, max_length=50, examples=["Turing"])
    email: EmailStr | None = None
    phone: str | None = None
    is_favorite: bool = False

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    pass

class ContactResponse(ContactBase):
    id: int
    
class ContactPatch(BaseModel):
    first_name: str = Field(default=None, min_length=1, max_length=50, examples=["Alan"])
    last_name: str = Field(default=None, min_length=1, max_length=50, examples=["Turing"])
    email: EmailStr | None = None
    phone: str | None = None
    is_favorite: bool = None