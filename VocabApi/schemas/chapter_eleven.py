from typing import Optional
from pydantic import BaseModel, constr, root_validator


# bodyパラメータ定義(PUT)
class ChapterElevenPut(BaseModel):
    id: int
    kanji: Optional[str] = "null"
    hiragana: Optional[str] = "null"
    meaning: Optional[str] = "null"


# bodyパラメータ定義(POST)
class ChapterElevenPost(BaseModel):
    kanji: Optional[str] = None
    hiragana: str
    meaning: str


# bodyパラメータ定義(DELETE)
class ChapterElevenDelete(BaseModel):
    id: int
