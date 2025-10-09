import os
import stat
import subprocess
import shutil

def get_covid():

    # Variables
    repo_url = "https://github.com/CSSEGISandData/COVID-19.git"
    clone_dir = "/app/etl/covid"
    folder_to_get = "csse_covid_19_data/csse_covid_19_daily_reports"

    # Remove file if it already exist
    def remove_readonly(func, path, excinfo):
        os.chmod(path, stat.S_IWRITE)
        func(path)

    if os.path.exists(clone_dir):
        shutil.rmtree(clone_dir, onerror=remove_readonly)

    # Clone the repo with sparse checkout and filter blob none to only copy what interests us
    subprocess.run(f'git clone --depth 1 --filter=blob:none --sparse "{repo_url}" "{clone_dir}"',
                shell=True, check=True)

    # Configure sparse-checkout to get only the folder we want
    subprocess.run(f'git sparse-checkout set "{folder_to_get}"',
                shell=True, check=True, cwd=clone_dir)

    print(f"Dossier '{folder_to_get}' récupéré dans {clone_dir}")

    python_path = "python"
    script_path = "/app/etl/get_csv.py"
    log_path = "/app/get_csv.log"

    # Every beginning of each month, we use a cron
    cron_line = f"0 0 1 * * {python_path} {script_path} >> {log_path} 2>&1"

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

get_covid()