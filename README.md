# Найпростіший Flask-додаток

Цей проєкт підготовлений для лабораторної роботи №1.

## Локальний запуск

1. Створіть та активуйте віртуальне середовище:

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux / macOS:
source venv/bin/activate
```

2. Встановіть залежності:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

3. Запустіть Flask-додаток:

```bash
flask run
```

або

```bash
python app.py
```

## Деплой на Render

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
gunicorn app:app
```
