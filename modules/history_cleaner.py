"""
BlackWipe Module : History Cleaner
Efface les historiques de navigation, commandes shell, fichiers récents, etc.
"""

import os
import shutil
import platform
import glob
from datetime import datetime

class HistoryCleanerModule:
    def __init__(self):
        self.results = {
            "module": "history_cleaner",
            "timestamp": datetime.now().isoformat(),
            "actions": []
        }

    def run(self, targets=None):
        """
        Nettoie les historiques.
        - targets: liste des cibles à nettoyer (browser, shell, recent, all)
        """
        print("[*] Nettoyage des historiques...")

        if not targets:
            targets = ["all"]

        if "all" in targets:
            targets = ["browser", "shell", "recent", "powershell", "bash"]

        system = platform.system()

        if "browser" in targets or "all" in targets:
            self._clean_browsers()
        
        if "shell" in targets or "all" in targets:
            self._clean_shell_history()
        
        if "recent" in targets or "all" in targets:
            self._clean_recent_files()
        
        if "powershell" in targets or "all" in targets:
            self._clean_powershell_history()
        
        if "bash" in targets or "all" in targets:
            self._clean_bash_history()

        print(f"    [+] {len(self.results['actions'])} action(s) effectuée(s)")
        return self.results

    def _clean_browsers(self):
        print("[*] Nettoyage des navigateurs...")
        
        system = platform.system()
        if system == "Windows":
            home = os.environ.get("USERPROFILE")
        else:
            home = os.environ.get("HOME")

        if not home:
            return

        # Chrome
        chrome_paths = [
            os.path.join(home, "AppData", "Local", "Google", "Chrome", "User Data", "Default", "History"),
            os.path.join(home, "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Cookies"),
            os.path.join(home, "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Login Data"),
            os.path.join(home, ".config", "google-chrome", "Default", "History"),
            os.path.join(home, ".config", "google-chrome", "Default", "Cookies"),
        ]
        for path in chrome_paths:
            if os.path.exists(path):
                try:
                    os.remove(path)
                    self.results["actions"].append(f"Chrome: {path} supprimé")
                    print(f"    [+] Chrome: {path}")
                except Exception as e:
                    print(f"    [!] Chrome: {e}")

        # Firefox
        firefox_base = os.path.join(home, "AppData", "Roaming", "Mozilla", "Firefox", "Profiles")
        if os.path.exists(firefox_base):
            for profile in os.listdir(firefox_base):
                profile_path = os.path.join(firefox_base, profile)
                if os.path.isdir(profile_path):
                    for file in ["places.sqlite", "places.sqlite-wal", "cookies.sqlite", "cookies.sqlite-wal"]:
                        filepath = os.path.join(profile_path, file)
                        if os.path.exists(filepath):
                            try:
                                os.remove(filepath)
                                self.results["actions"].append(f"Firefox: {filepath} supprimé")
                                print(f"    [+] Firefox: {filepath}")
                            except:
                                pass

        # Edge
        edge_paths = [
            os.path.join(home, "AppData", "Local", "Microsoft", "Edge", "User Data", "Default", "History"),
            os.path.join(home, "AppData", "Local", "Microsoft", "Edge", "User Data", "Default", "Cookies"),
        ]
        for path in edge_paths:
            if os.path.exists(path):
                try:
                    os.remove(path)
                    self.results["actions"].append(f"Edge: {path} supprimé")
                    print(f"    [+] Edge: {path}")
                except:
                    pass

    def _clean_shell_history(self):
        print("[*] Nettoyage des historiques shell...")
        
        system = platform.system()
        if system == "Windows":
            # CMD history
            try:
                os.system("doskey /REINSTALL")
                self.results["actions"].append("CMD history cleared")
                print("    [+] CMD history réinitialisé")
            except:
                pass

            # PowerShell (supprimer le fichier)
            ps_history = os.path.join(os.environ.get("APPDATA", ""), "Microsoft", "Windows", "PowerShell", "PSReadLine", "ConsoleHost_history.txt")
            if os.path.exists(ps_history):
                try:
                    os.remove(ps_history)
                    self.results["actions"].append("PowerShell history cleared")
                    print("    [+] PowerShell history supprimé")
                except:
                    pass

    def _clean_recent_files(self):
        print("[*] Nettoyage des fichiers récents...")
        
        system = platform.system()
        if system == "Windows":
            recent_dir = os.path.join(os.environ.get("APPDATA", ""), "Microsoft", "Windows", "Recent")
            if os.path.exists(recent_dir):
                for item in os.listdir(recent_dir):
                    try:
                        os.remove(os.path.join(recent_dir, item))
                    except:
                        pass
                self.results["actions"].append("Recent files cleared")
                print("    [+] Fichiers récents supprimés")

    def _clean_powershell_history(self):
        print("[*] Nettoyage PowerShell history...")
        try:
            if platform.system() == "Windows":
                ps_history = os.path.join(os.environ.get("APPDATA", ""), "Microsoft", "Windows", "PowerShell", "PSReadLine", "ConsoleHost_history.txt")
                if os.path.exists(ps_history):
                    os.remove(ps_history)
                    self.results["actions"].append("PowerShell history cleared")
                    print("    [+] PowerShell history supprimé")
        except:
            pass

    def _clean_bash_history(self):
        print("[*] Nettoyage Bash history...")
        home = os.environ.get("HOME")
        if home:
            bash_history = os.path.join(home, ".bash_history")
            if os.path.exists(bash_history):
                try:
                    os.remove(bash_history)
                    self.results["actions"].append("Bash history cleared")
                    print("    [+] Bash history supprimé")
                except:
                    pass
