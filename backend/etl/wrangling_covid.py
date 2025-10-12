import pandas as pd

def clean_covid():
    
    # ------------------------------
    # Step 1 : Load covid-19 CSV
    # ------------------------------

    # Load the CSVs
    df = pd.read_csv("/app/etl/covid/covid_19.csv")

    # Lowercase columns for consistency
    df.columns = df.columns.str.lower()

    # Sort by date
    df = df.sort_values(by='observation_date')

    # Remove rows with unwanted keywords
    mask = df.astype(str).apply(
        lambda col: col.str.contains("Unknown|Unassigned|Out of|Olympics|Recovered|Princess|MS Zaandam|Antarctica|Yakutat|New York City|Others|Repatriated Travellers|Port Quarantine|Federal Correctional Institution (FCI)|Michigan Department of Corrections (MDOC)|(FCI)|(MDOC)", na=False)
    ).any(axis=1)
    df = df[~mask]

    # Do a df and contaneate all rejected data for containing all of that

    # mask.to_csv("covid_19.csv", index=False)

    # Filter dates between 2020-03-01 and 2020-03-21
    df_lat = df[(df["observation_date"] >= "2020-03-01") & (df["observation_date"] <= "2020-03-21")].copy()

    # Clean province_state
    df_lat['province_state'] = df_lat['province_state'].fillna('').str.replace(" County", "", regex=False)
    df_lat['province_state'] = df_lat['province_state'].fillna('').str.replace(" Parish", "", regex=False)

    # Put city from province_state for US entries with comma
    mask_us_comma = (df_lat["country"] == "US") & (df_lat["province_state"].str.contains(","))
    df_lat.loc[mask_us_comma, "city"] = df_lat.loc[mask_us_comma, "province_state"].str.split(",").str[0].str.strip()
    df_lat.loc[mask_us_comma, "province_state"] = df_lat.loc[mask_us_comma, "province_state"].str.split(",").str[-1].str.strip()

    # Replace US state abbreviations with full names
    us_states = {
        "AL": "Alabama","AK": "Alaska","AZ": "Arizona","AR": "Arkansas",
        "CA": "California","CO": "Colorado","CT": "Connecticut","DE": "Delaware",
        "FL": "Florida","GA": "Georgia","HI": "Hawaii","ID": "Idaho",
        "IL": "Illinois","IN": "Indiana","IA": "Iowa","KS": "Kansas",
        "KY": "Kentucky","LA": "Louisiana","ME": "Maine","MD": "Maryland",
        "MA": "Massachusetts","MI": "Michigan","MN": "Minnesota","MS": "Mississippi",
        "MO": "Missouri","MT": "Montana","NE": "Nebraska","NV": "Nevada",
        "NH": "New Hampshire","NJ": "New Jersey","NM": "New Mexico","NY": "New York",
        "NC": "North Carolina","ND": "North Dakota","OH": "Ohio","OK": "Oklahoma",
        "OR": "Oregon","PA": "Pennsylvania","RI": "Rhode Island","SC": "South Carolina",
        "SD": "South Dakota","TN": "Tennessee","TX": "Texas","UT": "Utah",
        "VT": "Vermont","VA": "Virginia","WA": "Washington","WV": "West Virginia",
        "WI": "Wisconsin","WY": "Wyoming"
    }
    # We keep df_lat to concetenate later
    df_lat["province_state"] = df_lat["province_state"].replace(us_states)

    # CSV with population still missing
    # missing_lat=merged[merged["population"].isna()]

    print("Df lat created")

    # ------------------------------
    # Step 2 : Complete population for China, Taiwan and Korea
    # ------------------------------

    df_lat["country"] = df_lat["country"].replace({
        "Mainland China": "China",
        "Hong Kong SAR": "China",
        "Hong Kong": "China",
        "Macau SAR": "China",
        "Taiwan*": "Taiwan",
        "Macau": "China",
        "South Korea":"Korea, South",
        "occupied Palestinian territory":"West Bank and Gaza",
        "Czech Republic": "Czechia",
    })

    # CSV with population still missing
    # merged_china[merged_china["population"].isna()].to_csv("population_still_missing_country.csv", index=False)

    print("Df [lat] changed")

    # CSV with population still missing
    # df_country[df_country["population"].isna()].to_csv("population_still_missing_what.csv", index=False)

    # ------------------------------
    # Step 3 : Adding data the correct data in March
    # ------------------------------

    # Remove rows between 1st and 21st March
    df = df[(df["observation_date"] < "2020-03-01") | (df["observation_date"] > "2020-03-21")]

    # Concatenate with the corrected data
    df_corrected = pd.concat([df, df_lat], ignore_index=True)

    # Sort by date for consistency
    df_corrected = df_corrected.sort_values(by="observation_date")

    # Remove rows where 'long_' or population is NaN
    # df_corrected = df_corrected.dropna(subset=['long_'])
    # df_corrected = df_corrected.dropna(subset=['population'])



    df_corrected.drop_duplicates(inplace=True)

    # ------------------------------
    # Step 4 : Create new cases, deaths, recovered columns and rearrange columns
    # ------------------------------

    # Replace NaN in province_state and city with empty strings
    df_corrected['province_state'] = df_corrected['province_state'].fillna('')
    df_corrected['city'] = df_corrected['city'].fillna('')

    # Order by country, province_state, city, observation_date
    df_corrected = df_corrected.sort_values(['country', 'province_state', 'city', 'observation_date'])

    # Calculate new cases, deaths, recovered
    df_corrected['new_cases'] = df_corrected.groupby(['country', 'province_state', 'city'])['total_cases'].diff().fillna(df_corrected['total_cases'])
    df_corrected['new_deaths'] = df_corrected.groupby(['country', 'province_state', 'city'])['total_deaths'].diff().fillna(df_corrected['total_deaths'])

    # Rename "US" to "United States of America" and Malaysia
    df_corrected["country"] = df_corrected["country"].replace("US", "United States of America")
    df_corrected["province_state"] = df_corrected["province_state"].replace("W.P. Kuala Lumpur","WP Kuala Lumpur")
    df_corrected["province_state"] = df_corrected["province_state"].replace("W.P. Labuan","WP Labuan")
    df_corrected["province_state"] = df_corrected["province_state"].replace("W.P. Putrajaya","WP Putrajaya")

    # Reorder columns if they exist
    columns_order = ['observation_date','country','province_state','city',
                    'total_cases','new_cases',
                    'total_deaths','new_deaths','total_recovered',
                    'active_cases']

    df_corrected = df_corrected[columns_order]

    # ------------------------------
    # Step 5 : Cleaning data
    # ------------------------------

    # Replace negative values
    cols_to_check = ['total_cases','total_deaths','total_recovered','active_cases','new_cases','new_deaths']
    df_corrected[cols_to_check] = df_corrected[cols_to_check].clip(lower=0)

    # Identify duplicates
    duplicates = df_corrected[df_corrected.duplicated(subset=['observation_date','country','province_state','city'], keep=False)]
    if not duplicates.empty:
        print(f"Duplicates detected : {len(duplicates)} lines")
    else:
        print("No duplicates detected")

    # Remove duplicates
    df_corrected = df_corrected.sort_values(cols_to_check).drop_duplicates(
        subset=['observation_date','country','province_state','city'],
        keep='last'
    )

    # Remove special characters
    df_corrected["country"] = df_corrected["country"].str.replace(r"[^\w\s\-\(\)',]", "", regex=True)
    df_corrected["province_state"] = df_corrected["province_state"].str.replace(r"[^\w\s\-\(\)',]", "", regex=True)
    df_corrected["city"] = df_corrected["city"].str.replace(r"[^\w\s\-\(\)',]", "", regex=True)

    # Remove double spaces and leading/trailing spaces
    df_corrected["country"] = df_corrected["country"].str.replace(r'\s+', ' ', regex=True).str.strip()
    df_corrected["province_state"] = df_corrected["province_state"].str.replace(r'\s+', ' ', regex=True).str.strip()
    df_corrected["city"] = df_corrected["city"].str.replace(r'\s+', ' ', regex=True).str.strip()


    # === 4. Colonnes numériques à agréger ===
    cols_to_sum = ["new_cases", "total_cases", "new_deaths", "total_deaths", "active_cases"]

    dates_debut = {
        "Malaysia": "2020-03-22",
        "Japan": "2020-05-28",
        "Italy": "2020-06-14",
        "India": "2020-06-10",
        "Belgium": "2020-11-12",
        "Brazil": "2020-05-20",
        "Colombia": "2020-05-28",
        "Germany": "2020-05-15",
        "Spain": "2020-05-15",
        "Netherlands": "2020-07-17",
        "Pakistan": "2020-06-10",
        "Peru": "2020-05-28",
        "Russia": "2020-06-01",
        "Sweden": "2020-06-05",
        "Ukraine": "2020-06_01",
        "Canada": "2020-03-22",
        "China": "2020-03-22",
        "United States of America": "2020-03-22"
    }

    results = []

    for country, start_date in dates_debut.items():
        df_country = (
            df_corrected[
                (df_corrected["country"] == country)
                & (df_corrected["observation_date"] >= start_date)
            ]
            .groupby(["observation_date", "country"], as_index=False)[cols_to_sum]
            .sum()
        )
        df_country["date_debut"] = start_date
        results.append(df_country)

    
    df_corrected = pd.concat([df_corrected] + results, ignore_index=True)
    df_corrected = df_corrected.sort_values(['observation_date','country', 'province_state', 'city'])
    df_corrected.drop_duplicates(inplace=True)
    # ------------------------------
    # Step 6 : Save as JSON (and CSV)
    # ------------------------------
    

    # df_corrected.to_csv("full_clean_covid_19.csv", index=False)
    # print("CSV created")
    df_corrected.to_csv("/app/etl/covid/full_clean_covid_19.csv", index=False)
    df_corrected.to_json("/app/etl/covid/full_clean_covid_19.json", orient="records", force_ascii=False)
    print("JSON created")
    # Check if missing population
    # Check if missing latitude

# clean_covid()