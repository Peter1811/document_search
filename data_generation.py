# скрипт запускается перед запуском сервера, для заполнения БД

import os
import pandas as pd

from elasticsearch import Elasticsearch
from dotenv import load_dotenv

from database import session
from models import Document

load_dotenv()
es_host = os.getenv('ELASTICSEARCH_HOST')
es_port = os.getenv('ELASTICSEARCH_PORT')
client = Elasticsearch(f'http://{es_host}:{es_port}')

with session() as db:
    posts = pd.read_csv('posts.csv')
    for item in posts.values:
        item_dict = dict(zip(['Text', 'Date', 'Rubrics'], item))
        new_doc = Document(
            text=item_dict['Text'],
            created_date=item_dict['Date'],
            rubrics=eval(item_dict['Rubrics'])
        )

        db.add(new_doc)
        db.commit()
        db.refresh(new_doc)

        document_index = {
            'id': new_doc.id,
            'text': new_doc.text
        }

        client.index(index='document_index', id=new_doc.id, document=document_index)
