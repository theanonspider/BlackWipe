"""
BlackWipe Module : Report Generator
Génère un rapport des actions effectuées (HTML + JSON).
"""

import json
import os
from datetime import datetime

class ReportModule:
    def __init__(self, output_dir="./reports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.results = {
            "tool": "BlackWipe",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "modules": []
        }

    def add_module_result(self, module_name, module_result):
        """Ajoute les résultats d'un module au rapport."""
        self.results["modules"].append({
            "module": module_name,
            "timestamp": datetime.now().isoformat(),
            "data": module_result
        })

    def generate_json(self, filename=None):
        """Génère un rapport JSON."""
        if not filename:
            filename = f"blackwipe_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, "w") as f:
            json.dump(self.results, f, indent=2)
        
        print(f"[+] Rapport JSON généré : {filepath}")
        return filepath

    def generate_html(self, filename=None):
        """Génère un rapport HTML lisible."""
        if not filename:
            filename = f"blackwipe_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Compter les actions totales
        total_actions = 0
        for module in self.results["modules"]:
            if "actions" in module["data"]:
                total_actions += len(module["data"]["actions"])
            elif "cleaned_keys" in module["data"]:
                total_actions += len(module["data"]["cleaned_keys"])

        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BlackWipe Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ background: #0a0a0f; color: #ccc; font-family: 'Courier New', monospace; padding: 40px; }}
        .container {{ max-width: 1000px; margin: 0 auto; }}
        h1 {{ color: #ff1a1a; font-size: 2em; border-bottom: 2px solid #330000; padding-bottom: 15px; margin-bottom: 30px; }}
        h2 {{ color: #ff1a1a; font-size: 1.2em; margin-top: 30px; margin-bottom: 15px; border-left: 3px solid #660000; padding-left: 15px; }}
        .meta {{ background: #0f0f1a; border: 1px solid #1a1a2e; padding: 20px; margin-bottom: 20px; }}
        .meta span {{ color: #666; }}
        .module {{ background: #0f0f1a; border: 1px solid #1a1a2e; padding: 20px; margin-bottom: 20px; }}
        .module-title {{ color: #9b59b6; font-size: 1.1em; margin-bottom: 10px; }}
        .action {{ color: #aaa; padding: 5px 0; border-bottom: 1px solid #111; }}
        .action:last-child {{ border-bottom: none; }}
        .count {{ color: #27ae60; font-weight: bold; }}
        .footer {{ margin-top: 40px; color: #444; text-align: center; font-size: 0.8em; border-top: 1px solid #1a1a2e; padding-top: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🕷️ BlackWipe — Anti‑Forensic Report</h1>
        
        <div class="meta">
            <div><span>Generated:</span> {self.results['timestamp']}</div>
            <div><span>Tool:</span> {self.results['tool']} v{self.results['version']}</div>
            <div><span>Total actions:</span> <span class="count">{total_actions}</span></div>
        </div>

        <h2>📋 Modules Executed</h2>
"""

        for module in self.results["modules"]:
            module_name = module["module"]
            data = module["data"]
            
            # Compter les actions pour ce module
            if "actions" in data:
                nb_actions = len(data["actions"])
                if isinstance(data["actions"][0], dict) if data["actions"] else False:
                    actions_list = []
                    for action in data["actions"]:
                        if "file" in action:
                            actions_list.append(f"File: {action['file']} → {action.get('action', 'modified')}")
                        elif "drive" in action:
                            actions_list.append(f"Drive {action['drive']} - Pass {action.get('pass', 0)}")
                        else:
                            actions_list.append(str(action))
                else:
                    actions_list = data["actions"]
            elif "cleaned_keys" in data:
                nb_actions = len(data["cleaned_keys"])
                actions_list = data["cleaned_keys"]
            else:
                nb_actions = 0
                actions_list = ["No data"]

            html += f"""
        <div class="module">
            <div class="module-title">▪ {module_name.upper()} <span style="color: #666;">({nb_actions} action{'s' if nb_actions > 1 else ''})</span></div>
"""

            if actions_list and len(actions_list) > 0:
                max_display = min(len(actions_list), 20)
                for action in actions_list[:max_display]:
                    html += f'            <div class="action">→ {action}</div>\n'
                if len(actions_list) > 20:
                    html += f'            <div class="action" style="color: #666;">... and {len(actions_list) - 20} more</div>\n'
            else:
                html += '            <div class="action" style="color: #666;">No actions recorded</div>\n'

            html += f"""
        </div>
"""

        html += f"""
        <div class="footer">
            BlackWipe v1.0.0 — Anti‑Forensic Tool<br>
            Generated by BlackWipe on {self.results['timestamp']}
        </div>
    </div>
</body>
</html>"""

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        
        print(f"[+] Rapport HTML généré : {filepath}")
        return filepath

    def get_summary(self):
        """Retourne un résumé textuel."""
        summary = f"BlackWipe v1.0.0 - Report\n"
        summary += f"Generated: {self.results['timestamp']}\n"
        summary += "-" * 40 + "\n"
        
        for module in self.results["modules"]:
            module_name = module["module"]
            data = module["data"]
            if "actions" in data:
                nb = len(data["actions"])
            elif "cleaned_keys" in data:
                nb = len(data["cleaned_keys"])
            else:
                nb = 0
            summary += f"{module_name.upper()}: {nb} action(s)\n"
        
        return summary
