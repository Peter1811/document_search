import datetime

from fastapi import Body, Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from database import session
from models import Document
from schemas import DocumentCreate

app = FastAPI()

def get_db():
    with session() as sess:
        yield sess


@app.get('/')
def main():
    return {'Base': 'page'}

@app.post('/create/')
def create_document(document: DocumentCreate, db: Session = Depends(get_db)):
    curr_date = datetime.date.today()
    new_document = Document(
        text=document.text,
        created_data=curr_date
    )
    try:
        db.add(new_document)
        db.commit()
        db.refresh(new_document)
        return {'text': document.text}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f'Error: {e}')


@app.post('/search/')
def text_search(text: str = Body(...), db: Session = Depends(get_db)):
    return {'text': text}

@app.delete('/delete/')
def delete_document(id: int, db: Session = Depends(get_db)):
    try:
        document = db.query(Document).filter(Document.id == id).first()
        if not document:
            raise HTTPException(status_code=404, detail=f'Document with id {id} was not found in database')
        
        db.delete(document)
        db.commit()

        return {'deleted document with id': id}
    
    except HTTPException as exception:
        if exception.status_code == 404:
            return JSONResponse(status_code=404, content={'detail': 'Document was not found'})

    except Exception as e:
        db.rollback()
        return JSONResponse(content={'detail': 'Internal error'})
