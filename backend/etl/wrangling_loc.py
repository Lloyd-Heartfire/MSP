import pandas as pd

# ======================================
# LOAD, CLEAN AND STANDARDIZE DATA - LOCATIONS
# ======================================

def clean_locations():
    """Clean and standardize the locations dataframe"""

    # Load file
    locations = pd.read_pickle("/app/etl/locations/df_referentiel_locations.pkl")
    print("File 'df_referentiel_locations.pkl' loaded.")
    print(locations.info())

    # Remove records without essential geographic data
    locations = locations.dropna(subset=["iso3","latitude","longitude","population"])

    # Change data type into 'integer' for population and 'float' for latitude and longitude
    locations["population"] = locations["population"].astype(int)
    locations["latitude"] = pd.to_numeric(locations["latitude"], errors="coerce")
    locations["longitude"] = pd.to_numeric(locations["longitude"], errors="coerce")

    # Standardize iso3 to uppercase
    locations["iso3"] = locations["iso3"].str.upper()

        # Remove special characters
    locations["country_region"] = locations["country_region"].str.replace(r"[^\w\s\-\(\)',]", "", regex=True)
    locations["province_state"] = locations["province_state"].str.replace(r"[^\w\s\-\(\)',]", "", regex=True)
    locations["city"] = locations["city"].str.replace(r"[^\w\s\-\(\)',]", "", regex=True)

    # Remove double spaces and leading/trailing spaces
    locations["country_region"] = locations["country_region"].str.replace(r'\s+', ' ', regex=True).str.strip()
    locations["province_state"] = locations["province_state"].str.replace(r'\s+', ' ', regex=True).str.strip()
    locations["city"] = locations["city"].str.replace(r'\s+', ' ', regex=True).str.strip()

    # Check duplicates in locations based on latitude and longitude
    loc_duplicates = locations[locations.duplicated(subset=["latitude", "longitude"], keep=False)]
    print(f"Number of duplicate records based on latitude and longitude: {len(loc_duplicates)}")
    if not loc_duplicates.empty:
        print(loc_duplicates)  
    # Remove duplicates in locations based on latitude and longitude
    locations = locations.drop_duplicates(subset=["latitude", "longitude"], keep="first")
    # # Check removed duplicates 
    # loc_duplicates = locations[locations.duplicated(subset=["latitude", "longitude"], keep=False)]
    # print(f"Number of duplicate records based on latitude and longitude after removing duplicates: {len(loc_duplicates)}")
    # if not loc_duplicates.empty:
    #     print(loc_duplicates)

    print("Cleaned locations:")
    print(locations.info())

    return locations

# ======================================
# LOAD, CLEAN AND STANDARDIZE DATA - WHO REGIONS
# ======================================

def clean_who_regions():
    """Clean and standardize the WHO regions dataframe"""

    # Load file
    who_regions = pd.read_pickle("/app/etl/locations/df_referentiel_who_regions.pkl")
    print("File 'df_referentiel_who_regions.pkl' loaded.")
    print(who_regions.info())

    # Standardize iso3 to uppercase
    who_regions["iso3"] = who_regions["iso3"].str.upper()

    # Remove *, _, and other punctuation (keep -, spaces, apostrophes, parentheses, commas) in columns who_region, iso3
    who_regions["who_region"] = who_regions["who_region"].str.replace(r"[^\w\s\-\(\)',]", "", regex=True).str.strip()
    who_regions["iso3"] = who_regions["iso3"].str.replace(r"[^\w\s\-\(\)',]", "", regex=True).str.strip()

    # Remove double spaces and leading/trailing spaces
    who_regions["who_region"] = who_regions["who_region"].str.replace(r'\s+', ' ', regex=True).str.strip()
    who_regions["iso3"] = who_regions["iso3"].str.replace(r'\s+', ' ', regex=True).str.strip()  

    # Check duplicates in who_regions based on iso3
    who_duplicates = who_regions[who_regions.duplicated(subset=["iso3"], keep=False)]
    print(f"Number of duplicate records in WHO regions based on iso3: {len(who_duplicates)}")
    if not who_duplicates.empty:
        print(who_duplicates)
    # Remove duplicates in who_regions based on iso3
    who_regions = who_regions.drop_duplicates(subset=["iso3"], keep="first")
    # # Check removed duplicates
    # who_duplicates = who_regions[who_regions.duplicated(subset=["iso3"], keep=False)]
    # print(f"Number of duplicate records in WHO regions based on iso3 after removing duplicates: {len(who_duplicates)}")
    # if not who_duplicates.empty:
    #     print(who_duplicates)

    # Remove " (WHO)" from column who_region if exists
    who_regions["who_region"] = who_regions["who_region"].str.replace(" (WHO)", "", regex=False)
    print("Cleaned WHO regions:")
    print(who_regions["who_region"].unique())  

    print("Cleaned WHO regions:")
    print(who_regions.info())

    return who_regions

# # ======================================
# # WHO REGION MAPPING
# # ======================================

def who_region_mapping(locations, who_regions):
    """Map WHO regions to locations dataframe based on iso3 code"""

    # Merge locations with who_regions on iso3
    locations = locations.merge(who_regions[["iso3", "who_region"]], on="iso3", how="left")

    # Check for countries without assigned WHO region
    if locations["who_region"].isna().sum() > 0:
        print("\nCountries without WHO region:")
        print(locations[locations["who_region"].isna()]["country_region"].unique())

    print("Locations with WHO regions mapped:")
    print(locations.info())

     
    locations["country_region"] = locations["country_region"].replace("US", "United States of America")

    # Save cleaned file
    locations.to_csv("/app/etl/locations/full_clean_locations.csv", index=False, encoding="utf-8")
    locations.to_json("/app/etl/locations/full_clean_locations.json", orient="records", force_ascii=False)

    print(f"\n Cleaned locations file saved: full_clean_locations.csv")

    return locations

# ======================================
# PIPELINE EXECUTION
# ======================================

if __name__ == "__main__":
    locations = clean_locations()
    who_regions = clean_who_regions()
    locations = who_region_mapping(locations, who_regions)
