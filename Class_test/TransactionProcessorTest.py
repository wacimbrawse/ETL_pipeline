import unittest
import pandas as pd
import sys
import os

# Ajouter le dossier parent "Online Retail - Copie (2)" au chemin des modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Class_TransactionProcessor import TransactionProcessor  # Import de la classe à tester

class TestTransactionProcessor(unittest.TestCase):

    def setUp(self):
        
        # Initialise a test DataFrame 
        data_valid = {
            "InvoiceNo": ["10001", "10002", "10004"],
            "StockCode": ["A", "B", "D"],
            "Description": ["Prod1", "Prod2", "Prod4"],
            "Quantity": [10, 20, 15],
            "InvoiceDate": pd.to_datetime(["2021-07-01", "2021-07-02", "2021-07-04"]),
            "UnitPrice": [5.0, 10.0, 12.0],
            "CustomerID": [12345, 67890, 54321],
            "Country": ["France", "UK", "France"]
        }
        self.df_valid = pd.DataFrame(data_valid)

        data_supp = {
            "InvoiceNo": ["10001", "10002", "10004"],
            "Fournisseur": ["Supplier_A", "Supplier_B", "Supplier_D"]
        }
        self.df_supp = pd.DataFrame(data_supp)

        self.processor = TransactionProcessor(self.df_valid, self.df_supp)

        # Apply calculate_total_amount to ensure column exists
        self.df_valid = self.processor.calculate_total_amount(self.df_valid)

    def test_calculate_total_amount(self):

        # Check that the TotalAmount column has been calculated correctly.
        expected_total = [50.0, 200.0, 180.0]  # Quantity * UnitPrice
        self.assertListEqual(self.df_valid["TotalAmount"].tolist(), expected_total)

    def test_group_by_country(self):
        
        # Checks transaction grouping by country.
        df_grouped = self.processor.group_by_country(self.df_valid)
        self.assertEqual(len(df_grouped), 2)  # France et UK
        self.assertTrue("TotalAmount" in df_grouped.columns)

    def test_aggregate_monthly_date(self):
        
        #Checks that monthly aggregation is working.
        df_monthly = self.processor.aggregate_monthly_date(self.df_valid)
        self.assertEqual(len(df_monthly), 1)  # One month in the ex (Juillet 2021)
        self.assertTrue("TotalAmount" in df_monthly.columns)

    def test_calcul_stat_data(self):
       
        # Check that the calculation of statistics for France works.
        try:
            self.processor.calcul_stat_data(self.df_valid)
            success = True
        except Exception as e:
            print(f"Erreur rencontrée : {e}")
            success = False
        self.assertTrue(success)  # Le test réussit si aucune exception n'est levée


    def test_aggregate_supplier_data(self):
        
        #Checks that supplier aggregation is working.
        global_ranking, _ = self.processor.aggregate_supplier_data(self.df_valid, self.df_supp)
        self.assertEqual(len(global_ranking), 3)  # 3 fournisseurs
        self.assertTrue("TotalAmount" in global_ranking.columns)

    def test_aggregate_world_data(self):
        
        # Check that aggregate_world_data is working
        country_continent_mapping = {
            "United Kingdom": "Europe", "France": "Europe", "Germany": "Europe",
            "UK": "Europe", "Unspecified": "Unknown"
        }

        continent_sales, cancelled_operations = self.processor.aggregate_world_data(self.df_valid, country_continent_mapping, self.df_valid)

        self.assertTrue("TotalSales" in continent_sales.columns)
        self.assertTrue("Continent" in cancelled_operations.columns)



if __name__ == "__main__":
    unittest.main()
