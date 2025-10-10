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

# fonction principale qui géocode un dataframe et complète les valeurs vides
def geocode_location_data(df):
    
    print("donnée csv avant:")
    print(df.head(10))
    print(f"nbr de ligne: {len(df)}")
    print(f" nom colonne: {list(df.columns)}")
    
    #compter les valeurs vides avant géocodage
    empty_before = {
        'city': df['city'].isna().sum(),
        'province_state': df['province_state'].isna().sum(),
        'country_region': df['country_region'].isna().sum(),
        'iso3': df['iso3'].isna().sum()
    }
    
    print("\nvaleurs vides avant géocodage:")
    for col, count in empty_before.items():
        print(f"  {col}: {count} valeurs vides")
    
    #préparer les colonnes pour le géocodage
    df_geocode = df[['iso3', 'city', 'province_state', 'country_region', 'latitude', 'longitude']].copy()
    
    #ajouter les colonnes _new temporaires
    df_geocode['city_new'] = None
    df_geocode['province_state_new'] = None
    df_geocode['country_region_new'] = None
    df_geocode['iso3_new'] = None
    
    print(f"\ntravail sur les : {len(df_geocode)} lignes")
    
    #setup du geolocator avec timeout et rate limiter
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
    
    # maintenant on complète les valeurs vides avec les données géocodées
    print("\n Remplace valeurs vides avec les données géocodées...")
    
    #pour chaque colonne on remplit les valeurs vides avec les valeurs géocodées
    df['city'] = df['city'].fillna(df_geocode['city_new'])
    df['province_state'] = df['province_state'].fillna(df_geocode['province_state_new'])
    df['country_region'] = df['country_region'].fillna(df_geocode['country_region_new'])
    df['iso3'] = df['iso3'].fillna(df_geocode['iso3_new'])
    
    #compter les valeurs vides après complétion
    empty_after = {
        'city': df['city'].isna().sum(),
        'province_state': df['province_state'].isna().sum(),
        'country_region': df['country_region'].isna().sum(),
        'iso3': df['iso3'].isna().sum()
    }
    
    print("\nvaleurs vides après complétion:")
    for col, count in empty_after.items():
        filled = empty_before[col] - count
        print(f"  {col}: {count} vides restantes ({filled} complétées)")
    
    print("\nresultat final:")
    print(df.head(50))
    print(f"\nnbr lignes final: {len(df)}")
    print(f"colonnes final: {list(df.columns)}")
    
    return df

#exemple d'utilisation, pour toi mon Théo 

# if __name__ == "__main__":
#     #chargement du csv
#     df = pd.read_csv('cleaned_locations.csv')
    
#     #appel de la fonction de géocodage
#     df_result = geocode_location_data(df)

#     #export en csv avec les colonnes originales pleines
#     output_file = 'geocoded_data.csv'
#     df_result.to_csv(output_file, index=False)
#     print(f"\n nom fichier en sortie : {output_file}")
