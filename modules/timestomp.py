"""
BlackWipe Module : Timestomp
Modify file timestamps (creation, modification, access).
"""

import os
import random
import time
from datetime import datetime, timedelta

class TimestompModule:
    def __init__(self):
        self.results = {
            "module": "timestomp",
            "timestamp": datetime.now().isoformat(),
            "actions": []
        }

    def run(self, path, recursive=False, date=None, random_offset=False):
        """
        Modifie les timestamps d'un fichier ou dossier.
        - path : chemin du fichier/dossier
        - recursive : appliquer récursivement aux sous-dossiers
        - date : date fixe au format "YYYY-MM-DD HH:MM:SS" (None = maintenant)
        - random_offset : ajouter un décalage aléatoire (±30 jours)
        """
        print(f"[*] Timestomping {path}...")
        
        if date:
            try:
                target_time = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                print("    [!] Format de date invalide. Utilisation de la date actuelle.")
                target_time = datetime.now()
        else:
            target_time = datetime.now()

        if random_offset:
            days = random.randint(-30, 30)
            target_time += timedelta(days=days)
            print(f"    [i] Décalage aléatoire : {days} jours")

        timestamp = target_time.timestamp()

        if os.path.isfile(path):
            self._stomp_file(path, timestamp)
        elif os.path.isdir(path):
            if recursive:
                self._stomp_dir(path, timestamp)
            else:
                self._stomp_file(path, timestamp)
        else:
            print(f"    [!] {path} n'existe pas")

        return self.results

    def _stomp_file(self, filepath, timestamp):
        try:
            os.utime(filepath, (timestamp, timestamp))
            self.results["actions"].append({
                "file": filepath,
                "new_timestamp": datetime.fromtimestamp(timestamp).isoformat()
            })
            print(f"    [+] {filepath} → {datetime.fromtimestamp(timestamp)}")
        except Exception as e:
            print(f"    [!] Erreur sur {filepath} : {e}")

    def _stomp_dir(self, dirpath, timestamp):
        for root, dirs, files in os.walk(dirpath):
            for name in files + dirs:
                full_path = os.path.join(root, name)
                try:
                    os.utime(full_path, (timestamp, timestamp))
                    self.results["actions"].append({
                        "file": full_path,
                        "new_timestamp": datetime.fromtimestamp(timestamp).isoformat()
                    })
                except Exception as e:
                    print(f"    [!] Erreur sur {full_path} : {e}")
            print(f"    [+] Dossier {root} traité")
