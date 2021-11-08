from os import stat
from sqlalchemy.sql.expression import null, update
from starlette.status import HTTP_400_BAD_REQUEST
from schemas.chapter_twenty import ChapterTwentyPost, ChapterTwentyPut, ChapterTwentyDelete
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

from models.chapter_twenty import ChapterTwentyModel
from utils.log_utils import put_error


def get_chapter_twenty(next_id, db: Session):
    try:
        # データ取得SQL
        query = '''
            SELECT
                ID,
                CHAPTER_ID,
                KANJI,
                HIRAGANA,
                MEANING
            FROM
                CHAPTER_TWENTY
        '''
        # データ設定
        bind_params={
            "next_id": next_id
        }

        query += '''
            ORDER BY
                ID
            OFFSET
                CASE WHEN :next_id = 0 THEN 0
                    ELSE
                        (SELECT COUNT(*) FROM CHAPTER_TWENTY WHERE ID < :next_id)
                    END
            LIMIT
                10
            '''

        result = db.execute(query, bind_params).fetchall()

        last_index = len(result)-1

        next = result[last_index]['id']

        next_params = {
            "next": next
        }

        next_query = '''
            SELECT
                ID
            FROM
                CHAPTER_TWENTY
            WHERE
                ID > :next
            ORDER BY
                ID
            LIMIT
                1
        '''

        next_id_q = db.execute(next_query, next_params).fetchall()

        if len(next_id_q) == 0:
            pagination = {'next_id': None}
        else:
            pagination = {'next_id': next_id_q[0]['id']}

        final_result = {'data': result, 'pagination': pagination}
        response = {'result': final_result, 'status_code': status.HTTP_200_OK, "message": "Searching success"}

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


def post_chapter_twenty(body: ChapterTwentyPost, db: Session):
    try:
        # データ登録SQL

        query = '''
            INSERT INTO
                CHAPTER_TWENTY
                (CREATE_DATE,
                UPDATE_DATE,
                CHAPTER_ID,
                KANJI,
                HIRAGANA,
                MEANING)
            VALUES
                (now(),
                now(),
                20,
                :kanji,
                :hiragana,
                :meaning)
        '''

        # データ設定
        bind_params = {
            "kanji": body.kanji,
            "hiragana": body.hiragana,
            "meaning": body.meaning
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
        response = {'data': None, 'status_code': status.HTTP_400_BAD_REQUEST, 'message': "Vocabulary registration failed" }
        put_error(err)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=response
        )

    db.commit()
    response = {'data': None, 'status_code': status.HTTP_200_OK , 'message': "Vocabulary registration success" }
    return JSONResponse(
        content=response
    )


def put_chapter_twenty(body: ChapterTwentyPut, db: Session):

    update_params = []

    try:
        # データ更新SQL
        query = '''
            UPDATE
                CHAPTER_TWENTY
            SET
                UPDATE_DATE = now()
        '''

        # データ設定
        bind_params = {
            "id": body.id
        }

        for parms in body:
            key, value = parms
            if key == "id":
                continue
            if key == "kanji" and value == "":
                update_params.append(" " + key.capitalize() + " = :" + key + " ")
                bind_params.update({key : None})
            elif key == "hiragana" and value == "":
                update_params.append(" " + key.capitalize() + " = :" + key + " ")
                bind_params.update({key : None})
            elif key == "meaning" and value == "":
                update_params.append(" " + key.capitalize() + " = :" + key + " ")
                bind_params.update({key : None})
            elif value != "null":
                update_params.append(" " + key.capitalize() + " = :" + key + " ")
                bind_params.update({key : value})

        # データ更新設定チェック
        if len(update_params) != 0:
            query += "," + ",\n".join(update_params)

        # 検索条件の設定
        query += '''
            WHERE
                ID = :id
        '''

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
        response = {'data' : None, 'status_code': status.HTTP_400_BAD_REQUEST , 'message': "Vocabulary update failed" }
        put_error(err)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=response
        )

    db.commit()
    response = {'data': None, 'status_code': status.HTTP_200_OK , 'message': "Vocabulary update success" }
    return JSONResponse(
        content=response
    )


def delete_chapter_twenty(body: ChapterTwentyDelete, db: Session):
    try:
        # データ削除SQL
        query = '''
            DELETE FROM
                CHAPTER_TWENTY
            WHERE
                ID = :id
        '''

        # データ設定
        bind_params = {
            "id": body.id
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
        response = {'data': None, 'status_code': status.HTTP_400_BAD_REQUEST, 'message': "Vocabulary deletion failed" }
        put_error(err)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=response
        )

    db.commit()
    response = {'data': None, 'status_code': status.HTTP_200_OK , 'message': "Vocabulary deletion success" }
    return JSONResponse(
        content=response
    )

