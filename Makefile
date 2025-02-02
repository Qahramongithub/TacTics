create_app:
	python3 manage.py startapp apps

run:
	python3 manage.py runserver localhost:8000

mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

create_user:
	python3 manage.py createsuperuser

lang:
	django-admin makemessages -l uz
	django-admin makemessages -l en
	django-admin makemessages -l ru


com:
	django-admin compilemessages
