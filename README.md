# Тестовое задание

Проект работает на Python 3.8.10 

Для запуска проекта нужно установить модули из requirements.txt:

```python
pip install -r requirements.txt
```

Также, нужно создать базу данных на `postgresql`, по умолчанию база данных называется `journal`.

Все данные подключения к базе делаются в файле `./backend/.env`

Там же прописаны: ключ авторизации для google-sheets, имя sheets файла, телеграмм токен

Для запуска основного скрипта нужно запустить файл:

```sh
python3 ./backend/google_sheets_proc.py
```

Для запуска веб-части нужно запустить основной модуль:

```sh
python3 ./backend/main.py
```

Сообщения которые отправляются в телеграмм, отправляются в канал https://t.me/+3Xah1Rf7k002ZGM6

Изменить это можно в файле `./backend/.env` (TELEGRAM_CHAT_ID)
