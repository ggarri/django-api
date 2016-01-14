uwsgi --processes=10 --async=100 --ugreen --socket :3031 --http :8000 --module base7test.wsgi
