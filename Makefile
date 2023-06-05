PORT ?= 8000

dev:
	poetry run flask --app my_site.example --debug run

start:
	poetry run gunicorn --workers=4 --bind=0.0.0.0:$(PORT) my_site.example:app