from typing import Optional
from pydantic import BaseModel, constr, root_validator


# bodyパラメータ定義(PUT)
class VocabChapterGet(BaseModel):
    chp_id: int
    type: str

# bodyパラメータ定義(PUT)
class VocabChapterPut(BaseModel):
    id: int
    chapter_id: int


# bodyパラメータ定義(POST)
class VocabChapterPost(BaseModel):
    chapter_id: int


# bodyパラメータ定義(DELETE)
class VocabChapterDelete(BaseModel):
    chapter_id: int
