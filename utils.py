import datetime
import random

from string import ascii_lowercase


def generate_random_text(n):
    return ''.join([random.choice(ascii_lowercase) for _ in range(n)])


def generate_rubric_name(n):
    rubrics = []
    for i in range(n):
        name = generate_random_text(10)
        rubrics.append(name)

    return rubrics


def generate_random_date():
    day = random.randrange(1, 31)
    month = random.randrange(1, 13)
    year = random.randrange(2000, 2050)

    date = datetime.date(year, month, day)

    return date
