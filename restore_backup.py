# restore_backup.py

import os
import shutil

# Huidige directory = projectmap
base_dir = os.path.dirname(os.path.abspath(__file__))

# Correcte locaties
backup_dir = os.path.join(base_dir, ".filtered-graphs")
history_file = os.path.join(base_dir, "history.txt")

def list_backups():
    backups = sorted([
        f for f in os.listdir(backup_dir)
        if f.startswith("history_backup_") and f.endswith(".txt")
    ])
    return backups

def choose_backup(backups):
    print("Beschikbare back-ups:\n")
    for i, name in enumerate(backups):
        print(f"{i + 1}. {name}")
    print()

    while True:
        try:
            choice = int(input("Kies een back-upnummer om te herstellen: ")) - 1
            if 0 <= choice < len(backups):
                return backups[choice]
            else:
                print("Ongeldig nummer, probeer opnieuw.")
        except ValueError:
            print("Voer een geldig nummer in.")

def restore_backup(filename):
    src = os.path.join(backup_dir, filename)
    shutil.copy(src, history_file)
    print(f"\nBack-up '{filename}' is succesvol hersteld naar 'history.txt'.")

def main():
    backups = list_backups()
    if not backups:
        print("Geen back-ups gevonden in .filtered-graphs/")
        return

    selected = choose_backup(backups)
    restore_backup(selected)

if __name__ == "__main__":
    main()

