import inspect

from typing import List, Optional

import cruds.chapter_eighteen as crud
from schemas.chapter_eighteen import ChapterEighteenPost, ChapterEighteenPut, ChapterEighteenDelete
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from utils.db_utils import get_db


router = APIRouter()

@router.get("/get_chapter_eighteen", status_code=status.HTTP_200_OK)
async def get_chapter_eighteen(next_id: int = 0, db: Session = Depends(get_db)):
    response = crud.get_chapter_eighteen(next_id, db)
    return response


@router.post("/post_chapter_eighteen", status_code=status.HTTP_200_OK)
async def post_chapter_eighteen(body: ChapterEighteenPost, db: Session = Depends(get_db)):
    response = crud.post_chapter_eighteen(body, db)
    return response


@router.put("/put_chapter_eighteen", status_code=status.HTTP_200_OK)
async def put_chapter_eighteen(body: ChapterEighteenPut, db: Session = Depends(get_db)):
    response = crud.put_chapter_eighteen(body, db)
    return response


@router.delete("/delete_chapter_eighteen", status_code=status.HTTP_200_OK)
async def delete_chapter_eighteen(body: ChapterEighteenDelete, db: Session = Depends(get_db)):
    response = crud.delete_chapter_eighteen(body, db)
    return response