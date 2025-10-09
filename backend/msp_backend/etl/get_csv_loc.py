import pandas as pd

# JHU Repository GitHub
repo_owner = "CSSEGISandData"
repo_name = "COVID-19"
base_path = "csse_covid_19_data/"
base_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/master/{base_path}" # The raw.githubusercontent.com domain is used to serve unprocessed versions of files stored in GitHub repositories.

# File details
file_name = "UID_ISO_FIPS_LookUp_Table.csv"
file_url = f"{base_url}/{file_name}"

try:
    # Read the CSV file directly from the URL
    df_temp_locations = pd.read_csv(file_url)
    print(f"File '{file_name}' successfully retrieved from GitHub repository.")
    print(df_temp_locations.info())

    # Save as a temporary dataframe for next steps
    df_temp_locations.to_pickle("temp_data.pkl")
    print("Data saved in temp_data.pkl")    

except Exception as e:
    print(f"Error retrieving file '{file_name}': {e}")

# Automation every month (the 1st at 2am) with Cron
cron_line = f"0 2 1 * * {python_path} {script_path} >> {log_path} 2>&1"

# Recover existing crons
result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
existing_cron = result.stdout if result.returncode == 0 else ""

# Add a line in cron if it doesn't exist
if cron_line not in existing_cron:
    new_cron = existing_cron.strip() + "\n" + cron_line + "\n"
    subprocess.run(["crontab", "-"], input=new_cron, text=True)
    print("created")
else:
    print("La tâche cron existe déjà.")

