import inspect

from typing import List, Optional

import cruds.chapter_twelve as crud
from schemas.chapter_twelve import ChapterTwelvePost, ChapterTwelvePut, ChapterTwelveDelete
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from utils.db_utils import get_db


router = APIRouter()

@router.get("/get_chapter_twelve", status_code=status.HTTP_200_OK)
async def get_chapter_twelve(next_id: int = 0, db: Session = Depends(get_db)):
    response = crud.get_chapter_twelve(next_id, db)
    return response


@router.post("/post_chapter_twelve", status_code=status.HTTP_200_OK)
async def post_chapter_twelve(body: ChapterTwelvePost, db: Session = Depends(get_db)):
    response = crud.post_chapter_twelve(body, db)
    return response


@router.put("/put_chapter_twelve", status_code=status.HTTP_200_OK)
async def put_chapter_twelve(body: ChapterTwelvePut, db: Session = Depends(get_db)):
    response = crud.put_chapter_twelve(body, db)
    return response


@router.delete("/delete_chapter_twelve", status_code=status.HTTP_200_OK)
async def delete_chapter_twelve(body: ChapterTwelveDelete, db: Session = Depends(get_db)):
    response = crud.delete_chapter_twelve(body, db)
    return response