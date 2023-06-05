dev:
	poetry run flask --app example --debug run

start:
	poetry run gunicorn --workers=4 --bind=0.0.0.0:5000 my_site.example:app