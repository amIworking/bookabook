# bookabook

# Local Run
- create venv with Python 3.12
- install requirements: `pip install requirements.txt`
- install docker
- run database locally: `docker-compose up -d db`
- apply migrations: `python backend/manage.py migrate`
- run server: `python backend/manage.py runserver`
- create superuser: `python backend/manage.py createsuperuser`
- go http://127.0.0.1:8000/admin

# First Fast Run
- install docker
- download docker images: `docker-compose build`
- run database locally: `docker-compose up -d db`
- apply migrations: `docker-compose run --rm bookabook-backend sh -c "python manage.py migrate"`
- create superuser: `docker-compose run --rm bookabook-backend sh -c "python manage.py createsuperuser"`
- run server: `docker-compose up`
- go http://127.0.0.1:8000/admin

# Next Fast Run
- run server: `docker-compose up`
- go http://127.0.0.1:8000/admin