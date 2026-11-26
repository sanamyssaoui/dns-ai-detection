# Détection IA des attaques DNS — Lab Pentest

Laboratoire isolé (Kali / Ubuntu) pour simuler des attaques DNS et les
détecter via un module d'intelligence artificielle ne journalisant que
les vrais positifs.

## Architecture
- VM1 Kali (192.168.56.10) — attaquant
- VM2 Ubuntu (192.168.56.20) — cible + serveur DNS (BIND9) + capture Zeek
- VM3 Ubuntu (192.168.56.30) — moteur de détection IA
- Réseau Host-only isolé (aucun accès Internet)

## Attaques simulées
Reconnaissance (AXFR), DNS flood, tunneling, NXDOMAIN scan, zone walking.

## Chaîne de traitement
dns.log (Zeek) -> parse_dns.py -> features.csv -> label.py -> dataset.csv
-> train.py (Isolation Forest + Random Forest) -> detect.py -> log des vrais positifs

## Résultats
- Classification supervisée : F1-score = 0.92
- Détection : vrais positifs confirmés (recon, flood, tunnel, nxscan)

## Scripts
- scripts/parse_dns.py — extraction des features depuis les logs Zeek
- scripts/label.py — labellisation via attack_schedule.csv
- scripts/train.py — entraînement des modèles
- scripts/detect.py — détection + filtrage des faux positifs

## Auteur
Sana Missaoui
