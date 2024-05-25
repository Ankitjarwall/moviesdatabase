import subprocess

# List of your Python scripts
scripts = [
    r"index.py",
    r"github_update.py",
    # r"C:\path\to\script3.py",
]

for script in scripts:
    subprocess.run(["python", script], check=True)
