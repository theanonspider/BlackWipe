"""
BlackWipe Module : Secure Delete
Overwrite files multiple times to prevent forensic recovery.
"""

import os
import random
import math
from datetime import datetime

class SecureDeleteModule:
    def __init__(self):
        self.results = {
            "module": "secure_delete",
            "timestamp": datetime.now().isoformat(),
            "actions": []
        }

    def run(self, path, passes=3, method="dod"):
        """
        Efface sécurisé un fichier.
        - path : chemin du fichier
        - passes : nombre de passes d'écrasement (défaut: 3)
        - method : "dod" (DoD 5220.22-M), "gutmann" (35 passes), "random" (aléatoire)
        """
        print(f"[*] Secure delete : {path} ({passes} passes, method={method})")

        if not os.path.isfile(path):
            print(f"    [!] {path} n'existe pas ou n'est pas un fichier")
            return self.results

        try:
            file_size = os.path.getsize(path)
            if file_size == 0:
                print("    [i] Fichier vide, suppression directe")
                os.remove(path)
                self.results["actions"].append({
                    "file": path,
                    "action": "deleted (empty)",
                    "passes": 0
                })
                return self.results

            # Déterminer les patterns selon la méthode
            patterns = self._get_patterns(method, passes)

            # Ouvrir le fichier en écriture
            with open(path, "r+b") as f:
                for i, pattern in enumerate(patterns):
                    f.seek(0)
                    # Écrire le pattern sur toute la taille du fichier
                    chunk_size = 1024 * 1024  # 1 Mo
                    bytes_written = 0
                    while bytes_written < file_size:
                        chunk = pattern * (chunk_size // len(pattern)) + pattern[:chunk_size % len(pattern)]
                        f.write(chunk.encode() if isinstance(chunk, str) else chunk)
                        bytes_written += len(chunk)
                    f.flush()
                    os.fsync(f.fileno())
                    print(f"    [+] Passe {i+1}/{len(patterns)} terminée")

            # Supprimer le fichier
            os.remove(path)
            self.results["actions"].append({
                "file": path,
                "action": "deleted",
                "passes": len(patterns),
                "method": method
            })
            print(f"    [+] {path} supprimé définitivement")

        except Exception as e:
            print(f"    [!] Erreur : {e}")

        return self.results

    def _get_patterns(self, method, passes):
        patterns = []
        if method == "dod":
            # DoD 5220.22-M : 3 passes
            patterns = [
                b"\x00" * 1024,      # 1: zéros
                b"\xFF" * 1024,      # 2: uns
                b"\xAA" * 1024       # 3: 0xAA (alterné)
            ]
            # Si plus de 3 passes, on complète avec aléatoire
            while len(patterns) < passes:
                patterns.append(bytes([random.randint(0, 255) for _ in range(1024)]))
        elif method == "gutmann":
            # 35 passes (simplifié pour performance)
            patterns = []
            for i in range(35):
                if i < 4:
                    patterns.append(b"\x55" * 1024)  # 0x55
                elif i < 8:
                    patterns.append(b"\xAA" * 1024)  # 0xAA
                elif i < 12:
                    patterns.append(b"\x92" * 1024)  # 0x92
                elif i < 16:
                    patterns.append(b"\x49" * 1024)  # 0x49
                elif i < 20:
                    patterns.append(b"\x24" * 1024)  # 0x24
                elif i < 24:
                    patterns.append(b"\x00" * 1024)  # zéros
                elif i < 28:
                    patterns.append(b"\xFF" * 1024)  # uns
                else:
                    patterns.append(bytes([random.randint(0, 255) for _ in range(1024)]))
            # Limiter aux passes demandées si inférieur à 35
            patterns = patterns[:passes] if passes < 35 else patterns
        else:  # random
            patterns = [bytes([random.randint(0, 255) for _ in range(1024)]) for _ in range(passes)]

        return patterns
