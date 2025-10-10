from get_csv import get_covid
from check_covid_data import check_covid
from wrangling_covid import clean_covid
from import_data import import_database

if __name__ == '__main__':
    get_covid()
    check_covid()
    clean_covid()
    import_database()