from os import stat
from sqlalchemy.sql.expression import null, update
from starlette.status import HTTP_400_BAD_REQUEST
from schemas.vocab_chapter import VocabChapterPost, VocabChapterPut, VocabChapterDelete, VocabChapterGet
import inspect
import textwrap

from typing import List
from starlette.requests import Request

from fastapi.responses import JSONResponse
from fastapi import status
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from sqlalchemy import text

from models.vocab_chapter import VocabChapterModel
from utils.log_utils import put_error

def check_db(db: Session):
    # DB接続エラー
    if db:
        response = {'message': "データベース接続が出来ました" }
        return JSONResponse(
            content=response
        )
    response = {'message': "データベース接続が失敗しました" }
    return JSONResponse(
        content=response
    )


def get_chapter(body: VocabChapterGet, db: Session):

    try:
        # データ取得SQL
        query = '''
            SELECT
                CHAPTER_ID
            FROM
                VOCAB_CHAPTER
            ORDER BY
                CHAPTER_ID
        '''

        # データ設定
        bind_params={
        }

        if body.chp_id == 1 and body.type == 'previous':
            response = {'status_code': status.HTTP_400_BAD_REQUEST , 'message': "Invalid parameter" }
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=response
            )

        if body.type == 'next':
            bind_params.update({'offset' : body.chp_id + 3})
        if body.type == 'previous':
            bind_params.update({'offset' : body.chp_id - 5})

        # 検索条件の設定
        query += '''
            OFFSET
                :offset
            LIMIT
                4
        '''

        result = db.execute(query, bind_params).fetchall()
        last_id = result[0]
        final_result = {
            'data': result,
            'page': last_id
        }
        response = {
            'result': final_result,
            'status_code': status.HTTP_200_OK,
            "message": "Searching success"
        }

        return response

    # DB接続エラー
    except OperationalError as err:
        response = {'status_code': status.HTTP_400_BAD_REQUEST , 'message': "Database connection failed" }
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=response
        )

    # DBエラー
    except Exception as err:
        response = {'status_code': status.HTTP_400_BAD_REQUEST , 'message': "Searching failed" }
        put_error(err)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=response
        )


def post_chapter(body: VocabChapterPost, db: Session):
    try:
        # データ登録SQL

        query = '''
            INSERT INTO
                VOCAB_CHAPTER
                (CREATE_DATE,
                UPDATE_DATE,
                CHAPTER_ID)
            VALUES
                (now(),
                now(),
                :chapter_id)
        '''

        # データ設定
        bind_params = {
            "chapter_id": body.chapter_id
        }

        result = db.execute(query, bind_params)

    # DB接続エラー
    except OperationalError as err:
        response = {'status_code': status.HTTP_400_BAD_REQUEST , 'message': "Database connection failed" }
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=response
        )

    # DBエラー
    except Exception as err:
        db.rollback()
        response = {'data': None, 'status_code': status.HTTP_400_BAD_REQUEST, 'message': "Chapter registration failed" }
        put_error(err)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=response
        )

    db.commit()
    response = {'data': None, 'status_code': status.HTTP_200_OK , 'message': "Chapter registration success" }
    return JSONResponse(
        content=response
    )


def put_chapter(body: VocabChapterPut, db: Session):
    try:
        # データ更新SQL
        query = '''
            UPDATE
                VOCAB_CHAPTER
            SET
                UPDATE_DATE = now(),
                CHAPTER_ID = :chapter_id
        '''

        # データ設定
        bind_params = {
            "id": body.id,
            "chapter_id": body.chapter_id
        }

        query += " WHERE ID = :id"

        result = db.execute(query, bind_params)

    # DB接続エラー
    except OperationalError as err:
        response = {'status_code': status.HTTP_400_BAD_REQUEST , 'message': "Database connection failed" }
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=response
        )

    # DBエラー
    except Exception as err:
        db.rollback()
        response = {'data' : None, 'status_code': status.HTTP_400_BAD_REQUEST , 'message': "Chapter update failed" }
        put_error(err)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=response
        )

    db.commit()
    response = {'data': None, 'status_code': status.HTTP_200_OK , 'message': "Chapter update success" }
    return JSONResponse(
        content=response
    )


def delete_chapter(body: VocabChapterDelete, db: Session):
    try:
        # データ削除SQL
        query = '''
            DELETE FROM
                VOCAB_CHAPTER
            WHERE
                CHAPTER_ID = :chapter_id
        '''

        # データ設定
        bind_params = {
            "chapter_id": body.chapter_id
        }

        result = db.execute(query, bind_params)

    # DB接続エラー
    except OperationalError as err:
        response = {'status_code': status.HTTP_400_BAD_REQUEST , 'message': "Database connection failed" }
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=response
        )

    # DBエラー
    except Exception as err:
        db.rollback()
        response = {'data': None, 'status_code': status.HTTP_400_BAD_REQUEST, 'message': "Chapter deletion failed" }
        put_error(err)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=response
        )

    db.commit()
    response = {'data': None, 'status_code': status.HTTP_200_OK , 'message': "Chapter deletion success" }
    return JSONResponse(
        content=response
    )

