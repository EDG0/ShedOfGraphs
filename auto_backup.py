# auto_backup.py

import os
import time
import subprocess

def run_backup_loop():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)  # Zorg dat je altijd werkt vanuit de juiste map

    while True:
        try:
            subprocess.run(["python3", "backup_history.py"], check=True)
            print("[auto_backup] Backup uitgevoerd op", time.strftime("%Y-%m-%d %H:%M:%S"))
        except subprocess.CalledProcessError as e:
            print("[auto_backup] Fout tijdens uitvoeren van backup:", e)
        except KeyboardInterrupt:
            print("\n[auto_backup] Backup gestopt door gebruiker.")
            break

        # Wacht één uur (3600 seconden)
        time.sleep(3600)

if __name__ == "__main__":
    run_backup_loop()


