from os import stat
from sqlalchemy.sql.expression import null, update
from starlette.status import HTTP_400_BAD_REQUEST
from schemas.vocab_meaning import VocabMeaningPost, VocabMeaningPut, VocabMeaningDelete
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

from models.vocab_meaning import VocabMeningModel
from utils.log_utils import put_error


def get_vocab(chapter_id, next_id, db: Session):
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
                VOCAB_MEANING
        '''
        # データ設定
        bind_params={
            "chapter_id": chapter_id,
            "next_id": next_id
        }

        query += '''
            WHERE
                CHAPTER_ID = :chapter_id
            ORDER BY
                ID
            OFFSET
                CASE WHEN :next_id = 0 THEN 0
                    ELSE
                        (SELECT COUNT(*) FROM VOCAB_MEANING WHERE ID < :next_id)
                    END
            LIMIT
                10
            '''

        result = db.execute(query, bind_params).fetchall()

        next = result[9]['id']

        next_params = {
            "next": next
        }

        next_query = '''
            SELECT
                ID
            FROM
                VOCAB_MEANING
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


def post_vocab(body: VocabMeaningPost, db: Session):
    try:
        # データ登録SQL

        query = '''
            INSERT INTO
                VOCAB_MEANING
                (CREATE_DATE,
                UPDATE_DATE,
                CHAPTER_ID,
                KANJI,
                HIRAGANA,
                MEANING)
            VALUES
                (now(),
                now(),
                :chapter_id,
                :kanji,
                :hiragana,
                :meaning)
        '''

        # データ設定
        bind_params = {
            "chapter_id": body.chapter_id,
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


def put_vocab(body: VocabMeaningPut, db: Session):

    update_params = []

    try:
        # データ更新SQL
        query = '''
            UPDATE
                VOCAB_MEANING
            SET
                UPDATE_DATE = now()
        '''

        # データ設定
        bind_params = {
            "chapter_id": body.chapter_id,
            "kanji": body.kanji
        }

        for parms in body:
            key, value = parms
            if key == "kanji":
                continue
            if key == "hiragana" and value == "":
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
                CHAPTER_ID = :chapter_id
            AND
                KANJI = :kanji
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


def delete_vocab(body: VocabMeaningDelete, db: Session):
    try:
        # データ削除SQL
        query = '''
            DELETE FROM
                VOCAB_MEANING
            WHERE
                CHAPTER_ID = :chapter_id
            AND
                KANJI = :kanji
        '''

        # データ設定
        bind_params = {
            "chapter_id": body.chapter_id,
            "kanji": body.kanji
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

