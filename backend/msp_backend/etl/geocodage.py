import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time

#chargement du csv
#placer dans le même dossier pour le moment
df = pd.read_csv('UID_ISO_FIPS_LookUp_Table.csv')

#renommer admin2 en city
df.rename(columns={'Admin2': 'city'}, inplace=True)

#afficher les premières lignes pour vérifier
print("donnée csv avant:")
print(df.head(10))
print(f"nbr de ligne: {len(df)}")
print(f" nom colonne: {list(df.columns)}")

#préparer les colonnes pour le géocodage
df_geocode = df[['iso3', 'city', 'Province_State', 'Country_Region', 'Lat', 'Long_']].copy()

# ajouter les colonnes _new
df_geocode['city_New'] = None
df_geocode['Province_State_New'] = None
df_geocode['Country_Region_New'] = None
df_geocode['iso3_New'] = None

#afficher le dataframe préparé
print("\ndataframe prêt pour le géocodage:")
print(df_geocode.head(10))
print(f"colonnes finales: {list(df_geocode.columns)}")

#les 50 premier lignes pour test 
df_geocode = df_geocode.head(50).copy()
print(f"\ntest sur les {len(df_geocode)} premières lignes uniquement")

#time out au cas ou
geolocator = Nominatim(user_agent="msp_pandemic_geocoder", timeout=10)
#2s entre chaque requête pour eviter les problèmes de quota au niveau API
reverse = RateLimiter(geolocator.reverse, min_delay_seconds=2, max_retries=3, error_wait_seconds=5)

#fonction pour géocodage
def geocode_coordinates(lat, lon, max_attempts=3):
    #on skip si on il manque la lat. ou long.
    if pd.isna(lat) or pd.isna(lon):
        return None, None, None
    
    #on tente jusqu'a 3 fois en cas d'erreur
    for attempt in range(max_attempts):
        try:
            #géocodage methode 'inverse'
            location = reverse(f"{lat}, {lon}", language='en', exactly_one=True)
            if location and location.raw.get('address'):
                address = location.raw['address']
                #extraire city (plusieurs variantes possibles)
                city_new = address.get('city') or address.get('town') or address.get('village') or address.get('municipality')
                #extraire province/state
                state_new = address.get('state') or address.get('province') or address.get('region')
                #extraire country
                country_new = address.get('country')

                #j'ajoute iso3 plus tard
                return city_new, state_new, country_new
            else:
                return None, None, None
        
        except Exception as e:
                print(f"échec sur ({lat}, {lon}): {e}")
                return None, None, None
    return None, None, None

#appliquer le géocodage sur chaque ligne
print("\nprocess, merci de bien vouloir patienter .........(prendre café si besoin)")

#on appel les infos de Geopy
for idx, row in df_geocode.iterrows():
    city_new, state_new, country_new = geocode_coordinates(row['Lat'], row['Long_'])
    df_geocode.at[idx, 'city_New'] = city_new
    df_geocode.at[idx, 'Province_State_New'] = state_new
    df_geocode.at[idx, 'Country_Region_New'] = country_new

print("\ngéocodage fini")
print(df_geocode.head(50))
