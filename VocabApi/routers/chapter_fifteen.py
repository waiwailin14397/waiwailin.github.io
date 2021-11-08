import inspect

from typing import List, Optional

import cruds.chapter_fifteen as crud
from schemas.chapter_fifteen import ChapterFifteenPost, ChapterFifteenPut, ChapterFifteenDelete
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from utils.db_utils import get_db


router = APIRouter()

@router.get("/get_chapter_fifteen", status_code=status.HTTP_200_OK)
async def get_chapter_fifteen(next_id: int = 0, db: Session = Depends(get_db)):
    response = crud.get_chapter_fifteen(next_id, db)
    return response


@router.post("/post_chapter_fifteen", status_code=status.HTTP_200_OK)
async def post_chapter_fifteen(body: ChapterFifteenPost, db: Session = Depends(get_db)):
    response = crud.post_chapter_fifteen(body, db)
    return response


@router.put("/put_chapter_fifteen", status_code=status.HTTP_200_OK)
async def put_chapter_fifteen(body: ChapterFifteenPut, db: Session = Depends(get_db)):
    response = crud.put_chapter_fifteen(body, db)
    return response


@router.delete("/delete_chapter_fifteen", status_code=status.HTTP_200_OK)
async def delete_chapter_fifteen(body: ChapterFifteenDelete, db: Session = Depends(get_db)):
    response = crud.delete_chapter_fifteen(body, db)
    return response