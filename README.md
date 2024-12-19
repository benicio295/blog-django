# Blog

This is Blog project created with Django

## Requirements
* Python 3.13 or higher
* Docker with docker-compose last version

## Getting Started

1- First setting environment variables. Then, run docker compose

```bash
docker compose up -d
```

2- Create a virtual environment and activate it

```bash
python -m venv venv
```

```bash
source venv/bin/activate
```

3- Install all requirements projects and start the server.

```bash
pip install -r requirements.txt
```

```bash
python manage.py runserver
```
4- Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) with your browser to see the result.
To access admin page, go to [http://127.0.0.1:8000/adminpage](http://127.0.0.1:8000/adminpage)
