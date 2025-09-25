import pandas as pd
import numpy as np

class DataCleaner:
    @staticmethod
    def clean_dataset(df):
        """Limpeza básica do dataset"""
        df = df.drop_duplicates()
        df = df.dropna()
        df = df.reset_index(drop=True)
        return df
    
    @staticmethod
    def handle_missing_values(df, strategy='mean'):
        """Tratamento de valores missing"""
        if strategy == 'mean':
            return df.fillna(df.mean())
        elif strategy == 'median':
            return df.fillna(df.median())
        return df