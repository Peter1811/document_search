import os
import uvicorn

from dotenv import load_dotenv
from elasticsearch import Elasticsearch, NotFoundError
from fastapi import Body, Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import session
from models import Document

load_dotenv('.env_services', override=True)
es_host = os.getenv('ELASTICSEARCH_HOST')
es_port = os.getenv('ELASTICSEARCH_PORT')
run_host = os.getenv('RUN_HOST')
run_port = os.getenv('RUN_PORT')

app = FastAPI()

def get_db():
    with session() as db:
        yield db


@app.post('/search/')
def text_search(text: str = Body(...), db: Session = Depends(get_db)):

    client = Elasticsearch(f'http://{es_host}:{es_port}')
    try:
        response = client.search(
            index='document_index',
            query={
                'match': {
                    'text': text
                }
            },
            size=20
        )

        documents = response['hits']['hits']
        documents_ids = [document['_source']['id'] for document in documents]
        
        res = select(Document).where(Document.id.in_(documents_ids)).order_by(Document.created_date)
        results = db.execute(res).scalars().all()

        return list(results)
    
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.delete('/delete/{id:int}')
def delete_document(id: int, db: Session = Depends(get_db)):
    try:
        document = db.query(Document).filter(Document.id == id).first()
        if not document:
            raise HTTPException(status_code=404, detail=f'Document with id {id} was not found in database')
        
        client = Elasticsearch(f'http://{es_host}:{es_port}')
        client.delete(index='document_index', id=id)

        db.delete(document)
        db.commit()

        return {'deleted document with id': id}
    
    except NotFoundError:
        return JSONResponse(content={'detail': 'Document was not found in index'})

    except HTTPException as exception:
        if exception.status_code == 404:
            return JSONResponse(status_code=404, content={'detail': 'Document was not found'})

    except Exception as exc:
        db.rollback()
        return JSONResponse(content={'detail': 'Internal error: ' + str(exc)})


if __name__ == '__main__':
    uvicorn.run('main:app', host=run_host, port=int(run_port), reload=True)
