import time
import subprocess
import os

def run_backup_loop():
    print("Automatische backup gestart. Elke 60 minuten wordt history.txt geback-upt.")
    while True:
        try:
            # Ga naar de map waar dit script zich bevindt
            base_dir = os.path.dirname(os.path.abspath(__file__))
            os.chdir(base_dir)

            # Voer backup_history.py uit
            result = subprocess.run(["python3", "backup_history.py"], check=True)
            print("Backup uitgevoerd.")
        except Exception as e:
            print(f"Fout tijdens backup: {e}")

        # Wacht 1 uur
        time.sleep(3600)

if __name__ == "__main__":
    run_backup_loop()
