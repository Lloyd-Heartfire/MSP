import os
import stat
import subprocess
import shutil

# Variables
repo_url = "https://github.com/CSSEGISandData/COVID-19.git"
clone_dir = "/home/UIMM/project/MSP/Covid-19_github"
folder_to_get = "csse_covid_19_data/csse_covid_19_daily_reports"

# Remove file if it already exist
def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

if os.path.exists(clone_dir):
    shutil.rmtree(clone_dir, onerror=remove_readonly)

subprocess.run([
    "git", "clone", "--depth", "1", "--filter=blob:none", "--sparse", repo_url, clone_dir
], check=True)

subprocess.run(["git", "sparse-checkout", "init", "--cone"], check=True, cwd=clone_dir)
subprocess.run(["git", "sparse-checkout", "set", folder_to_get], check=True, cwd=clone_dir)

# Ensuite copier juste le dossier
shutil.move(os.path.join(clone_dir, folder_to_get), "/home/UIMM/project/MSP/donnees_covid")
shutil.rmtree(clone_dir, onerror=remove_readonly)

print(f"Dossier '{folder_to_get}' récupéré dans {clone_dir}")

python_path = "/usr/bin/python3"
script_path = "/home/UIMM/project/MSP/extract.py"
log_path = "/home/UIMM/project/MSP/extract.log"

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