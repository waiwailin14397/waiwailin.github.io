from enum import unique
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import *
from sqlalchemy.sql.sqltypes import Integer

from db import Base, engine


class VocabChapterModel(Base):
    __tablename__ = "vocab_chapter"
    id = Column("id", INTEGER, primary_key=True)
    chapterId = Column("chapter_id", INTEGER, nullable=False, unique=True)
    create_date = Column("create_date", TIMESTAMP(timezone=False), nullable=False)
    update_date = Column("update_date", TIMESTAMP(timezone=False), nullable=False)

Base.metadata.create_all(bind=engine)
