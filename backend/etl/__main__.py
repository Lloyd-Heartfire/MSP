import sys
import os
import django

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))  # /app/etl
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # /app

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "msp_backend.settings")
django.setup()


from etl.get_csv_covid import get_covid
from etl.check_file_covid  import check_covid
from etl.wrangling_covid import clean_covid

from etl.get_csv_loc import get_csv_from_github, get_who_regions_from_owid
from etl.check_file_loc import check_and_update_locations_referentiel, check_and_update_who_regions_referentiel
from etl.wrangling_loc import clean_locations, clean_who_regions, who_region_mapping

from etl.import_data import import_database

if __name__ == '__main__':
    # Get covid_data
    get_covid()
    check_covid()
    clean_covid()

    # Get locations_data
    get_csv_from_github()
    get_who_regions_from_owid()
    check_and_update_locations_referentiel()
    check_and_update_who_regions_referentiel()
    locations=clean_locations()
    who_regions=clean_who_regions()
    who_region_mapping(locations, who_regions)

    # import to database
    import_database()