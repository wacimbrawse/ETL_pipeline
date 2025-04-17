import pandas as pd
import logging
from Class_DataCleaner import DataCleaner  # Import de la classe DataCleaner
from Class_TransactionProcessor import TransactionProcessor  # Import de TransactionProcessor
from source.Dictionnaire_map import country_continent_mapping


# Configuration du logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class ETLPipeline:
    def __init__(self, file_path):
        """
        Initialise l'ETL avec le fichier Excel et les classes nécessaires.
        """
        logging.info("Début du chargement des données...")
        self.df = pd.read_excel(file_path)
        logging.info(f"Fichier {file_path} chargé avec {self.df.shape[0]} lignes et {self.df.shape[1]} colonnes.")

        # Initialisation des classes
        self.cleaner = DataCleaner(self.df)
        self.processor = None  

    def run_pipeline(self):
        
        #Runs the ETL pipeline: Cleaning, transformation and analysis.
        logging.info("Début du pipeline ETL...")

        # Step 1 : cleaning data
        df_no_duplicates = self.cleaner.remove_duplicates(self.df)
        df_clean = self.cleaner.handle_missing_values(df_no_duplicates, ["InvoiceNo", "StockCode", "Quantity", "InvoiceDate", "UnitPrice", "CustomerID"])
        df_valid = self.cleaner.filter_valid_transactions(df_clean)

        logging.info(f"Données nettoyées : {df_valid.shape[0]} transactions valides restantes.\n")

        # Load Supplier file for suppliers
        df_supp = pd.read_csv("source/Supplier.csv")

        # Step 2: Initialize TransactionProcessor with cleaned data
        self.processor = TransactionProcessor(df_valid, df_supp)

        # Step 3: Transaction calculation and analysis
        df_valid = self.processor.calculate_total_amount(df_valid)

        # 3.1 Supplier ranking by sales
        global_ranking, uk_2011_ranking = self.processor.aggregate_supplier_data(df_valid, df_supp)

        # 3.2 monthly statistique
        df_monthly = self.processor.aggregate_monthly_date(df_valid)
        logging.info("Statistiques mensuelles générées.\n")

        # 3.3 Stats of sales
        self.processor.calcul_stat_data(df_valid)  

        # 3.4 Classement des fournisseurs par ventes
        global_ranking, uk_2011_ranking = self.processor.aggregate_supplier_data(df_valid, df_supp)
        logging.info("Classement des fournisseurs terminé.\n")


        # 3.5 Classification of continents by expenditure
        continent_sales, cancelled_operations = self.processor.aggregate_world_data(df_valid, country_continent_mapping, df_valid)

        # Step 4: Save results in parquet
        self.save_as_parquet("cleaned_data.parquet")

        logging.info("Pipeline ETL terminé avec succès !\n")

    def save_as_parquet(self, path):
        """
        Sauvegarde le DataFrame final en format Parquet.
        """
        logging.info(f"Sauvegarde du DataFrame final en fichier Parquet : {path}\n")

        # Convert some columns to str to avoid errors with pyarrow
        self.df["InvoiceNo"] = self.df["InvoiceNo"].astype(str)  
        self.df["StockCode"] = self.df["StockCode"].astype(str)
        self.df["Description"] = self.df["Description"].astype(str)

        # Check types before saving
        logging.info(f"Types des colonnes avant sauvegarde :\n{self.df.dtypes}\n")

        #self.df.to_parquet(path, index=False)
        logging.info("Fichier Parquet sauvegardé avec succès !\n")




# Start the ETL pipeline
if __name__ == "__main__":
    etl = ETLPipeline("source/Online Retail.xlsx")
    etl.run_pipeline()
