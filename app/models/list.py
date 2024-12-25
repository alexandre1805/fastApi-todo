from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class List(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field()
    owner: str = Field()


class ListCreateUpdate(BaseModel):
    name: str
