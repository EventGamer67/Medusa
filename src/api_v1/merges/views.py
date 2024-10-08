import os
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache

from src.alchemy.db_helper import *
from . import crud
from .schemas import MergeResult

router = APIRouter(tags=["Merge"])

pass_ = os.environ.get("API_SECRET")


@router.patch("/teachers/{merge_from_id}/{merge_to_id}/{password}/")
async def merge_teachers(
    merge_from_id: int,
    merge_to_id: int,
    password: str,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> MergeResult:
    if password == pass_:
        raise HTTPException(status_code=403, detail="Not allowed")
    return await crud.merge_teachers(
        session=session, merge_from_id=merge_from_id, merge_to_id=merge_to_id
    )


@router.patch("/cabinets/{merge_from_id}/{merge_to_id}/{password}/")
async def merge_cabinets(
    merge_from_id: int,
    merge_to_id: int,
    password: str,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> MergeResult:
    if password == pass_:
        raise HTTPException(status_code=403, detail="Not allowed")
    return await crud.merge_cabinets(
        session=session, merge_from_id=merge_from_id, merge_to_id=merge_to_id
    )


@router.patch("/groups/{merge_from_id}/{merge_to_id}/{password}/")
async def merge_groups(
    merge_from_id: int,
    merge_to_id: int,
    password: str,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> MergeResult:
    if password == pass_:
        raise HTTPException(status_code=403, detail="Not allowed")
    return await crud.merge_groups(
        session=session, merge_from_id=merge_from_id, merge_to_id=merge_to_id
    )
