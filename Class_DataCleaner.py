import pandas as pd
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class DataCleaner:

    # The constructor method (__init__)
    def __init__(self, df):
        self.attribut1 = df
        logging.info(f"DataCleaner initialisé avec le data frame Retail qui contient {df.shape[0]} lignes et {df.shape[1]} colonnes.\n")
       
    """
    Function to remove duplicates
    In : df dataframe with duplicates
    Out : df_rd dataframe without duplicates
    """
    def remove_duplicates(self, df):

        # Copy of the dataframe
        df_rd = df.copy()

        # Number of initial rows
        initial_rows = df_rd.shape[0]

        # Remove duplicate rows from the DataFrame
        df_rd = df_rd.drop_duplicates()

        # Number of removed rows
        removed_rows = initial_rows - df_rd.shape[0]
        
        logging.info(f"Suppression des doublons du fichier retail: {removed_rows} lignes supprimées.\n")

        return df_rd
    
    """
    # Function to remove missing value
    # In : df_rd (data frame without duplicates) with missing value, 
    #      important_columns : list of important columns
    # Out : df_clean dataframe without missing value
    """
    def handle_missing_values(self, df_rd, important_columns):

        # Copy of the dataframe
        df_clean= df_rd.copy()

        # Number of initial rows
        initial_rows = df_clean.shape[0] 

        # Remove rows which contains NaN in important columns from the DataFrame
        df_clean = df_clean.dropna(subset=important_columns)

        # Number of removed rows
        removed_rows = initial_rows - df_clean.shape[0]
        
        logging.info(f"Suppression des lignes qui contiennet des valuer vulles sur les colonnes importantes du fichier retail: {removed_rows} lignes supprimées.")

        # Remplace nan values in non important columns
        df_clean = df_clean.fillna("unknown")

        logging.info("Les Valeurs nulles dans les colonnes non importantes sont remplacées par 'unknown' dans le fichier retail.\n")
        

        return df_clean
    

    """
    # Function to keep only uncancelled transactions
    # In : df_clean dataframe without missing value
    # Out : df_valid dataframe with only valid transaction
    """
    def filter_valid_transactions(self,df_clean):

        # Copy of the dataframe
        df_valid = df_clean.copy()

        # Transform to date type
        df_valid["InvoiceDate"] = pd.to_datetime(df_valid["InvoiceDate"])

        # Number of initial rows
        initial_rows = df_valid.shape[0] 

        # Remove rows with uncancelled transactions
        df_valid = df_valid[~df_valid["InvoiceNo"].str.startswith("C", na=False)]

        # Number of removed rows
        removed_rows = initial_rows - df_valid.shape[0]
        
        logging.info(f"Filtrage des transactions annulées dans le fichier retail: {removed_rows} lignes supprimées.\n")


        return df_valid