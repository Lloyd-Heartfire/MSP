import pandas as pd
from datetime import datetime

# Final columns
final_columns_locations = [
    "iso3","city","province_state","country_region","latitude","longitude","combined_key","population"
]

# Initialize empty dataframe with chosen columns
df_referentiel_locations = pd.DataFrame(columns=final_columns_locations)

# 
try: 
    # Retrieve the contents of the CSV in memory
    df_temp_locations = pd.read_pickle("temp_data.pkl")
    print("Temporary data loaded from temp_data.pkl")    
       
    # Keep only the final columns
    df_temp_locations = df_temp_locations.reindex(columns=final_columns_locations)
    
    # 
    df_referentiel_locations = pd.concat([df_referentiel_locations, df_temp_locations], ignore_index=True)

    # Save
    df_referentiel_locations.to_pickle("referentiel_locations.pkl")
    print("Data saved in referentiel_locations.pkl")
    print(df_referentiel_locations.info())

except Exception as e:
    print(f"Error", e)    

print(df_referentiel_locations.info())