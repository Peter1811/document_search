import asyncio
import os
import uvicorn

from dotenv import load_dotenv
from elasticsearch import NotFoundError, AsyncElasticsearch
from fastapi import Body, Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from models.document import Document

load_dotenv('.env_services', override=True)
es_host = os.getenv('ELASTICSEARCH_HOST')
es_port = os.getenv('ELASTICSEARCH_PORT')
run_host = os.getenv('RUN_HOST')
run_port = os.getenv('RUN_PORT')

app = FastAPI()


@app.post('/search/')
async def text_search(text: str = Body(...), db: AsyncSession = Depends(get_db)):
    try:
        async with AsyncElasticsearch(f'http://{es_host}:{es_port}') as client:
            response = await client.search(
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
        
        query = select(Document).where(Document.id.in_(documents_ids)).order_by(Document.created_date)
        query_result = await db.execute(query)
        result = query_result.scalars().all()

        return list(result)
    
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.delete('/delete/{id:int}')
async def delete_document(id: int, db: AsyncSession = Depends(get_db)):
    try:
        query = select(Document).where(Document.id == id)
        query_result = await db.execute(query)
        document = query_result.scalar()
        
        if not document:
            raise HTTPException(status_code=404)
        
        async with AsyncElasticsearch(f'http://{es_host}:{es_port}') as client:
            await client.delete(index='document_index', id=id)

        await db.delete(document)
        await db.commit()

        return {'deleted document with id': id}
    
    except NotFoundError:
        return JSONResponse(content={'detail': 'Document was not found in index'})

    except HTTPException as exception:
        if exception.status_code == 404:
            return JSONResponse(status_code=404, content={'detail': 'Document was not found'})

    except Exception as exc:
        await db.rollback()
        return JSONResponse(content={'detail': 'Internal error: ' + str(exc)})


if __name__ == '__main__':
    uvicorn.run('main:app', host=run_host, port=int(run_port), reload=True)
