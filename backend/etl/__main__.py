import sys
import os
import django

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))  # /app/etl
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # /app

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "msp_backend.settings")
django.setup()


from etl.get_csv import get_covid
from etl.check_covid_data import check_covid
from etl.wrangling_covid import clean_covid
# from etl.import_data import import_database

if __name__ == '__main__':
    # Get covid_data
    get_covid()
    check_covid()
    clean_covid()

    

    # import_database()