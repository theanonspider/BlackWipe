# 🕷️ BlackWipe — Anti‑Forensic Tool

> ⚠️ **AVERTISSEMENT** — Usage exclusivement éducatif et défensif.  
> Toute utilisation non autorisée est **ILLÉGALE** et engage votre responsabilité.

---

## 📖 Pourquoi BlackWipe ?

**BlackWipe** est un outil anti‑forensique léger mais puissant.  
Il permet d’effacer les traces d’une opération autorisée sur Windows (et partiellement Linux) : logs, fichiers, registre, historiques, etc.

Que vous soyez **pentester, Red Teamer ou chercheur en sécurité**, BlackWipe vous aide à **nettoyer proprement** après une mission.

---

## 🧩 Modules (8)

| Module | Fonction |
|--------|----------|
| `log_wiper` | Efface les logs système (Event Logs, syslog) |
| `timestomp` | Modifie les timestamps de fichiers |
| `secure_delete` | Écrasement sécurisé (DoD 5220.22‑M, Gutmann) |
| `registry_cleaner` | Nettoie les clés de registre sensibles |
| `free_space_wiper` | Écrase l’espace libre des disques |
| `history_cleaner` | Efface historiques (navigateurs, shell, fichiers récents) |
| `mft_cleaner` | Nettoie la Master File Table (NTFS) |
| `report` | Génère des rapports JSON + HTML |

---

## 🔐 Sécurité

Un **token** est obligatoire pour exécuter l’outil :

```bash
echo "BLACKWIPE_AUTHORIZED" > blackwipe.token

Sans ce fichier, BlackWipe refuse de s’exécuter.
C’est votre garde‑fou contre toute utilisation accidentelle.
⚙️ Installation
bash

git clone https://github.com/theanonspider/BlackWipe.git
cd BlackWipe
pip install -r requirements.txt
echo "BLACKWIPE_AUTHORIZED" > blackwipe.token

🚀 Exemples d’utilisation
bash

# 1. Effacer les logs
python blackwipe.py wipe-logs

# 2. Modifier les timestamps d’un fichier
python blackwipe.py timestomp -p /path/to/file --random

# 3. Supprimer sécurisé un fichier (3 passes DoD)
python blackwipe.py secure-delete -p /path/to/file -n 3

# 4. Nettoyer tous les historiques
python blackwipe.py history-cleaner --targets all

# 5. Générer un rapport
python blackwipe.py report -o ./reports -f html
📄 Sortie

Rapports dans reports/ : JSON + HTML.

⚖️ Licence

Usage éducatif et défensif uniquement.
👤 Auteur

@theanonspider — Cybersécurité éthique. 🐺
