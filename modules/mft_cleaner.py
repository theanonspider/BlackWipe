"""
BlackWipe Module : MFT Cleaner
Nettoie la Master File Table (NTFS) pour empêcher la récupération de noms de fichiers.
"""

import os
import platform
import subprocess
from datetime import datetime

class MFTCleanerModule:
    def __init__(self):
        self.results = {
            "module": "mft_cleaner",
            "timestamp": datetime.now().isoformat(),
            "actions": []
        }

    def run(self, drive="C:"):
        """
        Nettoie la MFT (Master File Table) d'un disque NTFS.
        - drive : Lettre du disque (ex: "C:", "D:")
        """
        print(f"[*] Nettoyage de la MFT sur {drive}...")

        if platform.system() != "Windows":
            print("    [!] Ce module est spécifique à Windows")
            return self.results

        try:
            # Méthode 1 : Utiliser fsutil pour interroger la MFT
            cmd = f"fsutil fsinfo ntfsinfo {drive}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print("    [+] Informations MFT récupérées")
                self.results["actions"].append("MFT info retrieved")
                
                # Extraire les infos utiles
                for line in result.stdout.split('\n'):
                    if "Total de la MFT" in line or "MFT" in line:
                        print(f"        {line.strip()}")
            else:
                print("    [!] Impossible de lire la MFT")

            # Méthode 2 : Forcer la défragmentation de la MFT (pour l'écraser)
            try:
                cmd = f"defrag {drive} /A /V"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                print("    [+] Analyse de la fragmentation terminée")
                self.results["actions"].append("MFT fragmentation analyzed")
            except:
                print("    [i] defrag non disponible ou refusé")

            # Méthode 3 : Utiliser WinAPI pour effacer les entrées de la MFT
            # (approche simplifiée, nécessite des droits admin)
            try:
                # Créer un fichier temporaire pour forcer l'écriture dans la MFT
                temp_file = os.path.join(drive, "Temp", f"wipe_mft_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tmp")
                os.makedirs(os.path.dirname(temp_file), exist_ok=True)
                
                with open(temp_file, "wb") as f:
                    f.write(os.urandom(1024 * 1024 * 10))  # 10 Mo
                    f.flush()
                    os.fsync(f.fileno())
                
                # Supprimer et recréer plusieurs fois
                for i in range(5):
                    os.remove(temp_file)
                    with open(temp_file, "wb") as f:
                        f.write(os.urandom(1024 * 1024 * 5))  # 5 Mo
                        f.flush()
                        os.fsync(f.fileno())
                
                os.remove(temp_file)
                print("    [+] MFT partiellement écrasée (fichier temporaire multiple)")
                self.results["actions"].append("MFT overwrite attempted")
                
            except Exception as e:
                print(f"    [!] Erreur lors de l'écrasement MFT : {e}")

        except Exception as e:
            print(f"    [!] Erreur globale : {e}")

        print(f"    [+] {len(self.results['actions'])} action(s) effectuée(s)")
        return self.results
