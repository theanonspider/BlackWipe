"""
BlackWipe Module : Registry Cleaner
Nettoyage des clés de registre sensibles (Run, RunOnce, services, etc.)
"""

import os
import platform
from datetime import datetime

try:
    import winreg
    WINDOWS = True
except ImportError:
    WINDOWS = False

class RegistryCleanerModule:
    def __init__(self):
        self.results = {
            "module": "registry_cleaner",
            "timestamp": datetime.now().isoformat(),
            "actions": []
        }
        self.cleaned_keys = []

    def run(self, targets=None):
        """
        Nettoie les clés de registre spécifiées.
        - targets: liste des clés à nettoyer (par défaut: toutes)
        """
        print("[*] Nettoyage du registre...")

        if not WINDOWS:
            print("    [!] Ce module ne fonctionne que sous Windows")
            return self.results

        if platform.system() != "Windows":
            print("    [!] Ce module est spécifique à Windows")
            return self.results

        # Clés sensibles par défaut
        default_targets = [
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\RunOnce"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\RunOnce"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run"),
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedPidlMRU"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSavePidlMRU"),
        ]

        if targets:
            # Convertir les cibles en tuples (hive, path)
            parsed_targets = []
            for t in targets:
                if isinstance(t, tuple):
                    parsed_targets.append(t)
                else:
                    parsed_targets.append((winreg.HKEY_CURRENT_USER, t))
            targets_to_clean = parsed_targets
        else:
            targets_to_clean = default_targets

        for hive, key_path in targets_to_clean:
            self._clean_key(hive, key_path)

        print(f"    [+] {len(self.cleaned_keys)} clé(s) nettoyée(s)")
        return self.results

    def _clean_key(self, hive, key_path):
        try:
            # Ouvrir la clé en écriture
            key = winreg.OpenKey(hive, key_path, 0, winreg.KEY_SET_VALUE | winreg.KEY_READ)
            
            # Récupérer toutes les valeurs
            try:
                i = 0
                values = []
                while True:
                    name, value, type = winreg.EnumValue(key, i)
                    values.append((name, value, type))
                    i += 1
            except OSError:
                pass  # Fin des valeurs

            # Supprimer chaque valeur
            for name, _, _ in values:
                try:
                    winreg.DeleteValue(key, name)
                    self.cleaned_keys.append(f"{self._hive_name(hive)}\\{key_path}\\{name}")
                    print(f"    [+] Supprimé : {name} dans {key_path}")
                except Exception as e:
                    print(f"    [!] Impossible de supprimer {name} : {e}")

            winreg.CloseKey(key)

        except FileNotFoundError:
            print(f"    [~] Clé inexistante : {key_path}")
        except PermissionError:
            print(f"    [!] Permission refusée sur {key_path}")
        except Exception as e:
            print(f"    [!] Erreur sur {key_path} : {e}")

    def _hive_name(self, hive):
        hives = {
            winreg.HKEY_CURRENT_USER: "HKCU",
            winreg.HKEY_LOCAL_MACHINE: "HKLM",
            winreg.HKEY_CLASSES_ROOT: "HKCR",
            winreg.HKEY_USERS: "HKU",
            winreg.HKEY_CURRENT_CONFIG: "HKCC"
        }
        return hives.get(hive, "UNKNOWN")
