from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class UserSchema(BaseModel):
    username: str | None = None


class UserWithPasswordSchema(BaseModel):
    username: str | None = None
    password: str | None = None


class ItemSchema(BaseModel):
    name: str | None = None
    description: str | None = None
    category: str | None = None
    quantity: int
    price: float


class UserItemSchema(BaseModel):
    name: str
