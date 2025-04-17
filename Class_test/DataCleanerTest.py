import unittest
import pandas as pd
import sys
import os

# Ajouter le dossier parent "Online Retail - Copie (2)" au chemin des modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Maintenant, on peut importer la classe DataCleaner
from Class_DataCleaner import DataCleaner


class TestDataCleaner(unittest.TestCase):

    def setUp(self):
        
        # Initialise a test DataFrame 
        
        data = {
            "InvoiceNo": ["10001", "10002", "C10003", "10004", "10002"],
            "StockCode": ["A", "B", "C", "D", "B"],
            "Description": ["Prod1", "Prod2", "Prod3", "Prod4", "Prod2"],
            "Quantity": [10, 20, -5, 15, 20],
            "InvoiceDate": pd.to_datetime(["2021-07-01", "2021-07-02", "2021-07-03", "2021-07-04", "2021-07-02"]),
            "UnitPrice": [5.0, 10.0, 8.0, 12.0, 10.0],
            "CustomerID": [12345, 67890, None, 54321, 67890],
            "Country": ["France", "UK", "Germany", "France", "UK"]
        }

        # Initialise the constructor
        self.df = pd.DataFrame(data)
        self.cleaner = DataCleaner(self.df)

    def test_remove_duplicates(self):

        # Verify the suppression of duplicates 
        df_clean = self.cleaner.remove_duplicates(self.df)
        self.assertEqual(len(df_clean), 4)  # Il y avait un doublon, donc 5 → 4

    def test_handle_missing_values(self):
        
        # Verify the processing of the missing value
        df_clean = self.cleaner.handle_missing_values(self.df, ["InvoiceNo", "StockCode", "Quantity", "InvoiceDate", "UnitPrice", "CustomerID"])
        # Verify there is no Nan
        self.assertFalse(df_clean.isnull().values.any())
        self.assertEqual(df_clean["CustomerID"].dtype, float)

    def test_filter_valid_transactions(self):
        """
        Checks that cancelled transactions (InvoiceNo beginning with “C”) have been deleted.
        """
        df_valid = self.cleaner.filter_valid_transactions(self.df)
        self.assertFalse(df_valid["InvoiceNo"].str.startswith("C").any())  

if __name__ == "__main__":
    unittest.main()
