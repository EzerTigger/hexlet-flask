dev:
	poetry run flask --app example --debug run

start:
	poetry run gunicorn --workers=4 --bind=127.0.0.1:8080 example:app