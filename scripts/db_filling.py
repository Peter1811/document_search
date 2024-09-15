# скрипт запускается перед запуском сервера, для заполнения БД

import asyncio
import datetime
import os
import pandas as pd
import sys

from elasticsearch import AsyncElasticsearch
from dotenv import load_dotenv, find_dotenv

sys.path.append(os.getcwd())
from db.database import session
from models.document import Document

path = find_dotenv(filename='.env_services')
load_dotenv(path)
es_host = os.getenv('ELASTICSEARCH_HOST')
es_port = os.getenv('ELASTICSEARCH_PORT')

async def main():
    async with session() as db:
        posts = pd.read_csv('posts.csv')
        for item in posts.values:
            item_dict = dict(zip(['Text', 'Date', 'Rubrics'], item))
            
            year, month, day = map(int, item_dict['Date'].split()[0].split('-'))
            new_doc = Document(
                text=item_dict['Text'],
                created_date=datetime.date(year=year, month=month, day=day),
                rubrics=eval(item_dict['Rubrics'])
            )

            db.add(new_doc)
            await db.commit()
            await db.refresh(new_doc)

            document_index = {
                'id': new_doc.id,
                'text': new_doc.text
            }

            async with AsyncElasticsearch(f'http://{es_host}:{es_port}') as client:
                await client.index(index='document_index', id=new_doc.id, document=document_index)

asyncio.run(main())
