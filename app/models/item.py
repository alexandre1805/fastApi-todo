from sqlmodel import Field, SQLModel


class Item(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field()
    description: str | None = Field(
        default=None,
    )
    list_id: int = Field(foreign_key="list.id")
