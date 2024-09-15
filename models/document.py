from sqlalchemy import Date, Integer, String, Text, ARRAY
from sqlalchemy.orm import DeclarativeBase, mapped_column

class Base(DeclarativeBase):
    pass


class Document(Base):
    __tablename__ = 'document_table'

    id = mapped_column(Integer, primary_key=True)
    text = mapped_column(String)
    created_date = mapped_column(Date)
    rubrics = mapped_column(ARRAY(Text))
