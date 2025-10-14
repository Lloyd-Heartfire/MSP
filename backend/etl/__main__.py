from get_csv import get_covid
from check_covid_data import check_covid
from wrangling_covid import clean_covid
from import_data import import_database

from et_csv_loc import get_csv_from_github, get_who_regions_from_owid
from check_file_loc import check_and_update_locations_referentiel, check_and_update_who_regions_referentiel
from clean_file_loc import clean_locations, clean_who_regions, who_region_mapping
from clean_geocode import clean_geocode

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
    clean_locations()
    clean_who_regions()
    who_region_mapping()
    clean_geocode()

    import_database()