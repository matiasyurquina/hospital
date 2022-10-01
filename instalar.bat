psql -U postgres -f create.sql
pip install Django==4.0.4
pip install psycopg2
python manage.py migrate
python manage.py loaddata osociales.json
python manage.py loaddata localidades.json
python manage.py loaddata paises.json

echo presione una tecla para continuar
pause
