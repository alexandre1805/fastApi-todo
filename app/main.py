from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select
from models.item import Item
from utils.db import create_db_and_tables, get_session

app = FastAPI()

create_db_and_tables()

@app.post("/items/")
def create_item(item: Item, session: Session = Depends(get_session)):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@app.patch("/items/{item_id}")
def partial_update_item(item_id: int, item_update: Item, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if item_update.name is not None:
        item.name = item_update.name
    if item_update.description is not None:
        item.description = item_update.description

    session.commit()
    session.refresh(item)

    return item

@app.put("/items/{item_id}")
def update_item(item_id: int, item_update: Item, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item.name = item_update.name
    item.description = item_update.description

    session.commit()
    session.refresh(item)

    return item

@app.get("/items/")
def get_items(session: Session = Depends(get_session)):
    items =session.exec(select(Item)).all()
    return items

@app.get("/items/{item_id}")
def get_item(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
