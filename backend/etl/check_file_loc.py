import pandas as pd
from datetime import datetime
import os

# ========================================
# LOCATIONS DATAFRAME
# ========================================

def check_and_update_locations_referentiel():
    """Check and update the referentiel locations dataframe"""
    # Define final columns
    final_columns_locations = [
        "iso3","city","province_state","country_region","latitude","longitude","combined_key","population"
    ]

    # Create an empty referentiel
    df_referentiel_locations = pd.DataFrame(columns=final_columns_locations)
    print("New locations referentiel created")

    try: 
        # Retrieve the contents of the CSV in memory
        df_temp_locations = pd.read_pickle("/app/etl/locations/temp_data.pkl")
        print("Temporary data loaded from temp_data.pkl") 

        # Map columns to final names
        column_mapping = {
            "iso3": "iso3",
            "Admin2": "city",
            "Province_State": "province_state",
            "Country_Region": "country_region",
            "Lat": "latitude",
            "Long_": "longitude",
            "Combined_Key": "combined_key",
            "Population": "population"
        }

        df_temp_locations = df_temp_locations.rename(columns=column_mapping)

        # Keep only the final columns
        df_temp_locations = df_temp_locations.reindex(columns=final_columns_locations)

        # Concatenate with the referentiel locations dataframe
        df_referentiel_locations = pd.concat([df_referentiel_locations, df_temp_locations], ignore_index=True)

        # Save the referentiel locations dataframe
        df_referentiel_locations.to_pickle("/app/etl/locations/df_referentiel_locations.pkl")
        print("Referentiel locations updated and saved to df_referentiel_locations.pkl")
        print(df_referentiel_locations.info())

    except FileNotFoundError:
        print("No temporary data found. Please run get_csv_loc.py first.")
    except Exception as e: 
        print(f"Error: {e}")

# Execute the function to check and update the locations referentiel
check_and_update_locations_referentiel()

# ========================================
# WHO REGIONS DATAFRAME
# ========================================

def check_and_update_who_regions_referentiel():
    """Check and update the referentiel WHO regions dataframe"""
    
    # Define final columns
    final_columns_who_regions = [
        "iso3","who_region"
    ]

    # Create an empty referentiel
    df_referentiel_who_regions = pd.DataFrame(columns=final_columns_who_regions)
    print("New WHO Regions referentiel created")

    try:
        # Retrieve the contents of the CSV in memory
        df_temp_who_regions = pd.read_pickle("/app/etl/locations/who_regions_temp_data.pkl")
        print("Temporary WHO Regions data loaded from who_regions_temp_data.pkl")

        # Map columns to final names
        column_mapping_who = {
            "Code": "iso3",
            "World regions according to WHO": "who_region"
        }
        df_temp_who_regions = df_temp_who_regions.rename(columns=column_mapping_who)

        # Keep only the final columns
        df_temp_who_regions = df_temp_who_regions.reindex(columns=final_columns_who_regions)

        # Concatenate with the referentiel WHO regions dataframe
        df_referentiel_who_regions = pd.concat([df_referentiel_who_regions, df_temp_who_regions], ignore_index=True)    

        # Save the referentiel WHO regions dataframe
        df_referentiel_who_regions.to_pickle("/app/etl/locations/df_referentiel_who_regions.pkl")
        print("Referentiel WHO Regions updated and saved to df_referentiel_who_regions.pkl")
        print(df_referentiel_who_regions.info())

    except FileNotFoundError:
        print("No temporary WHO Regions data found. Please run get_csv_loc.py first.")
    except Exception as e: 
        print(f"Error: {e}")

# Execute the function to check and update the WHO regions referentiel
check_and_update_who_regions_referentiel()
        