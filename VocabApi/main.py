import uvicorn
from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, sessionmaker
from starlette.requests import Request
from starlette.exceptions import HTTPException as StarletteHTTPException
from environs import Env

from utils.log_utils import put_error
from utils.message_handling import get_messages


from db import engine, session
from routers import (
    vocab_chapter,
    vocab_meaning,
    chapter_one,
    chapter_two,
    chapter_three,
    chapter_four,
    chapter_five,
    chapter_six,
    chapter_seven,
    chapter_eight,
    chapter_nine,
    chapter_ten,
    chapter_eleven,
    chapter_twelve,
    chapter_thirteen,
    chapter_fourteen,
    chapter_fifteen,
    chapter_sixteen,
    chapter_seventeen,
    chapter_eighteen,
    chapter_nineteen,
    chapter_twenty
)

env = Env()
env.read_env()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

#Validation Message Override
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return get_messages(request, exc)


# router登録
app.include_router(vocab_chapter.router)
app.include_router(vocab_meaning.router)
app.include_router(chapter_one.router)
app.include_router(chapter_two.router)
app.include_router(chapter_three.router)
app.include_router(chapter_four.router)
app.include_router(chapter_five.router)
app.include_router(chapter_six.router)
app.include_router(chapter_seven.router)
app.include_router(chapter_eight.router)
app.include_router(chapter_nine.router)
app.include_router(chapter_ten.router)
app.include_router(chapter_eleven.router)
app.include_router(chapter_twelve.router)
app.include_router(chapter_thirteen.router)
app.include_router(chapter_fourteen.router)
app.include_router(chapter_fifteen.router)
app.include_router(chapter_sixteen.router)
app.include_router(chapter_seventeen.router)
app.include_router(chapter_eighteen.router)
app.include_router(chapter_nineteen.router)
app.include_router(chapter_twenty.router)



# リクエストの都度呼ばれるミドルウェア（DB接続用セッションインスタンス作成）
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = session
    response = await call_next(request)
    request.state.db.close()
    return response


# サーバ起動
if __name__ == '__main__':
    # log_config = uvicorn.config.LOGGING_CONFIG
    # log_config["formatters"]["access"]["fmt"] = '%(asctime)s [%(levelname)s] %(client_addr)s - "%(request_line)s" %(status_code)s'
    # log_config["formatters"]["default"]["fmt"] = "%(asctime)s [%(levelname)s] %(message)s"

    uvicorn.run("main:app",
                host=env("SVR_HOST"),
                port=int(env("SVR_PORT")),
                reload=env("SVR_RELOAD")
                # access_log=env("SVR_ACCESS_LOG"),
                # log_level=env("SVR_LEVEL"),
                # log_config=log_config
                )
