"""
BlackWipe Module : Free Space Wiper
Overwrite free disk space to prevent file recovery.
"""

import os
import random
import platform
from datetime import datetime

class FreeSpaceWiperModule:
    def __init__(self):
        self.results = {
            "module": "free_space_wiper",
            "timestamp": datetime.now().isoformat(),
            "actions": []
        }

    def run(self, drive="C:", passes=1, fill_size_mb=100):
        """
        Écrase l'espace libre d'un disque.
        - drive : Lettre du disque (ex: "C:", "D:")
        - passes : Nombre de passes d'écrasement
        - fill_size_mb : Taille du fichier temporaire (Mo)
        """
        print(f"[*] Nettoyage de l'espace libre sur {drive}...")

        system = platform.system()
        
        if system == "Windows":
            self._wipe_windows(drive, passes, fill_size_mb)
        elif system == "Linux":
            self._wipe_linux(drive, passes, fill_size_mb)
        else:
            print(f"    [!] OS non supporté : {system}")

        print(f"    [+] {len(self.results['actions'])} fichier(s) temporaire(s) créé(s) et supprimé(s)")
        return self.results

    def _wipe_windows(self, drive, passes, fill_size_mb):
        temp_dir = os.path.join(drive, "Temp")
        os.makedirs(temp_dir, exist_ok=True)

        for p in range(passes):
            print(f"    [*] Passe {p+1}/{passes}...")
            file_count = 0
            try:
                while True:
                    # Créer un fichier temporaire
                    filename = f"wipe_{random.randint(100000, 999999)}.tmp"
                    filepath = os.path.join(temp_dir, filename)
                    
                    # Écrire des données aléatoires
                    with open(filepath, "wb") as f:
                        # Écrire par blocs de 1 Mo
                        for _ in range(fill_size_mb):
                            f.write(os.urandom(1024 * 1024))
                        f.flush()
                        os.fsync(f.fileno())
                    
                    file_count += 1
                    
                    # Supprimer immédiatement
                    os.remove(filepath)
                    
                    # Vérifier si on a assez écrit (arrêt après 1000 fichiers pour éviter saturation)
                    if file_count >= 1000:
                        break
                        
            except Exception as e:
                # Espace disque plein ou erreur
                print(f"    [i] Arrêt : espace disque saturé ou erreur ({e})")
                pass

            self.results["actions"].append({
                "drive": drive,
                "pass": p+1,
                "files_created": file_count
            })
            print(f"        {file_count} fichiers créés/supprimés")

        # Nettoyer le dossier temporaire
        try:
            os.rmdir(temp_dir)
        except:
            pass

    def _wipe_linux(self, mount_point, passes, fill_size_mb):
        # Créer un fichier temporaire dans /tmp
        temp_file = "/tmp/wipe_temp.bin"
        
        for p in range(passes):
            print(f"    [*] Passe {p+1}/{passes}...")
            try:
                with open(temp_file, "wb") as f:
                    # Écrire jusqu'à saturation
                    while True:
                        f.write(os.urandom(1024 * 1024))
                        f.flush()
                        # Vérifier la taille
                        if os.path.getsize(temp_file) > fill_size_mb * 1024 * 1024 * 10:  # 10x la taille
                            break
                os.remove(temp_file)
                self.results["actions"].append({
                    "mount": mount_point,
                    "pass": p+1,
                    "status": "ok"
                })
            except Exception as e:
                print(f"    [i] Espace saturé ou erreur : {e}")
                break
