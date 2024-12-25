from fastapi import APIRouter, Depends, HTTPException, status
from models.item import Item
from models.list import List
from sqlmodel import Session, select
from utils.auth import User, get_user
from utils.db import get_session

router = APIRouter(prefix="/item", tags=["Item"])


@router.post("/")
def create_item(
    item: Item, session: Session = Depends(get_session), user: User = Depends(get_user)
) -> Item:
    list = session.get(List, item.list_id)

    if not list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="List not found"
        )

    if list.owner != user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{user.username} is not the owner of list {item.list_id}",
        )
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.patch("/{item_id}")
def partial_update_item(
    item_id: int,
    item_update: Item,
    session: Session = Depends(get_session),
    user: User = Depends(get_user),
) -> Item:
    item = session.get(Item, item_id)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )

    list = session.get(List, item.list_id)
    if list.owner != user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{user.username} is not the owner of list {item.list_id}",
        )

    if item_update.name is not None:
        item.name = item_update.name

    session.commit()
    session.refresh(item)

    return item


@router.put("/{item_id}")
def update_item(
    item_id: int,
    item_update: Item,
    session: Session = Depends(get_session),
    user: User = Depends(get_user),
) -> Item:
    item = session.get(Item, item_id)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )

    list = session.get(List, item.list_id)
    if list.owner != user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{user.username} is not the owner of list {item.list_id}",
        )

    item.name = item_update.name

    session.commit()
    session.refresh(item)

    return item


@router.get("/")
def get_items(
    session: Session = Depends(get_session), user: User = Depends(get_user)
) -> list[Item]:
    items = session.exec(
        select(Item).join(List).where(List.owner == user.username)
    ).all()
    return items


@router.get("/{item_id}")
def get_item(
    item_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_user),
) -> Item:
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )

    list = session.get(List, item.list_id)
    if list.owner != user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{user.username} is not the owner of list {item.list_id}",
        )

    return item
