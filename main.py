from sqlalchemy import select

from fastapi import Body, Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import session
from models import Document

app = FastAPI()

def get_db():
    with session() as db:
        yield db


@app.post('/search/')
def text_search(text: str = Body(...), db: Session = Depends(get_db)):
    try:
        request = select(Document)
        documents = list(db.execute(request).scalars())
        if len(documents) == 0:
            return JSONResponse(content={'detail': 'No items in table'})
        
        results = {}
        for document in documents:
            results[document.id] = [document.created_data, document.text, [rubric.text for rubric in document.rubrics]]
        sorted_results = dict(sorted(results.items(), key=lambda x: x[1][0]))
        return {'res': list(sorted_results.items())}
    except Exception as exc:
        return JSONResponse(content={'detail': str(exc)})


@app.delete('/delete/{id:int}')
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

    except Exception as exc:
        db.rollback()
        return JSONResponse(content={'detail': 'Internal error: ' + str(exc)})
