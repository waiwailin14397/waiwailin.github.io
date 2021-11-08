from typing import Optional
from pydantic import BaseModel, constr, root_validator


# bodyパラメータ定義(PUT)
class VocabMeaningPut(BaseModel):
    chapter_id: int
    kanji: str
    hiragana: Optional[str] = "null"
    meaning: Optional[str] = "null"


# bodyパラメータ定義(POST)
class VocabMeaningPost(BaseModel):
    chapter_id: int
    kanji: Optional[str] = None
    hiragana: str
    meaning: str


# bodyパラメータ定義(DELETE)
class VocabMeaningDelete(BaseModel):
    chapter_id: int
    kanji: str
