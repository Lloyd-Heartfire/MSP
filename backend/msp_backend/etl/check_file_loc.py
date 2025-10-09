import pandas as pd
from datetime import datetime
import os

# Define final columns
final_columns_locations = [
    "iso3","city","province_state","country_region","latitude","longitude","combined_key","population"
]

# Load the existing referentiel or create an empty one
if os.path.exists("df_referentiel_locations.pkl"):
    df_referentiel_locations = pd.read_pickle("df_referentiel_locations.pkl")
    print(f"Existing referentiel loaded")
else:
    df_referentiel_locations = pd.DataFrame(columns=final_columns_locations)
    print("New referentiel created")

try: 
    # Retrieve the contents of the CSV in memory
    df_temp_locations = pd.read_pickle("temp_data.pkl")
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
    df_referentiel_locations.to_pickle("df_referentiel_locations.pkl")
    print("Referentiel locations updated and saved to df_referentiel_locations.pkl")
    print(df_referentiel_locations.info())

except FileNotFoundError:
    print("No temporary data found. Please run get_csv_loc.py first.")
except Exception as e: 
    print(f"Error: {e}")