.PHONY: install
install:
	poetry install

.PHONY: runserver
runserver:
	poetry run py .\manage.py runserver	

.PHONY: migrate
migrate:
	poetry run py .\manage.py migrate

.PHONY: migrations
migrations:
	poetry run py .\manage.py makemigrations

.PHONY: superuser 
superuser :
	poetry run py .\manage.py createsuperuser

.PHONY: update
update: install migrate