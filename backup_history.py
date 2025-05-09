import os
import shutil
from datetime import datetime

def backup_history():
    # Vind het pad van de map waar dit script zich bevindt
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Pad naar het originele history.txt bestand
    source_file = os.path.join(base_dir, "history.txt")

    # Pad naar de map waar de backups worden opgeslagen (~/.filtered-graphs)
    backup_dir = os.path.join(base_dir, ".filtered-graphs")
    os.makedirs(backup_dir, exist_ok=True)

    # Als history.txt bestaat, maak een backup
    if os.path.exists(source_file):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"history_backup_{timestamp}.txt")
        shutil.copy2(source_file, backup_file)
        print(f"Backup gemaakt: {backup_file}")
    else:
        print(f"Bestand niet gevonden: {source_file}")

if __name__ == "__main__":
    backup_history()

