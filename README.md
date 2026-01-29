# nmap-scan
nmap-scan est un petit outil développé en Python visant à simplifier l’exécution de scans Nmap et à générer automatiquement des rapports au format Markdown.

## Installation de l'outil 
Avant la première utilisation, il est nécessaire d’exécuter le script de configuration afin d’installer Nmap et de configurer les permissions requises.

```
git clone https://github.com/Th1sma/nmap-scan.git
cd nmap-scan
chmod +x setup.sh
./setup.sh
```

## Fonctionnalités
- **Rapports automatisés :** Conversion des sorties de Nmap en rapport Markdown.
- **Analyse de vulnérabilités :** Extraction ciblée des résultats des scripts NSE (Nmap Scripting Engine).
- **Profils de scan variés :** Choix entre scans rapides, complets ou orientés vulnérabilités.
- **Gestion des fichiers :** Création automatique du répertoire `reports/` et suppression des fichiers temporaires.

## Utilisation 
```
./nmap-scan -m <MODE> <IP_CIBLE> 
```

### Modes disponibles : 
| Mode      | Description                                                        | Commandes Nmap  |
| --------- | ------------------------------------------------------------------ | --------------- |
| `quick`   | Scan standard des 1000 ports TCP                                   | `-sS -sV -sC...`|
| `full`    | Scan exhaustif (65535 ports TCP/UDP), détection d’OS...            | `-p- -A...`     |
| `stealth` | Reconnaissance discrète (scan SYN, fragmentation, vitesse réduite) | `-sS -Pn -f`    |
| `audit`   | Recherche active de vulnérabilités et d’exploits connus            | `--script vuln...`|

