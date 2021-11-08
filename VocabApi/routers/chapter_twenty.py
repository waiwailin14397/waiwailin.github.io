import inspect

from typing import List, Optional

import cruds.chapter_twenty as crud
from schemas.chapter_twenty import ChapterTwentyPost, ChapterTwentyPut, ChapterTwentyDelete
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from utils.db_utils import get_db


router = APIRouter()

@router.get("/get_chapter_twenty", status_code=status.HTTP_200_OK)
async def get_chapter_twenty(next_id: int = 0, db: Session = Depends(get_db)):
    response = crud.get_chapter_twenty(next_id, db)
    return response


@router.post("/post_chapter_twenty", status_code=status.HTTP_200_OK)
async def post_chapter_twenty(body: ChapterTwentyPost, db: Session = Depends(get_db)):
    response = crud.post_chapter_twenty(body, db)
    return response


@router.put("/put_chapter_twenty", status_code=status.HTTP_200_OK)
async def put_chapter_twenty(body: ChapterTwentyPut, db: Session = Depends(get_db)):
    response = crud.put_chapter_twenty(body, db)
    return response


@router.delete("/delete_chapter_twenty", status_code=status.HTTP_200_OK)
async def delete_chapter_twenty(body: ChapterTwentyDelete, db: Session = Depends(get_db)):
    response = crud.delete_chapter_twenty(body, db)
    return response