"""Pydantic request/response models."""

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=64, pattern=r"^[a-zA-Z0-9_.-]+$")
    # bcrypt rejects passwords longer than 72 bytes, so enforce it up front
    password: str = Field(min_length=8, max_length=72)


class UserLogin(BaseModel):
    username: str
    password: str


class UserPublic(BaseModel):
    username: str
    is_active: bool = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
