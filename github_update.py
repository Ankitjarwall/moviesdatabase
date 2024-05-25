import subprocess
import time


def git_auto_push():
    try:
        subprocess.run(['git', 'add', '.'])
        subprocess.run(['git', 'commit', '-m', 'Automated commit'])
        subprocess.run(['git', 'push'])
        print("Code pushed to the repository.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    while True:
        git_auto_push()
        time.sleep(60)  # Wait for 60 seconds before the next push
