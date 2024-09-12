# скрипт запускается перед запуском сервера, для заполнения БД

import pandas as pd

from database import session
from models import Document

from elasticsearch import Elasticsearch

client = Elasticsearch('http://localhost:9200')

with session() as db:

    posts = pd.read_csv('posts.csv')

    for item in posts.values:
        item_dict = dict(zip(['Text', 'Date', 'Rubrics'], item))

        print(item_dict['Rubrics'])
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
