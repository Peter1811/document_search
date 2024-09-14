# Поисковик по текстам документов
## Гайд по поднятию сервиса
Запуск описывается для операционной системы Windows 10 (cmd)
1) Выполнить установку необходимых библиотек в виртуальное окружение из файла `requirements.txt`
```
python -m venv venv
venv/Scripts/activate
pip install -r requirements.txt
```

2) Создать в родительской директории два файла: .env_database и .env_services со следующим содержимым
## .env_database
```
USERNAME=
PASSWORD=
HOST=
PORT=
DATABASE=
```

##.env_services
```
ELASTICSEARCH_HOST=localhost
ELASTICSEARCH_PORT=9200
RUN_HOST=localhost
RUN_PORT=8000
```
Подставить необходимые значения - БД (используется postgresql), elasticsearch, непосредственный запуск сервиса

3) Поднять кластер elasticsearch (предварительно необходимо установить его, скачав с официального сайта)
```
es/bin/elasticsearch
```
4) Запустить скрипт для заполнения базы данных `db_filling.py` (предварительно необходимо добавить данные в файл `posts.csv` - содержимое, дату создания и массив рубрик)
```
python db_filling.py
```
5) Запустить сервис
```
python main.py
```
6) Открыть в браузере выведенный в командной строке адрес, добавить в конец адресной строки `/docs` - там можно выполнять тестирование сервиса.
