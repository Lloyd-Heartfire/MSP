import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time
import pycountry

#fonction pour psser l'iso2 obtenue avec GeoPy en iso3
def iso2_to_iso3(iso2_code):
    #si vide on laisse vide
    if not iso2_code:
        return None
    try:
        #conversion iso2 to iso3 avec pycountry
        country = pycountry.countries.get(alpha_2=iso2_code.upper())
        return country.alpha_3 if country else None
    except:
        return None

#chargement du csv
#placer dans le même dossier pour le moment
df = pd.read_csv('cleaned_locations.csv')

#afficher les premières lignes pour vérifier
print("donnée csv avant:")
print(df.head(10))
print(f"nbr de ligne: {len(df)}")
print(f" nom colonne: {list(df.columns)}")

#préparer les colonnes pour le géocodage
df_geocode = df[['iso3', 'city', 'province_state', 'country_region', 'latitude', 'longitude']].copy()

# ajouter les colonnes _new
df_geocode['city_new'] = None
df_geocode['province_state_new'] = None
df_geocode['country_region_new'] = None
df_geocode['iso3_new'] = None

#afficher le dataframe préparé
print("\ndataframe prêt pour le géocodage:")
print(df_geocode.head(10))
print(f"colonnes finales: {list(df_geocode.columns)}")

print(f"\ntravail sur les : {len(df_geocode)} lignes")

#time out au cas ou
geolocator = Nominatim(user_agent="msp_pandemic_geocoder", timeout=10)
#2s entre chaque requête pour eviter les problèmes de quota au niveau API
reverse = RateLimiter(geolocator.reverse, min_delay_seconds=2, max_retries=3, error_wait_seconds=5)

#fonction pour géocodage
def geocode_coordinates(lat, lon, max_attempts=3):
    #on skip si on il manque la lat. ou long.
    if pd.isna(lat) or pd.isna(lon):
        return None, None, None, None
    
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

                #recupére iso2 (car ne fournit pas iso3) et convertir en iso3 avec la fonction en début de code qui utilise pycountry
                iso2_code = address.get('country_code')
                iso3_new = iso2_to_iso3(iso2_code)
                
                return city_new, state_new, country_new, iso3_new
            else:
                return None, None, None, None
        
        except Exception as e:
                print(f"échec sur ({lat}, {lon}): {e}")
                return None, None, None, None
    return None, None, None, None

#appliquer le géocodage sur chaque ligne
print("\nprocess en cours ,merci de bien vouloir patienter .........(prendre café si besoin)")

#on appel les infos de Geopy
for idx, row in df_geocode.iterrows():
    city_new, state_new, country_new, iso3_new = geocode_coordinates(row['latitude'], row['longitude'])
    df_geocode.at[idx, 'city_new'] = city_new
    df_geocode.at[idx, 'province_state_new'] = state_new
    df_geocode.at[idx, 'country_region_new'] = country_new
    df_geocode.at[idx, 'iso3_new'] = iso3_new

print("\ngéocodage fini")
print(df_geocode.head(50))

#ajouter directement les colonnes géocodées au dataframe original
#car ils gardent le même index, et cela nous evité les problèmes de doublons du au merge
print("\najout des colonnes géocodées...")
df['city_new'] = df_geocode['city_new']
df['province_state_new'] = df_geocode['province_state_new']
df['country_region_new'] = df_geocode['country_region_new']
df['iso3_new'] = df_geocode['iso3_new']
df_final = df

print("\nresultat du merge:")
print(df_final.head(50))
print(f"\nnbr lignes final: {len(df_final)}")
print(f"colonnes final: {list(df_final.columns)}")

#export en csv
output_file = 'geocoded_data.csv'
df_final.to_csv(output_file, index=False)
print(f"\n nom fichier out : {output_file}")
