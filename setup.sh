#!/bin/bash

echo "🚀 Installation de nmap-scan..."
sudo apt update && sudo apt install -y nmap pandoc texlive-latex-base

mkdir -p reports

chmod +x nmap-scan

echo "✅ Installation terminée ! Utilise './nmap-scan --help' pour commencer et voir les commandes disponibles."