import pandas as pd
import sys
import os
import subprocess

# ========================================
# GET CSV FILE FROM GITHUB
# ========================================

def get_csv_from_github():
    """Get Locations CSV file from JHU GitHub repository"""

    # JHU GitHub repository 
    repo_owner = "CSSEGISandData"
    repo_name = "COVID-19"
    base_path = "csse_covid_19_data"
    base_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/master/{base_path}" 
    # The raw.githubusercontent.com domain is used to serve unprocessed versions of files stored in GitHub repositories.

    # File details
    file_name = "UID_ISO_FIPS_LookUp_Table.csv"
    file_url = f"{base_url}/{file_name}"

    try:
        # Read the CSV file directly from the URL
        df_temp_locations = pd.read_csv(file_url)
        print(f"File '{file_name}' successfully retrieved from GitHub repository.")
        print(df_temp_locations.info())

        # Save as a temporary dataframe for next steps
        # A Pickle file is a serialized binary file format used to store Python objects, including pandas DataFrames. It is more efficient for saving and loading large datasets compared to CSV.
        df_temp_locations.to_pickle("temp_data.pkl")
        print("Data saved in temp_data.pkl")    

    except Exception as e:
        print(f"Error retrieving file '{file_name}': {e}")

# Execute the function to get the CSV file
get_csv_from_github()

# ========================================
# CRON AUTOMATION (execute only once)
# ========================================

def setup_cron():
    """Setup a cron job to run this script on the 1st of each month"""
    
    # Pathes
    python_path = sys.executable # Path to the current Python interpreter
    script_path = os.path.abspath(__file__)  # Path to this script
    script_dir = os.path.dirname(script_path) # Directory of this script
    log_path = f"{script_dir}/cron_logs.log" # Log file path
    
    # Every beginning of each month at midnight
    cron_line = f"0 0 1 * * cd {script_dir} && {python_path} {script_path} >> {log_path} 2>&1"
    
    try:
        # Recover existing crons
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        existing_cron = result.stdout if result.returncode == 0 else ""
        
        # Create cron task only if the script is not already scheduled
        if script_path not in existing_cron:          
            new_cron = existing_cron.strip() + "\n" + cron_line + "\n"
            subprocess.run(["crontab", "-"], input=new_cron, text=True, check=True)        
            print("Cron task created successfully.")
            print(f"Logs in: {log_path}")
        else:
            print("Cron task already exists.")
        
    except FileNotFoundError:
        print("Crontab command not found. Cron setup skipped.")
    except Exception as e:
        print(f"Error while creating the file: {e}")

# Uncomment the line below to setup cron (execute only once)
# setup_cron()
