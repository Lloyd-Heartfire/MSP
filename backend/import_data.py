from django.utils import timezone
from msp_backend.models import DataSource, Pandemic, DataFile, Location, PandemicData
import json, os

# Create data for covid_19 in pandemic, source and file table 

pandemic = Pandemic.objects.create(
        pandemic_name='COVID-19',
        start_date='2019-12-01',
        pandemic_description='Pandémie mondiale causée par le SARS-CoV-2',
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
        file_name='covid_19.csv',
        user_id=1,
        source_id=source.id,
        upload_date=timezone.now(),
)

# Adding locations and pandemics_data
print("=== Import des locations ===")
with open("locations_cleaned.json") as f:
    data_list = json.load(f)
    batch = [Location(
        continent=d.get("continent"),
        country=d.get("country"),
        province_state=d.get("province_state") or None,
        admin2_usa=d.get("admin2_usa") or None,
        iso_code=d.get("iso_code") or None,
        latitude=d.get("latitude"),
        longitude=d.get("longitude"),
        population=int(float(d.get("population"))) if d.get("population") else None,
        who_region=d.get("who_region") or None,
        created_at=timezone.now(),
        updated_at=timezone.now(),
    ) for d in data_list]
    Location.objects.bulk_create(batch, batch_size=1000)

print("Locations importées !")

print("=== Import des données COVID ===")

# -----------------------------
# Configurations
# -----------------------------

BATCH_SIZE = 10000  # Number of lines inserted by batch
JSON_FILE = "covid_19.json"

# -----------------------------
# Load all locations into memory
# -----------------------------

print("Préchargement des locations existantes...")
locations_map = {
    (loc.country, loc.province_state, loc.admin2_usa): loc
    for loc in Location.objects.all()
}
print(f"{len(locations_map)} locations chargées.")

# -----------------------------
# Prepare import
# -----------------------------

batch = []
missing_locations = []

now = timezone.now()

with open(JSON_FILE) as f:
    data_list = json.load(f)
print(f"{len(data_list)} lines in the JSON.")

for idx, data in enumerate(data_list, 1):
    country = data.get('country')
    province = data.get('province_state') or None
    admin2 = data.get('admin2_usa') or None

    key = (country, province, admin2)
    location = locations_map.get(key)

    # Every 10 000 lines
    if idx % 10000 == 0:
        print(f"{idx} lines inserted on {len(data_list)}...")

    if not location:
        missing_locations.append(key)
        continue  # Skip if location doesn't exist

    # Create PandemicData object
    batch.append(PandemicData(
        pandemic_id=pandemic.id,
        file_id=file.id,
        location=location,
        observation_date=data.get("observation_date") or None,
        new_cases = max(int(float(data.get("new_cases") or 0)), 0),
        new_deaths = max(int(float(data.get("new_deaths") or 0)), 0),
        total_cases = max(int(float(data.get("total_cases") or 0)), 0),
        total_deaths = max(int(float(data.get("total_deaths") or 0)), 0),
        total_recovered = max(int(float(data.get("total_recovered") or 0)), 0),
        created_at=now,
        updated_at=now,
    ))

    # Insert by batch
    if len(batch) >= BATCH_SIZE:
        PandemicData.objects.bulk_create(batch, batch_size=BATCH_SIZE)
        print(f"{idx} lines treated")
        batch.clear()

# Insert the rest in the end
if batch:
    PandemicData.objects.bulk_create(batch, batch_size=BATCH_SIZE)

print(f"Finished import ! {len(data_list) - len(missing_locations)} inserted lines.")
if missing_locations:
    print(f"{len(missing_locations)} locations not found, example : {missing_locations[:5]}")