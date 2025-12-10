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

## Лабораторна робота №2 — Маршрутизація та шаблони

У цій лабораторній роботі проєкт доповнено:

- додано маршрути `/resume` та `/contacts`;
- створено шаблони Jinja2 з наслідуванням (`base.html`, `resume.html`, `contacts.html`);
- винесено спільні частини в окремі include-файли (`includes/navbar.html`, `includes/footer.html`);
- підключено Bootstrap через CDN та власні стилі `static/css/styles.css`;
- додано статичне зображення `static/images/profile.svg` та підключено його через `url_for`;
- створено просту форму зворотного зв'язку на сторінці контактів (форма-заглушка без реальної відправки).

### Запуск проєкту

1. Створити та активувати віртуальне середовище (як у ЛР №1).
2. Встановити залежності:

   ```bash
   pip install -r requirements.txt
   ```

3. Запустити застосунок:

   ```bash
   flask run
   ```

   або

   ```bash
   python app.py
   ```

4. Перейти в браузері на:

   - `http://127.0.0.1:5000/` — буде автоматичне перенаправлення на `/resume`;
   - `http://127.0.0.1:5000/resume` — сторінка резюме;
   - `http://127.0.0.1:5000/contacts` — сторінка контактів з формою.
