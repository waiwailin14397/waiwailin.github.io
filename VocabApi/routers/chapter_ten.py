import inspect

from typing import List, Optional

import cruds.chapter_ten as crud
from schemas.chapter_ten import ChapterTenPost, ChapterTenPut, ChapterTenDelete
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from utils.db_utils import get_db


router = APIRouter()

@router.get("/get_chapter_ten", status_code=status.HTTP_200_OK)
async def get_chapter_ten(next_id: int = 0, db: Session = Depends(get_db)):
    response = crud.get_chapter_ten(next_id, db)
    return response


@router.post("/post_chapter_ten", status_code=status.HTTP_200_OK)
async def post_chapter_ten(body: ChapterTenPost, db: Session = Depends(get_db)):
    response = crud.post_chapter_ten(body, db)
    return response


@router.put("/put_chapter_ten", status_code=status.HTTP_200_OK)
async def put_chapter_ten(body: ChapterTenPut, db: Session = Depends(get_db)):
    response = crud.put_chapter_ten(body, db)
    return response


@router.delete("/delete_chapter_ten", status_code=status.HTTP_200_OK)
async def delete_chapter_ten(body: ChapterTenDelete, db: Session = Depends(get_db)):
    response = crud.delete_chapter_ten(body, db)
    return response