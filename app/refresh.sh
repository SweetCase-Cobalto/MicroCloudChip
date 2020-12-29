rm -rf app/migrations
rm db.sqlite3

python manage.py makemigrations
python manage.py migrate
python manage.py makemigrations app
python manage.py migrate app
