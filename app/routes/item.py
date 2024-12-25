from fastapi import APIRouter, Depends, HTTPException, status
from models.item import Item
from sqlmodel import Session, select
from utils.auth import get_auth
from utils.db import get_session

router = APIRouter(prefix="/item", tags=["Item"])


@router.post("/")
def create_item(item: Item, session: Session = Depends(get_session)) -> Item:
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.patch("/{item_id}")
def partial_update_item(
    item_id: int, item_update: Item, session: Session = Depends(get_session)
) -> Item:
    item = session.get(Item, item_id)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )

    if item_update.name is not None:
        item.name = item_update.name
    if item_update.description is not None:
        item.description = item_update.description

    session.commit()
    session.refresh(item)

    return item


@router.put("/{item_id}")
def update_item(
    item_id: int, item_update: Item, session: Session = Depends(get_session)
) -> Item:
    item = session.get(Item, item_id)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )

    item.name = item_update.name
    item.description = item_update.description

    session.commit()
    session.refresh(item)

    return item


@router.get("/", dependencies=[Depends(get_auth)])
def get_items(session: Session = Depends(get_session)) -> list[Item]:
    items = session.exec(select(Item)).all()
    return items


@router.get("/{item_id}")
def get_item(item_id: int, session: Session = Depends(get_session)) -> Item:
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return item
