dev:
	poetry run flask --app example --debug run

start:
	poetry run gunicorn --workers=4 --bind=127.0.0.1:5000 my_site.example:app