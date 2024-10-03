from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.core.models.db_helper import db_helper

router = APIRouter(
    tags=["Task"],
    prefix="/task"
)


@router.post("/create")
async def create_task(
        data_task:,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ]
) ->:
    pass
