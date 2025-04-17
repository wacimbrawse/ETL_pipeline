import pandas as pd
import logging
from Class_DataCleaner import DataCleaner 

class TransactionProcessor:

    # The constructor method (__init__)
    def __init__(self, df_valid, df_supp):
        self.attribut1 = df_valid
        self.attribut1 = df_supp
        logging.info(f"TransactionProcessor initialisé avec le data frame Retail qui contient {df_valid.shape[0]} lignes et {df_valid.shape[1]} colonnes et le dataframe Supplier qui contient  {df_supp.shape[0]} lignes et {df_supp.shape[1]} colonnes.\n")

    """
    Function to calculate total amount
    In : df_valid data frame
    Out : df_valid data frame with new column Total Amount
    """
    def calculate_total_amount(self,df_valid):

        # Add new column TotalAmount
        df_valid["TotalAmount"] = df_valid["Quantity"] * df_valid["UnitPrice"]

        logging.info("Nouvelle colonne ajoutée 'TotalAmount'.\n")

        return df_valid
    
    """
    Function to calculate total amount
    In : df_valid data frame
    Out : df_grouped data frame with sum of transactions for each country
    """
    def group_by_country(self, df_valid):

        # Calculate sum of transaction for each country
        df_grouped = df_valid.groupby("Country", as_index=False)["TotalAmount"].sum()

        logging.info("Somme totale des montants des transactions pour chaque pays.\n")
        print(df_grouped)
        return df_grouped
    
    """
    Function to calculate monthly statistiques
    In : df_valid data frame
    Out : df_grouped data frame with sum of transactions and Quantity for each month
    """
    def aggregate_monthly_date(self, df_valid):

        # Group by year and month TotalAmount and Quantity
        df_agg_m = df_valid.groupby(pd.Grouper(key="InvoiceDate", freq="ME"))[["TotalAmount", "Quantity"]].sum()

        logging.info("Somme totale des montants des transactions et quantité par numéro de facture.\n")
        print(df_agg_m,"\n")

        return df_agg_m
    
    """
    Function to calculate statistiques
    In : df_valid data frame
    """
    def calcul_stat_data(self, df_valid):

        # Filter for France
        df_fr = df_valid[df_valid["Country"] == "France"]

        # Calculate sum of transaction for each country
        df_grouped_fr = df_fr.groupby("Description", as_index=False)["TotalAmount"].sum()
        df_grouped_fr = df_grouped_fr.sort_values(by="TotalAmount", ascending=False)

        # Display the product with the highest earnings
        top_product = df_grouped_fr.iloc[0]
        top_product_name = top_product["Description"]

        logging.info(f"Le produit qui a généré le plus de gain en France : {top_product_name} .")

        # Create data frame with new columns Hour
        df_hr = df_valid.copy()
        df_hr["InvoiceDate"] = pd.to_datetime(df_hr["InvoiceDate"])
        df_hr["Hour"] = df_hr["InvoiceDate"].dt.hour

        # Group by Hour 
        df_hourly = df_hr.groupby("Hour", as_index=False).size()

        # Sort by size
        df_hourly = df_hourly.sort_values(by="size", ascending=False)
        busiest_hour = df_hourly.iloc[0]

        # Get the Hour with the highest number of transactions
        peak_hour = busiest_hour["Hour"]
        peak_transactions = busiest_hour["size"]
        

        logging.info(f"L'heure où il y a le plus de transactions est : {peak_hour}h avec {peak_transactions} transactions.\n")

    """
    Function for information on suppliers
    In : df_valid data frame, df_supp
    Out : global_ranking, uk_2011_ranking
    """
    def aggregate_supplier_data(self, df_valid, df_supp):

        # Remove rows with uncancelled transactions
        df_supp = df_supp[~df_supp["InvoiceNo"].str.startswith("C", na=False)]
        logging.info(f"Filtrage des transactions annulées dans le fichier supplier: {len(df_supp)} transactions valides restantes.")


        # Merge dataframes on InvoiceNo
        df_valid.loc[:, "InvoiceNo"] = pd.to_numeric(df_valid["InvoiceNo"], errors="coerce").astype("Int64")
        df_supp.loc[:, "InvoiceNo"] = pd.to_numeric(df_supp["InvoiceNo"], errors="coerce").astype("Int64")
        df_merged = df_valid.merge(df_supp, on="InvoiceNo", how="left")
        logging.info(f"Apres le merge du dataframe Retail et Supplier: {len(df_merged)} lignes dans le dataframe mergé.")


        # Aggregate total sales per supplier
        global_ranking = df_merged.groupby("Fournisseur")["TotalAmount"].sum().reset_index()
        global_ranking = global_ranking.sort_values(by="TotalAmount", ascending=False)
        

        # Filter sales for the year 2011 and "United Kingdom"
        df_merged["InvoiceDate"] = pd.to_datetime(df_merged["InvoiceDate"])
        df_uk_2011 = df_merged[(df_merged["InvoiceDate"].dt.year == 2011) & (df_merged["Country"] == "United Kingdom")]
        logging.info(f"Transactions UK 2011 filtré: {len(df_uk_2011)} lignes trouvées.")
        
        # Aggregate sales for UK in 2011
        uk_2011_ranking = df_uk_2011.groupby("Fournisseur")["TotalAmount"].sum().reset_index()
        uk_2011_ranking = uk_2011_ranking.sort_values(by="TotalAmount", ascending=False)
        if not global_ranking.empty:
            logging.info(f"Classement global calculé. Meilleur fournisseur : {global_ranking.iloc[0]['Fournisseur']} avec {global_ranking.iloc[0]['TotalAmount']:.2f} en ventes. \n")

        return global_ranking, uk_2011_ranking
    

    """
    Function for aggregate world data
    In : df_valid data frame, country_continent_mapping, df
    Out : continent_sales, cancelled_operations
    """
    def aggregate_world_data(self, df_valid, country_continent_mapping, df):
        
    
        # Add a “Continent” column by mapping countries
        df["Continent"] = df["Country"].map(country_continent_mapping).fillna("Unknown")
        logging.info("Ajout de la colonne Continent terminé.")
    
        # Calculation of total sales by continent
        df["TotalSales"] = df["Quantity"] * df["UnitPrice"]
        continent_sales = df.groupby("Continent")["TotalSales"].sum().reset_index()
        continent_sales = continent_sales.sort_values(by="TotalSales", ascending=False)
        logging.info("Classement des continents selon les dépenses terminé.")
    
        # Identify the continent with the most cancelled operations
        df["IsCancelled"] = df["InvoiceNo"].astype(str).str.startswith("C")
        cancelled_operations = df[df["IsCancelled"]].groupby("Continent")["InvoiceNo"].count().reset_index()
        cancelled_operations = cancelled_operations.sort_values(by="InvoiceNo", ascending=False)
    
        if not cancelled_operations.empty:
            worst_continent = cancelled_operations.iloc[0]["Continent"]
            worst_count = cancelled_operations.iloc[0]["InvoiceNo"]
            logging.info(f"Le continent avec le plus d'opérations annulées est {worst_continent} avec {worst_count} annulations.\n")
    
        return continent_sales, cancelled_operations