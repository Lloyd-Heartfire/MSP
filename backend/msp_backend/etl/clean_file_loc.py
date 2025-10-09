import pandas as pd

# ======================================
# LOAD FILE AND EVALUATE DATA QUALITY
# ======================================

# Loading file
locations = pd.read_pickle("df_referentiel_locations.pkl")
print("File 'df_referentiel_locations.pkl' loaded.")
print(locations.info())

# ======================================
# CLEAN AND STANDARDIZE DATA
# ======================================

# Remove records without essential geographic data
locations = locations.dropna(subset=["iso3","latitude","longitude","population"])

# Change data type into 'integer' for population and 'float' for latitude and longitude
locations["population"] = locations["population"].astype(int)
locations["latitude"] = pd.to_numeric(locations["latitude"], errors="coerce")
locations["longitude"] = pd.to_numeric(locations["longitude"], errors="coerce")

# Check duplicates
duplicates = locations[locations.duplicated(subset=["latitude", "longitude"], keep=False)]
print(f"Number of duplicate records based on latitude and longitude: {len(duplicates)}")
# if not duplicates.empty:
#     print(duplicates)  
# Remove duplicates 
locations = locations.drop_duplicates()

# Export locations to a CSV file 
locations.to_csv("cleaned_locations.csv", index=False)
print("Cleaned locations saved to 'cleaned_locations.csv'")
print(locations.info())

# ======================================
# GEOCODING CHECK
# ======================================

# OTHER PART TO INTEGRATE LATER WITH GEOPY

# ======================================
# TEXT CLEANING
# ======================================

# # Replace missing values with empty strings
# locations = locations.fillna("")

# # Rename "US" to "United States of America"
# locations["Country_Region"] = locations["Country_Region"].replace("US", "United States of America")

# # Remove *, _, and other punctuation (keep -, spaces, apostrophes, parentheses, commas) in columns city, province_state, country_region
# locations["city"] = locations["city"].str.replace(r"[^\w\s\-\(\)',]", "", regex=True).str.strip()
# locations["province_state"] = locations["province_state"].str.replace(r"[^\w\s\-\(\)',]", "", regex=True).str.strip()
# locations["country_region"] = locations["country_region"].str.replace(r"[^\w\s\-\(\)',]", "", regex=True).str.strip()

# # Remove double spaces and leading/trailing spaces
# locations["city"] = locations["city"].str.replace(r'\s+', ' ', regex=True).str.strip()
# locations["province_state"] = locations["province_state"].str.replace(r'\s+', ' ', regex=True).str.strip()
# locations["country_region"] = locations["country_region"].str.replace(r'\s+', ' ', regex=True).str.strip()

# ======================================
# WHO Region mapping
# ======================================

# WHO region mapping based on ISO3 codes
who_region_mapping = {
    # WHO "African Region"
    "DZA": "African Region", 
    "AGO": "African Region", 
    "BEN": "African Region", 
    "BWA": "African Region",
    "BFA": "African Region", 
    "BDI": "African Region", 
    "CPV": "African Region", 
    "CMR": "African Region",
    "CAF": "African Region", 
    "TCD": "African Region", 
    "COM": "African Region", 
    "COG": "African Region",
    "COD": "African Region", 
    "CIV": "African Region", 
    "GNQ": "African Region", 
    "DJI": "African Region", 
    "ERI": "African Region", 
    "SWZ": "African Region", 
    "ETH": "African Region",
    "GAB": "African Region", 
    "GMB": "African Region", 
    "GHA": "African Region", 
    "GIN": "African Region",
    "GNB": "African Region",
    "KEN": "African Region", 
    "LSO": "African Region", 
    "LBR": "African Region", 
    "MDG": "African Region",
    "MWI": "African Region", 
    "MLI": "African Region", 
    "MRT": "African Region", 
    "MUS": "African Region",
    "MOZ": "African Region",
    "NAM": "African Region", 
    "NER": "African Region", 
    "NGA": "African Region", 
    "RWA": "African Region",
    "STP": "African Region", 
    "SEN": "African Region", 
    "SYC": "African Region", 
    "SLE": "African Region",
    "ZAF": "African Region", 
    "SSD": "African Region", 
    "TGO": "African Region",
    "UGA": "African Region",
    "TZA": "African Region",
    
    # WHO "Region of the Americas"
    "ATG": "Region of the Americas", "ARG": "Region of the Americas", "BHS": "Region of the Americas",
    "BRB": "Region of the Americas", "BLZ": "Region of the Americas", "BOL": "Region of the Americas", "BRA": "Region of the Americas",
    "CAN": "Region of the Americas", "CHL": "Region of the Americas", "COL": "Region of the Americas", "CRI": "Region of the Americas",
    "CUB": "Region of the Americas", "DMA": "Region of the Americas", "DOM": "Region of the Americas", "ECU": "Region of the Americas", "SLV": "Region of the Americas",
    "GRD": "Region of the Americas", "GTM": "Region of the Americas", "GUY": "Region of the Americas", "HTI": "Region of the Americas",
    "HND": "Region of the Americas", "JAM": "Region of the Americas", "MEX": "Region of the Americas", "NIC": "Region of the Americas",
    "PAN": "Region of the Americas", "PRY": "Region of the Americas", "PER": "Region of the Americas", "KNA": "Region of the Americas",
    "LCA": "Region of the Americas", "VCT": "Region of the Americas", "SUR": "Region of the Americas", "TTO": "Region of the Americas",
    "USA": "Region of the Americas", "URY": "Region of the Americas", "VEN": "Region of the Americas", "ABW": "Region of the Americas",
    "AIA": "Region of the Americas", "CUW": "Region of the Americas", "MSR": "Region of the Americas", "SXM": "Region of the Americas",
    "TCA": "Region of the Americas", "VGB": "Region of the Americas", "BES": "Region of the Americas",
    
    # WHO "South-East Asia Region"
    "BGD": "South-East Asia Region", "BTN": "South-East Asia Region", "MMR": "South-East Asia Region",
    "IND": "South-East Asia Region", "IDN": "South-East Asia Region", "MDV": "South-East Asia Region",
    "NPL": "South-East Asia Region", "LKA": "South-East Asia Region", "THA": "South-East Asia Region",
    "TLS": "South-East Asia Region", "PRK": "South-East Asia Region", "PAK": "South-East Asia Region",  
    
    # WHO "European Region"
    "ALB": "European Region", "AND": "European Region", "AUT": "European Region", "BLR": "European Region",
    "BEL": "European Region", "BIH": "European Region", "BGR": "European Region", "HRV": "European Region",
    "CYP": "European Region", "CZE": "European Region", "DNK": "European Region", "EST": "European Region",
    "FIN": "European Region", "FRA": "European Region", "DEU": "European Region", "GRC": "European Region",
    "HUN": "European Region", "ISL": "European Region", "IRL": "European Region", "ITA": "European Region",
    "LVA": "European Region", "LTU": "European Region", "LUX": "European Region", "MLT": "European Region",
    "MDA": "European Region", "MCO": "European Region", "MNE": "European Region", "NLD": "European Region",
    "MKD": "European Region", "NOR": "European Region", "POL": "European Region", "PRT": "European Region",
    "ROU": "European Region", "RUS": "European Region", "SMR": "European Region", "SRB": "European Region",
    "SVK": "European Region", "SVN": "European Region", "ESP": "European Region", "SWE": "European Region",
    "CHE": "European Region", "UKR": "European Region", "GBR": "European Region", "VAT": "European Region",

    # WHO "Eastern Mediterranean Region"
    "AFG": "Eastern Mediterranean Region", "BHR": "Eastern Mediterranean Region", "EGY": "Eastern Mediterranean Region",
    "IRN": "Eastern Mediterranean Region", "IRQ": "Eastern Mediterranean Region", "ISR": "Eastern Mediterranean Region",
    "JOR": "Eastern Mediterranean Region", "KWT": "Eastern Mediterranean Region", "LBN": "Eastern Mediterranean Region",
    "LBY": "Eastern Mediterranean Region", "MAR": "Eastern Mediterranean Region", "OMN": "Eastern Mediterranean Region",
    "PSE": "Eastern Mediterranean Region", "QAT": "Eastern Mediterranean Region", "SAU": "Eastern Mediterranean Region",
    "SOM": "Eastern Mediterranean Region", "SSD": "Eastern Mediterranean Region", "SDN": "Eastern Mediterranean Region",
    "SYR": "Eastern Mediterranean Region", "TUN": "Eastern Mediterranean Region", "ARE": "Eastern Mediterranean Region",
    "YEM": "Eastern Mediterranean Region", 

    # WHO "Western Pacific Region"
    "AUS": "Western Pacific Region", "BRN": "Western Pacific Region", "KHM": "Western Pacific Region",
    "CHN": "Western Pacific Region", "COK": "Western Pacific Region", "FJI": "Western Pacific Region",
    "JPN": "Western Pacific Region", "LAO": "Western Pacific Region", "MYS": "Western Pacific Region",
    "MHL": "Western Pacific Region", "FSM": "Western Pacific Region", "NRU": "Western Pacific Region",
    "NZL": "Western Pacific Region", "PLW": "Western Pacific Region", "PNG": "Western Pacific Region",
    "PHL": "Western Pacific Region", "KOR": "Western Pacific Region", "SGP": "Western Pacific Region",
    "SLB": "Western Pacific Region", "TWN": "Western Pacific Region", "TUV": "Western Pacific Region",
    "VUT": "Western Pacific Region", "VNM": "Western Pacific Region", "WSM": "Western Pacific Region", 

}

locations["who_region"] = locations["iso3"].map(who_region_mapping)

# ======================================
# FINAL CHECKS AND SAVE CLEANED FILE
# ======================================

# print("\n=== FINAL CHECKS ===")
# print(f"Final rows: {len(locations):,}")
# print(f"Unique countries: {locations["country"].nunique()}")
# print(f"Missing continents: {locations["continent"].isna().sum()}")
# print(f"Missing WHO regions: {locations["who_region"].isna().sum()}")

# # Display countries without assigned continent
# if locations["continent"].isna().sum() > 0:
#     print("\nCountries without continent:")
#     print(locations[locations["continent"].isna()]["country"].unique())

# # Display countries without assigned WHO region
# if locations["who_region"].isna().sum() > 0:
#     print("\nCountries without WHO region:")
#     print(locations[locations["who_region"].isna()]["country"].unique())

#     # Final column order to match DB schema
# column_order = [
#     "continent", "country", "province_state", "admin2_usa", "iso_code",
#     "latitude", "longitude", "population", "who_region", "combined_key"
# ]
# locations = locations.reindex(columns=column_order)

# print("\n=== FINAL STRUCTURE ===")
# locations.info()
# print("\nFirst rows:")
# print(locations.head())

# # Save cleaned file
# locations.to_csv("full_clean_locations.csv", index=False, encoding="utf-8")
# print(f"\n Cleaned file saved: full_clean_locations.csv")
