import inspect

from typing import List

import cruds.vocab_chapter as crud
from schemas.vocab_chapter import VocabChapterPost, VocabChapterPut, VocabChapterDelete, VocabChapterGet
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from utils.db_utils import get_db


router = APIRouter()

@router.get("/")
async def check_db(db: Session = Depends(get_db)):
    response = crud.check_db(db)
    return response


@router.get("/get_chapter", status_code=status.HTTP_200_OK)
async def get_chapter_data(body: VocabChapterGet, db: Session = Depends(get_db)):
    response = crud.get_chapter(body, db)
    return response


@router.post("/post_chapter", status_code=status.HTTP_200_OK)
async def post_chapter_data(body: VocabChapterPost, db: Session = Depends(get_db)):
    response = crud.post_chapter(body, db)
    return response


@router.put("/put_chapter", status_code=status.HTTP_200_OK)
async def put_chapter_data(body: VocabChapterPut, db: Session = Depends(get_db)):
    response = crud.put_chapter(body, db)
    return response


@router.delete("/delete_chapter", status_code=status.HTTP_200_OK)
async def delete_chapter_data(body: VocabChapterDelete, db: Session = Depends(get_db)):
    response = crud.delete_chapter(body, db)
    return response