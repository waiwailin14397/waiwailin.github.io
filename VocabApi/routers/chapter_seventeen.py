import inspect

from typing import List, Optional

import cruds.chapter_seventeen as crud
from schemas.chapter_seventeen import ChapterSeventeenPost, ChapterSeventeenPut, ChapterSeventeenDelete
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from utils.db_utils import get_db


router = APIRouter()

@router.get("/get_chapter_seventeen", status_code=status.HTTP_200_OK)
async def get_chapter_seventeen(next_id: int = 0, db: Session = Depends(get_db)):
    response = crud.get_chapter_seventeen(next_id, db)
    return response


@router.post("/post_chapter_seventeen", status_code=status.HTTP_200_OK)
async def post_chapter_seventeen(body: ChapterSeventeenPost, db: Session = Depends(get_db)):
    response = crud.post_chapter_seventeen(body, db)
    return response


@router.put("/put_chapter_seventeen", status_code=status.HTTP_200_OK)
async def put_chapter_seventeen(body: ChapterSeventeenPut, db: Session = Depends(get_db)):
    response = crud.put_chapter_seventeen(body, db)
    return response


@router.delete("/delete_chapter_seventeen", status_code=status.HTTP_200_OK)
async def delete_chapter_seventeen(body: ChapterSeventeenDelete, db: Session = Depends(get_db)):
    response = crud.delete_chapter_seventeen(body, db)
    return response