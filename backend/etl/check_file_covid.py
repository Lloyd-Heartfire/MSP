import pandas as pd
import glob
import os
from datetime import datetime

def check_covid():

    # Data range from March 1, 2020 to March 1, 2022
    start = datetime(2020, 3, 1)
    end = datetime(2022, 3, 1)

    # Final columns to keep
    final_columns = [
        "observation_date","city","province_state","country","total_cases","total_deaths","total_recovered","active_cases","incident_rate"
    ]

    # List to hold individual DataFrames
    dfs = []

    # Loop through all CSV files in the directory
    for f in sorted(glob.glob("/app/etl/covid/csse_covid_19_data/csse_covid_19_daily_reports/*.csv")):
        # Extract date from filename
        filename = os.path.basename(f).replace(".csv", "")
        # Parse date and check if within range
        try:
            date = datetime.strptime(filename, "%m-%d-%Y")
            if start <= date <= end:
                df_temp = pd.read_csv(f)
                
                # Standardize column names
                df_temp = df_temp.rename(columns={
                    "Province_State":"province_state",
                    "Country_Region":"country",
                    "Admin2":"city",
                    "Province/State": "province_State",
                    "Country/Region": "country",
                    "Confirmed":"total_cases",
                    "Deaths":"total_deaths",
                    "Recovered":"total_recovered",
                    "Active":"active_cases",
                    "Incident_Rate":"incident_rate",
                })
                # Add date column
                df_temp["observation_date"] = date
                # Ensure all final columns are present
                df_temp = df_temp.reindex(columns=final_columns)
                # Append to list
                dfs.append(df_temp)
        except ValueError:
            # Ignore files that don't match the date format
            pass

    # Concatenate all DataFrames
    df_final = pd.concat(dfs, ignore_index=True)

    # Créer le dossier si nécessaire
    output_dir = "/app/etl/covid"
    os.makedirs(output_dir, exist_ok=True)

    # Sauvegarder le CSV
    df_final.to_csv(os.path.join(output_dir, "covid_19.csv"), index=False)

    print("CSV created : covid_19.csv")

# check_covid()

