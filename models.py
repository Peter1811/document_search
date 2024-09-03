from sqlalchemy import Date, Integer, String, ForeignKey, Table, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, mapped_column

Base = declarative_base()

DocumentRubric = Table('document_rubric_table',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('document_id', Integer, ForeignKey('document_table.id')),
    Column('rubric_id', Integer, ForeignKey('rubric_table.id'))
)

class Document(Base):
    __tablename__ = 'document_table'

    id = mapped_column(Integer, primary_key=True, index=True)
    text = mapped_column(String, index=True)
    created_data = mapped_column(Date)

    rubrics = relationship('Rubric', secondary='document_rubric_table', back_populates='document')


class Rubric(Base):
    __tablename__ = 'rubric_table'

    id = mapped_column(Integer, primary_key=True)
    text = mapped_column(String)

    document = relationship('Document',secondary='document_rubric_table', back_populates='rubrics')
