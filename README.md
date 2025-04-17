🛍️ Projet ETL - Analyse de Données Transactionnelles (POO - Python)
📌 Description du Projet
Ce projet a pour objectif de concevoir et développer un pipeline ETL (Extract, Transform, Load) orienté objet en Python, basé sur un jeu de données transactionnelles fourni par l'UCI Machine Learning Repository.
Le dataset contient des informations de ventes en ligne pour une entreprise britannique spécialisée dans la vente de cadeaux.

Le pipeline s'articule autour de trois grandes classes responsables du nettoyage, du traitement des transactions et de l'orchestration complète du processus ETL, avec un enregistrement final au format Parquet.

📁 Structure du Projet
bash
Copier
Modifier
ETL_Project/
│
├── data/                      # Contient les fichiers source (transactions, fournisseurs, mapping continent)
│
├── src/
│   ├── data_cleaner.py        # Classe DataCleaner
│   ├── transaction_processor.py  # Classe TransactionProcessor
│   ├── etl_pipeline.py        # Classe ETLPipeline
│
├── tests/
│   ├── data_cleaner_test.py   # Tests unitaires pour DataCleaner
│   ├── transaction_processor_test.py # Tests unitaires pour TransactionProcessor
│
├── output/                    # Contiendra les fichiers générés (.parquet)
│
├── README.md
└── requirements.txt
🧠 Fonctionnalités Principales
🔹 DataCleaner
Classe responsable du nettoyage du DataFrame :

Suppression des doublons

Traitement des valeurs manquantes

Filtrage des transactions valides (hors annulations)

🔹 TransactionProcessor
Classe métier dédiée à l’analyse des transactions :

Calcul du montant total de chaque transaction

Agrégation par pays et par mois

Analyse des heures de pointe des ventes

Classement des produits les plus rentables par pays

Traitement des fournisseurs et leur performance

Analyse continentale via un mapping externe

🔹 ETLPipeline
Classe d’orchestration du projet ETL :

Exécution de bout en bout du pipeline (nettoyage → transformation → enrichissement)

Sauvegarde finale au format Parquet

🧪 Tests Unitaires
Des tests unitaires ont été développés pour garantir la robustesse du code.
Chaque classe fonctionnelle dispose de son propre fichier de test :

data_cleaner_test.py

transaction_processor_test.py

Ces tests valident le bon comportement de chaque méthode, ainsi que la gestion des cas particuliers (valeurs manquantes, formats inattendus, etc.).

📝 Exigences Techniques
Python 3.9+

Pandas

Pytest

PyArrow

Installe les dépendances avec :

bash
Copier
Modifier
pip install -r requirements.txt
🚀 Exécution du Pipeline
python
Copier
Modifier
from src.etl_pipeline import ETLPipeline

pipeline = ETLPipeline("data/transactions.csv", "data/suppliers.csv", "data/country_continent_mapping.csv")
pipeline.run_pipeline()
pipeline.save_as_parquet("output/transactions_cleaned.parquet")
📊 Résultats Attendues
Un DataFrame enrichi, prêt pour l’analyse exploratoire ou la modélisation.

Des insights business : pays les plus dépensiers, heures de ventes les plus actives, fournisseurs les plus performants.

Un pipeline modulaire, maintenable et réutilisable.

📚 Source de Données
Jeu de données :
UCI Machine Learning Repository
Online Retail Data Set

👨‍💻 Auteur
Développé par TonNom dans le cadre d’un projet de data engineering orienté objet.

Tu veux que je le traduise aussi en anglais ou tu préfères tout en français pour l’instant ?