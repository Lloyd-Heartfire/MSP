from django.utils import timezone
from msp_backend.models import DataSource, Pandemic, DataFile, Location, PandemicData
import json
import pandas as pd

# Create data for covid_19 in pandemic, source and file table 
def import_database():
    pandemic = Pandemic.objects.create(
            pandemic_name='Covid-19',
            start_date='2019-12-01',
            pandemic_description='Global pandemic caused by SARS-CoV-2',
            pathogene_agent='virus',
            who_classification='pandemic',
            created_at=timezone.now(),
            updated_at=timezone.now(),
    )

    source = DataSource.objects.create(
            source_name='Johns Hopkins University',
            source_url='https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data',
            source_type='Official',
            created_at=timezone.now(),
            updated_at=timezone.now(),
    )

    file = DataFile.objects.create(
            file_name='full_clean_covid_19.json',
            user_id=1,
            source_id=source.id,
            upload_date=timezone.now(),
    )

    # Adding locations and pandemics_data
    print("Import locations")
    with open("/app/etl/locations/full_clean_locations.json") as f:
        data_list = json.load(f)
        batch = [Location(
            country=d.get("country_region"),
            province_state=d.get("province_state") or None,
            city=d.get("city") or None,
            iso_code=d.get("iso3") or None,
            latitude=d.get("latitude"),
            longitude=d.get("longitude"),
            # Convert into an integer if it exists
            population=int(float(d.get("population"))) if d.get("population") else None,
            who_region=d.get("who_region") or None,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        ) for d in data_list]
        # Bulk_create allows us to make a single SQL request for our entire batch instead of one per object
        Location.objects.bulk_create(batch, batch_size=1000)

    print("Locations inserted")

    print("Inserting covid data now")

    # -----------------------------
    # Load all locations into memory to link it with covid_19 json
    # -----------------------------

    print("Loading location data")

    locations_map = {
        (loc.country, loc.province_state, loc.city): loc
        for loc in Location.objects.all()
    }
    print(f"{len(locations_map)} locations inserted.")

    print("Loading covid_19 data")
    # Preparing batch
    batch = []
    missing_locations = []
    now = timezone.now()

    with open("/app/etl/covid/full_clean_covid_19.json") as f:
        data_list = json.load(f)
    print(f"{len(data_list)} lines in the JSON.")

    # Keeping idx as a value to keep track of the number of lines processed and putting it to 1 at the beginning
    for idx, data in enumerate(data_list, 1):
        country = data.get('country')
        province = data.get('province_state') or None
        city = data.get('city') or None

        # Our location has to be the same value as the values in locations_map
        key = (country, province, city)
        location = locations_map.get(key)

        # Every 10 000 lines
        if idx % 10000 == 0:
            print(f"{idx} lines inserted on {len(data_list)}...")

        if not location:
            missing_locations.append(key)
            continue

        # Create PandemicData object that will be inserted in the next step
        batch.append(PandemicData(
            pandemic_id=pandemic.id,
            file_id=file.id,
            location=location,
            observation_date=data.get("observation_date") or None,
            # Replace by 0 if None or negative value
            new_cases = max(int(float(data.get("new_cases") or 0)), 0),
            new_deaths = max(int(float(data.get("new_deaths") or 0)), 0),
            total_cases = max(int(float(data.get("total_cases") or 0)), 0),
            total_deaths = max(int(float(data.get("total_deaths") or 0)), 0),
            total_recovered = max(int(float(data.get("total_recovered") or 0)), 0),
            active_cases= max(int(float(data.get("active_cases") or 0)), 0),
            created_at=now,
            updated_at=now,
        ))

        # Insert by batch until the list is less than the batch size
        if len(batch) >= 10000:
            PandemicData.objects.bulk_create(batch, batch_size=10000)
            print(f"{idx} lines treated")
            batch.clear()

    # Insert the rest in the end
    if batch:
        PandemicData.objects.bulk_create(batch, batch_size=10000)

    print(f"Finished import : {len(data_list) - len(missing_locations)} inserted lines.")
    if missing_locations:
        print(f"{len(missing_locations)} locations not found, example : {missing_locations[:5]}")
        # Convertir en DataFrame pour pouvoir sauvegarder
        df_missing = pd.DataFrame(missing_locations, columns=["country", "province_state", "city"])

        # Sauvegarde en CSV
        df_missing.to_csv("/app/etl/locations/missing_locations.csv", index=False, encoding="utf-8")

        print("Missing locations saved to /app/etl/locations/missing_locations.csv")
    