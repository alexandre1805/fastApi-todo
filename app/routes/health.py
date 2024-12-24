
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from utils.db import get_session


router = APIRouter(
    prefix='/health',
    tags=['Health']
)

@router.get(
    '',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
            status.HTTP_503_SERVICE_UNAVAILABLE: {
                'description': 'Database connection is unavailable',
            }
        }
)
def health(
    session: Session = Depends(get_session),
):
    try:
        #  SELECT 1 is a simple SQL query used to test database connectivity
       session.exec(select(1))
    except:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database connection is unavailable")
    return
