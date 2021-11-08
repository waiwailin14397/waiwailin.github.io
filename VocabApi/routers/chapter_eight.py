import inspect

from typing import List, Optional

import cruds.chapter_eight as crud
from schemas.chapter_eight import ChapterEightPost, ChapterEightPut, ChapterEightDelete
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from utils.db_utils import get_db


router = APIRouter()

@router.get("/get_chapter_eight", status_code=status.HTTP_200_OK)
async def get_chapter_eight(next_id: int = 0, db: Session = Depends(get_db)):
    response = crud.get_chapter_eight(next_id, db)
    return response


@router.post("/post_chapter_eight", status_code=status.HTTP_200_OK)
async def post_chapter_eight(body: ChapterEightPost, db: Session = Depends(get_db)):
    response = crud.post_chapter_eight(body, db)
    return response


@router.put("/put_chapter_eight", status_code=status.HTTP_200_OK)
async def put_chapter_eight(body: ChapterEightPut, db: Session = Depends(get_db)):
    response = crud.put_chapter_eight(body, db)
    return response


@router.delete("/delete_chapter_eight", status_code=status.HTTP_200_OK)
async def delete_chapter_eight(body: ChapterEightDelete, db: Session = Depends(get_db)):
    response = crud.delete_chapter_eight(body, db)
    return response