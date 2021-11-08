from enum import unique
from sqlalchemy import Column, Index
from sqlalchemy.dialects.postgresql import *
from sqlalchemy.sql.sqltypes import Integer

from db import Base, engine


class ChapterFourModel(Base):
    __tablename__ = "chapter_four"
    id = Column("id", INTEGER, primary_key=True)
    chapterId = Column("chapter_id", INTEGER, nullable=False)
    kanji = Column("kanji", VARCHAR(255), unique=True)
    hiragana = Column("hiragana", VARCHAR(255), nullable=False)
    meaning = Column("meaning", VARCHAR(255), nullable=False)
    create_date = Column("create_date", TIMESTAMP(timezone=False), nullable=False)
    update_date = Column("update_date", TIMESTAMP(timezone=False), nullable=False)

    __table_args__ = (Index('chapter_four_idx01', kanji),)

Base.metadata.create_all(bind=engine)
