import pandas as pd
import glob
import os
from datetime import datetime

# Data range from March 1, 2020 to March 1, 2022
start = datetime(2020, 3, 1)
end = datetime(2022, 3, 1)

# Final columns to keep
final_columns = [
    "Date","Admin2","Province_State","Country_Region","Confirmed","Deaths","Recovered","Active",
]

# List to hold individual DataFrames
dfs = []

# Loop through all CSV files in the directory
for f in sorted(glob.glob("covid/csse_covid_19_data/csse_covid_19_daily_reports/*.csv")):
    # Extract date from filename
    filename = os.path.basename(f).replace(".csv", "")
    # Parse date and check if within range
    try:
        date = datetime.strptime(filename, "%m-%d-%Y")
        if start <= date <= end:
            df_temp = pd.read_csv(f)
            
            # Standardize column names
            df_temp = df_temp.rename(columns={
                "Province/State": "Province_State",
                "Country/Region": "Country_Region",
            })
            # Add date column
            df_temp["Date"] = date
            # Ensure all final columns are present
            df_temp = df_temp.reindex(columns=final_columns)
            # Append to list
            dfs.append(df_temp)
    except ValueError:
        # Ignore files that don't match the date format
        pass

# Concatenate all DataFrames
df_final = pd.concat(dfs, ignore_index=True)

# Save the final CSV
df_final.to_csv("covid_19.csv", index=False)

print("CSV created : covid_19.csv")

