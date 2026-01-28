#!/usr/bin/env python3
import os
import subprocess
import argparse
import sys
import xml.etree.ElementTree as ET
from datetime import datetime

# Configuration des profils de scan
SCAN_PROFILES = {
    "quick": {
        "args": "-sV -sC -A -T4",
        "desc": "Scan standard (1 000 ports) avec détection d'OS, services et scripts par défaut."
    },
    "full": {
        "args": "-p- -sV -sC -A -T4",
        "desc": "Scan exhaustif de tous les ports (65535), détection complète et scripts."
    },
    "stealth": {
        "args": "-sS -Pn -f -T2",
        "desc": "Scan furtif (SYN scan, fragmentation, vitesse lente) sans ping."
    }
}

def print_banner():
    banner = """
  _   _                      ____                      
 | \ | |_ __ ___   __ _ _ __/ ___|  ___ __ _ _ __      
 |  \| | '_ ` _ \ / _` | '_ \___ \ / __/ _` | '_ \     
 | |\  | | | | | | (_| | |_) |__) | (_| (_| | | | |    
 |_| \_|_| |_| |_|\__,_| .__/____/ \___\__,_|_| |_|    
                       |_|                             
    --- Microgiciel de scan de port ---
    """
    print(banner)

# Exécution des scans Nmap selon le profil choisi
def run_nmap(target, mode):
    """Exécute nmap et retourne le chemin du fichier XML généré."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_xml = f"reports/scan_{target.replace('.', '_')}_{timestamp}.xml"
    
    nmap_cmd = f"nmap {SCAN_PROFILES[mode]['args']} -oX {output_xml} {target}"
    
    print(f"[*] Mode : {mode.upper()}")
    print(f"[*] Cible : {target}")
    print(f"[*] Lancement de Nmap... (cela peut prendre du temps)\n")
    
    try:
        # Shell=True pour la simplicité de la commande
        subprocess.run(nmap_cmd, shell=True, check=True)
        return output_xml
    except subprocess.CalledProcessError:
        print("\n❌ Erreur : Nmap a échoué. Vérifie tes droits (sudo requis pour stealth).")
        sys.exit(1)

# Construction du rapport Markdown à partir du XML
def build_report(xml_path, target, mode):
    """Analyse le XML et génère un fichier Markdown."""
    md_path = xml_path.replace(".xml", ".md")
    
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(f"# Rapport de Scan : {target}\n\n")
            f.write(f"- **Date** : {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
            f.write(f"- **Profil** : {mode.upper()}\n")
            f.write(f"- **Détails** : {SCAN_PROFILES[mode]['desc']}\n\n")
            
            f.write("## 📝 Résultats des Ports Ouverts\n\n")
            f.write("| Port | Protocole | État | Service | Version |\n")
            f.write("| :--- | :--- | :--- | :--- | :--- |\n")
            
            for port in root.findall(".//port"):
                state = port.find('state').get('state')
                if state == "open":
                    port_id = port.get('portid')
                    proto = port.get('protocol')
                    service_tag = port.find('service')
                    service = service_tag.get('name', 'N/A') if service_tag is not None else "N/A"
                    product = service_tag.get('product', '') if service_tag is not None else ""
                    version = service_tag.get('version', '') if service_tag is not None else ""
                    
                    f.write(f"| {port_id} | {proto} | {state} | {service} | {product} {version} |\n")
        
        return md_path
    except Exception as e:
        print(f"❌ Erreur lors de la génération du rapport : {e}")
        sys.exit(1)

# Exportation en PDF via Pandoc
def export_pdf(md_path):
    """Convertit le Markdown en PDF via Pandoc."""
    pdf_path = md_path.replace(".md", ".pdf")
    print(f"[*] Conversion en PDF...")
    try:
        subprocess.run(f"pandoc {md_path} -o {pdf_path}", shell=True, check=True)
        print(f"✅ Rapport PDF généré : {pdf_path}")
    except Exception:
        print("⚠️ Alerte : Pandoc n'a pas pu générer le PDF. Le rapport Markdown est conservé.")

# Main
if __name__ == "__main__":
    print_banner()
    
    parser = argparse.ArgumentParser(description="nmap-scan : Scanner de port.")
    parser.add_argument("target", help="IP ou domaine à scanner")
    parser.add_argument("-m", "--mode", choices=SCAN_PROFILES.keys(), default="quick", 
                        help="Mode de scan (quick, full, stealth)")
    
    args = parser.parse_args()
    
    # Création du dossier reports si inexistant
    if not os.path.exists("reports"):
        os.makedirs("reports")

    # Workflow
    xml_file = run_nmap(args.target, args.mode)
    md_file = build_report(xml_file, args.target, args.mode)
    export_pdf(md_file)
    
    # Nettoyage
    if os.path.exists(xml_file):
        os.remove(xml_file)
    print(f"\n[+] Travail terminé. Les rapports sont dans le dossier 'reports/'.")