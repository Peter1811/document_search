# скрипт запускается перед запуском сервера, для заполнения БД

import random

from sqlalchemy import select

from database import session
from models import Document, Rubric
from utils import generate_rubric_name, generate_random_date, generate_random_text

rubrics = generate_rubric_name(15)

rubric_objects = []

with session() as db:

    for rubric in rubrics:
        new_rubric = Rubric(
            text=rubric
        )

        rubric_objects.append(new_rubric)
        db.add(new_rubric)
        db.commit()
        db.refresh(new_rubric)

    for i in range(10):
        new_document = Document(
            text=generate_random_text(50),
            created_data=generate_random_date()
        )

        new_document.rubrics = random.sample(rubric_objects, 2)

        db.add(new_document)
        db.commit()
        db.refresh(new_document)

