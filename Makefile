dev:
	poetry run flask --app example --debug run

start:
	poetry run gunicorn --workers=4 --bind=0.0.0.0:8000 example:app