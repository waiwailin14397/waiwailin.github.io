import inspect

from typing import List, Optional

import cruds.chapter_eleven as crud
from schemas.chapter_eleven import ChapterElevenPost, ChapterElevenPut, ChapterElevenDelete
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from utils.db_utils import get_db


router = APIRouter()

@router.get("/get_chapter_eleven", status_code=status.HTTP_200_OK)
async def get_chapter_eleven(next_id: int = 0, db: Session = Depends(get_db)):
    response = crud.get_chapter_eleven(next_id, db)
    return response


@router.post("/post_chapter_eleven", status_code=status.HTTP_200_OK)
async def post_chapter_eleven(body: ChapterElevenPost, db: Session = Depends(get_db)):
    response = crud.post_chapter_eleven(body, db)
    return response


@router.put("/put_chapter_eleven", status_code=status.HTTP_200_OK)
async def put_chapter_eleven(body: ChapterElevenPut, db: Session = Depends(get_db)):
    response = crud.put_chapter_eleven(body, db)
    return response


@router.delete("/delete_chapter_eleven", status_code=status.HTTP_200_OK)
async def delete_chapter_eleven(body: ChapterElevenDelete, db: Session = Depends(get_db)):
    response = crud.delete_chapter_eleven(body, db)
    return response