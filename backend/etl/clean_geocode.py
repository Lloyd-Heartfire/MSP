import pandas as pd
from clean_file_loc import clean_who_regions

# ======================================
# LOAD, CLEAN AND STANDARDIZE DATA
# ======================================

def clean_geocode():
    """Clean and standardize the geocoding dataframe"""

    # Load file
    df_geocode = pd.read_csv("geocoded_data.csv")
    print("File 'geocoded_data.csv' loaded.")
    print(df_geocode.info())
    
    # Check duplicates in df_geocode based on 'latitude' and 'longitude'
    geocode_latlong_duplicates = df_geocode[df_geocode.duplicated(subset=["latitude", "longitude"], keep=False)]
    print(f"Number of duplicate records in geocode based on latitude and longitude: {len(geocode_latlong_duplicates)}")
    # if not geocode_latlong_duplicates.empty:
    #     print(geocode_latlong_duplicates)
    # Remove duplicates in df_geocode based on latitude and longitude
    df_geocode = df_geocode.drop_duplicates(subset=["latitude", "longitude"], keep="first")
    # # Check removed duplicates in df_geocode based on latitude and longitude
    # geocode_latlong_duplicates = df_geocode[df_geocode.duplicated(subset=["latitude", "longitude"], keep=False)]
    # print(f"Number of duplicate records in geocode based on latitude and longitude after removing duplicates: {len(geocode_latlong_duplicates)}")
    # if not geocode_latlong_duplicates.empty:
    #     print(geocode_latlong_duplicates)    

    # Check number of missing values in each column
    print("Missing values in each column:")
    print(df_geocode.isnull().sum())

    # k-means clustering to find centroids of locations
    # Si on garde les valeurs manquantes et qu'on les complète via les k-means : on gagne en quantité mais on perd en qualité / pertinence
    # Si on supprime les valeurs manquantes : on perd en quantité mais on gagne en qualité / pertinence

    # Delete missing values in 'city' and 'province_state'
    df_geocode = df_geocode.dropna(subset=["city", "province_state"])
    print(f"Number of records after dropping missing values in 'city' and 'province_state': {len(df_geocode)}")
    print(df_geocode.isnull().sum())

    # Rename "US" to "United States of America"
    df_geocode["country_region"] = df_geocode["country_region"].replace("US", "United States of America")

    # Display cleaned dataframe info
    print("Cleaned geocode dataframe:")
    print(df_geocode.info())

    return df_geocode

# # ======================================
# # WHO REGION MAPPING
# # ======================================

def who_region_mapping(df_geocode, who_regions):
    """Map WHO regions to the geocoding dataframe based on iso3 code"""

    # Merge df_geocode with who_regions on 'iso3'
    df_geocode = df_geocode.merge(who_regions, on="iso3", how="left")

    # Check for missing WHO region
    if df_geocode["who_region"].isna().sum() > 0:
        print("\nCountries without WHO region:")
        print(df_geocode[df_geocode["who_region"].isna()]["country_region"].unique())
    
    # Display final dataframe info
    print("Final geocoding dataframe with WHO regions:")
    print(df_geocode.info())

    # Save final file
    df_geocode.to_csv("full_clean_geocoded_data.csv", index=False)
    print("Final geocoded data with WHO regions saved to 'full_clean_geocoded_data.csv'")

    return df_geocode

# ======================================
# PIPELINE EXECUTION
# ======================================

if __name__ == "__main__":
    df_geocode = clean_geocode()
    who_regions = clean_who_regions()
    df_geocode = who_region_mapping(df_geocode, who_regions)
