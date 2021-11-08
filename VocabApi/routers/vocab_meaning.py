import inspect

from typing import List, Optional

import cruds.vocab_meaning as crud
from schemas.vocab_meaning import VocabMeaningPost, VocabMeaningPut, VocabMeaningDelete
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from utils.db_utils import get_db


router = APIRouter()

@router.get("/get_vocab", status_code=status.HTTP_200_OK)
async def get_vocab(chapter_id: int = 1, next_id: int = 0, db: Session = Depends(get_db)):
    response = crud.get_vocab(chapter_id, next_id, db)
    return response


@router.post("/post_vocab", status_code=status.HTTP_200_OK)
async def post_vocab(body: VocabMeaningPost, db: Session = Depends(get_db)):
    response = crud.post_vocab(body, db)
    return response


@router.put("/put_vocab", status_code=status.HTTP_200_OK)
async def put_vocab(body: VocabMeaningPut, db: Session = Depends(get_db)):
    response = crud.put_vocab(body, db)
    return response


@router.delete("/delete_vocab", status_code=status.HTTP_200_OK)
async def delete_vocab(body: VocabMeaningDelete, db: Session = Depends(get_db)):
    response = crud.delete_vocab(body, db)
    return response