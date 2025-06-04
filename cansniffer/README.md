# Moniteur de Port Série

Cette application permet de se connecter à un port série, de recevoir des trames et de les afficher. Elle utilise PyQt6 pour l'interface graphique et PySerial pour la communication série.

## Fonctionnalités

- Détection automatique des ports série disponibles
- Sélection de la vitesse de communication (baud rate)
- Affichage des données reçues en temps réel
- Possibilité d'enregistrer les données dans un fichier texte
- Interface utilisateur intuitive

## Prérequis

- Python 3.6 ou supérieur
- PyQt6
- PySerial

## Installation

1. Installez les dépendances requises :
   ```
   pip install -r requirements.txt
   ```

2. Lancez l'application avec le fichier batch `run_app.bat` ou directement avec Python :
   ```
   python serial_monitor.py
   ```

## Utilisation

1. Sélectionnez le port série dans la liste déroulante
2. Choisissez la vitesse de communication (baud rate)
3. Cliquez sur "Connecter" pour commencer à recevoir des données
4. Les données reçues s'affichent dans la zone de texte
5. Utilisez les boutons "Effacer" pour nettoyer l'affichage ou "Enregistrer" pour sauvegarder les données dans un fichier
