# BlackWipe — Documentation utilisateur

---

## 📋 Sommaire

1. [Présentation](#présentation)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Modules](#modules)
5. [Commandes](#commandes)
6. [Exemples](#exemples)
7. [Rapports](#rapports)
8. [Compatibilité](#compatibilité)
9. [FAQ](#faq)
10. [Licence](#licence)

---

## 📖 Présentation

**BlackWipe** est un outil anti‑forensique conçu pour effacer les traces d'une opération de sécurité autorisée.

Il permet de :
- Supprimer définitivement des fichiers (écrasement sécurisé)
- Effacer les logs système (Windows Event Logs, syslog)
- Nettoyer le registre Windows
- Modifier les timestamps (timestomping)
- Écraser l'espace libre des disques
- Nettoyer les historiques (navigateurs, shell)
- Générer des rapports d'actions

---

## ⚙️ Installation

### Prérequis

- Python 3.8 ou supérieur
- Windows 10/11 (recommandé) ou Linux

### Étapes

```bash
git clone https://github.com/theanonspider/BlackWipe.git
cd BlackWipe
pip install -r requirements.txt
```

---

## 🔐 Configuration

### Token d'autorisation

L'outil nécessite un token pour s'exécuter :

```bash
echo "BLACKWIPE_AUTHORIZED" > blackwipe.token
```

### Fichier `config.json`

```json
{
  "token_required": true,
  "reports_dir": "./reports",
  "log_level": "info",
  "modules": {
    "log_wiper": true,
    "timestomp": true,
    "secure_delete": true,
    "registry_cleaner": true,
    "free_space_wiper": true,
    "history_cleaner": true,
    "mft_cleaner": true,
    "report": true
  }
}
```

---

## 🧩 Modules

| Module | Fichier | Fonction |
|--------|---------|----------|
| Log Wiper | `log_wiper.py` | Efface les logs système |
| Timestomp | `timestomp.py` | Modifie les timestamps |
| Secure Delete | `secure_delete.py` | Écrasement sécurisé |
| Registry Cleaner | `registry_cleaner.py` | Nettoie le registre |
| Free Space Wiper | `free_space_wiper.py` | Écrase l'espace libre |
| History Cleaner | `history_cleaner.py` | Nettoie les historiques |
| MFT Cleaner | `mft_cleaner.py` | Nettoie la MFT |
| Report | `report.py` | Génère des rapports |

---

## ⌨️ Commandes

### `wipe-logs`

Efface les logs système.

```bash
python blackwipe.py wipe-logs
```

---

### `timestomp`

Modifie les timestamps d'un fichier ou dossier.

```bash
python blackwipe.py timestomp -p /path/to/file
python blackwipe.py timestomp -p /path/to/dir --recursive
```

**Options :**
- `-p, --path` : chemin du fichier/dossier
- `-r, --recursive` : applique récursivement
- `-d, --date` : date cible (format `YYYY-MM-DD HH:MM:SS`)
- `--random` : ajoute un décalage aléatoire

---

### `secure-delete`

Supprime un fichier de manière sécurisée.

```bash
python blackwipe.py secure-delete -p /path/to/file -n 3
```

**Options :**
- `-p, --path` : fichier à supprimer
- `-n, --passes` : nombre de passes (défaut : 3)
- `-m, --method` : `dod`, `gutmann` ou `random`

---

### `registry-cleaner`

Nettoie les clés de registre sensibles.

```bash
python blackwipe.py registry-cleaner
python blackwipe.py registry-cleaner -t "HKCU\Software\Microsoft\Windows\CurrentVersion\Run"
```

**Options :**
- `-t, --targets` : clés spécifiques à nettoyer

---

### `wipe-free-space`

Écrase l'espace libre d'un disque.

```bash
python blackwipe.py wipe-free-space -d C:
python blackwipe.py wipe-free-space -d C: -n 3
```

**Options :**
- `-d, --drive` : lettre du disque (défaut : `C:`)
- `-n, --passes` : nombre de passes (défaut : 1)

---

### `history-cleaner`

Nettoie les historiques (navigateurs, shell, fichiers récents, etc.).

```bash
python blackwipe.py history-cleaner --targets all
python blackwipe.py history-cleaner -t browser -t shell
```

**Options :**
- `-t, --targets` : `browser`, `shell`, `recent`, `powershell`, `bash`, `all`

---

### `mft-cleaner`

Nettoie la Master File Table (NTFS).

```bash
python blackwipe.py mft-cleaner -d C:
```

**Options :**
- `-d, --drive` : lettre du disque (défaut : `C:`)

---

### `report`

Génère un rapport des actions effectuées.

```bash
python blackwipe.py report
python blackwipe.py report -o ./my_reports -f both
```

**Options :**
- `-o, --output` : dossier de sortie (défaut : `./reports`)
- `-f, --format` : `html`, `json` ou `both`

---

## 📄 Exemples

### Effacer toutes les traces sur Windows

```bash
# 1. Créer le token
echo "BLACKWIPE_AUTHORIZED" > blackwipe.token

# 2. Effacer les logs
python blackwipe.py wipe-logs

# 3. Nettoyer le registre
python blackwipe.py registry-cleaner

# 4. Effacer les historiques
python blackwipe.py history-cleaner --targets all

# 5. Écraser l'espace libre du disque C:
python blackwipe.py wipe-free-space -d C:

# 6. Générer un rapport
python blackwipe.py report
```

---

### Supprimer sécurisé un fichier sensible

```bash
python blackwipe.py secure-delete -p /path/to/secret.pdf -n 7 -m gutmann
```

---

## 📊 Rapports

Les rapports sont générés dans le dossier configuré (par défaut `./reports/`) :

- `blackwipe_report_<timestamp>.json` – données brutes (JSON)
- `blackwipe_report_<timestamp>.html` – visualisation (HTML)

---

## 🖥️ Compatibilité

| OS | Modules fonctionnels |
|----|----------------------|
| **Windows 10/11** | ✅ Tous les modules |
| **Linux** | ✅ log_wiper, timestomp, secure_delete, free_space_wiper, history_cleaner |
| **macOS** | ⚠️ Partiel (non testé) |

---

## ❓ FAQ

### L'outil ne s'exécute pas
Vérifie que le fichier `blackwipe.token` existe avec le bon contenu.

### Les logs ne sont pas effacés
Assure-toi d'avoir les droits administrateur sous Windows.

### Le rapport n'est pas généré
Vérifie que le dossier `./reports` est accessible en écriture.

---

## ⚖️ Licence

Ce projet est fourni à des fins **exclusivement éducatives et défensives**.
Toute utilisation non autorisée est interdite.

---

## 👤 Auteur

**@theanonspider** — Pour la cybersécurité éthique. 🐺
