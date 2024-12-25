from fastapi import APIRouter, Depends, HTTPException, status
from models.item import Item
from models.list import List, ListCreateUpdate
from sqlmodel import Session, select
from utils.auth import User, get_user
from utils.db import get_session

router = APIRouter(prefix="/list", tags=["List"])


@router.post("/")
def create_list(
    list_create: ListCreateUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_user),
) -> List:
    list = List(name=list_create.name, owner=user.username)
    session.add(list)
    session.commit()
    session.refresh(list)
    return list


@router.patch("/{list_id}")
def partial_update_list(
    list_id: int,
    list_update: ListCreateUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_user),
) -> List:
    list = session.get(List, list_id)

    if not list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="List not found"
        )

    if list.owner != user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{user.username} is not the owner of list {list_id}",
        )

    if list_update.name is not None:
        list.name = list_update.name

    session.commit()
    session.refresh(list)

    return list


@router.put("/{list_id}")
def update_list(
    list_id: int,
    list_update: ListCreateUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_user),
) -> List:
    list = session.get(List, list_id)

    if not list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="List not found"
        )

    if list.owner != user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{user.username} is not the owner of list {list_id}",
        )

    list.name = list_update.name
    list.description = list_update.description

    session.commit()
    session.refresh(list)

    return list


@router.get("/")
def get_lists(
    session: Session = Depends(get_session), user: User = Depends(get_user)
) -> list[List]:
    lists = session.exec(select(List).where(List.owner == user.username)).all()
    return lists


@router.get("/{list_id}/items")
def get_list_items(
    list_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_user),
) -> list[Item]:
    list = session.get(List, list_id)
    if not list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="List not found"
        )

    if list.owner != user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{user.username} is not the owner of list {list_id}",
        )

    items = session.exec(select(Item).where(Item.list_id == list_id)).all()
    return items


@router.get("/{list_id}")
def get_list(
    list_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_user),
) -> List:
    list = session.get(List, list_id)
    if not list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="List not found"
        )

    if list.owner != user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{user.username} is not the owner of list {list_id}",
        )

    return list
