# 🕷️ BlackWipe — Anti-Forensic Tool

> ⚠️ **AVERTISSEMENT** — Cet outil est conçu exclusivement pour :
> - Des tests d'intrusion **autorisés** (pentests, Red Team)
> - La **formation** et la **recherche** en cybersécurité défensive
> - Des démonstrations d'impact dans un cadre **contractuel**
>
> **Toute utilisation sur un système sans autorisation écrite est ILLÉGALE.**
> L'auteur décline toute responsabilité en cas d'usage malveillant.

---

## 📖 Description

**BlackWipe** est un outil anti‑forensique pour Windows et Linux. Il permet d'effacer les traces d'une opération autorisée : logs, timestamps, fichiers, registre, espace libre, historiques, MFT, etc.

L'outil ne communique **jamais** avec Internet. Toutes les actions sont enregistrées localement dans un rapport (JSON + HTML).

---

## 🔐 Sécurité intégrée

L'exécution est **bloquée** sans un fichier d'autorisation :

1. Créer le fichier `blackwipe.token` à la racine
2. Écrire `BLACKWIPE_AUTHORIZED` dedans

Sans ce fichier, le programme refuse de s'exécuter.

---

## 🧩 Modules (8)

| Module | Fonction |
|--------|----------|
| `log_wiper` | Efface les logs système (Event Logs, syslog) |
| `timestomp` | Modifie les timestamps des fichiers |
| `secure_delete` | Écrasement sécurisé (DoD, Gutmann, aléatoire) |
| `registry_cleaner` | Nettoie les clés de registre sensibles |
| `free_space_wiper` | Écrase l'espace libre des disques |
| `history_cleaner` | Efface historiques (navigateurs, shell, fichiers récents) |
| `mft_cleaner` | Nettoie la Master File Table (NTFS) |
| `report` | Génère des rapports JSON + HTML |

---

## ⚙️ Installation

```bash
git clone https://github.com/theanonspider/BlackWipe.git
cd BlackWipe
pip install -r requirements.txt
```

---

## 🚀 Utilisation

### 1. Créer le token d'autorisation

```bash
echo "BLACKWIPE_AUTHORIZED" > blackwipe.token
```

### 2. Exécuter un module

```bash
# Effacer les logs
python blackwipe.py wipe-logs

# Modifier les timestamps d'un fichier
python blackwipe.py timestomp -p /path/to/file

# Supprimer sécurisé un fichier (3 passes)
python blackwipe.py secure-delete -p /path/to/file -n 3

# Nettoyer le registre
python blackwipe.py registry-cleaner

# Effacer l'espace libre du disque C:
python blackwipe.py wipe-free-space -d C:

# Nettoyer les historiques
python blackwipe.py history-cleaner --targets all

# Nettoyer la MFT
python blackwipe.py mft-cleaner -d C:

# Générer un rapport
python blackwipe.py report
```

### 3. Voir toutes les commandes

```bash
python blackwipe.py --help
```

---

## 📄 Sortie

Tous les modules génèrent un rapport dans le dossier `reports/` :
- `blackwipe_report_<timestamp>.json`
- `blackwipe_report_<timestamp>.html`

---

## 🛠️ Compatibilité

| OS | Modules fonctionnels |
|----|----------------------|
| Windows 10/11 | ✅ Tous les modules |
| Linux | ✅ log_wiper, timestomp, secure_delete, free_space_wiper, history_cleaner |
| macOS | ⚠️ Partiel (non testé) |

---

## ⚖️ Licence

Ce projet est fourni à des fins **exclusivement éducatives et défensives**.
Toute utilisation non autorisée est interdite.

---

## 👤 Auteur

Projet maintenu par **@theanonspider** — Pour la cybersécurité éthique. 🐺
