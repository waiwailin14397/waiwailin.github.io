import inspect

from typing import List, Optional

import cruds.chapter_two as crud
from schemas.chapter_two import ChapterTwoPost, ChapterTwoPut, ChapterTwoDelete
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from utils.db_utils import get_db


router = APIRouter()

@router.get("/get_chapter_two", status_code=status.HTTP_200_OK)
async def get_chapter_two(next_id: int = 0, db: Session = Depends(get_db)):
    response = crud.get_chapter_two(next_id, db)
    return response


@router.post("/post_chapter_two", status_code=status.HTTP_200_OK)
async def post_chapter_two(body: ChapterTwoPost, db: Session = Depends(get_db)):
    response = crud.post_chapter_two(body, db)
    return response


@router.put("/put_chapter_two", status_code=status.HTTP_200_OK)
async def put_chapter_two(body: ChapterTwoPut, db: Session = Depends(get_db)):
    response = crud.put_chapter_two(body, db)
    return response


@router.delete("/delete_chapter_two", status_code=status.HTTP_200_OK)
async def delete_chapter_two(body: ChapterTwoDelete, db: Session = Depends(get_db)):
    response = crud.delete_chapter_two(body, db)
    return response