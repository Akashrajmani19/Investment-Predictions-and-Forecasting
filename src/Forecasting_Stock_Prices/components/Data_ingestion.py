import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path
from dataclasses import dataclass

from src.Forecasting_Stock_Prices.logger import logging
from src.Forecasting_Stock_Prices.exception import CustomException
import yfinance as yf
import win32com.shell




class Data_Caller:
    def __init__(self,ticker):
        self.ticker = ticker
        ''' Creating object of DataIngestionConfig class to provide path to save all artifacts at artifacts folder'''
        self.ingestion_config = DataIngestionConfig()

    def data_ingestion(self):
        logging.info('Data ingestion started.')

        try:
            # Importing data from data folder
            data_address = self.ticker+".csv"
            path_data = os.path.join('data',data_address)
            df = pd.read_csv(path_data)
            logging.info('Data has been imported from drive')
            df['Date'] = pd.to_datetime(df['Date'])
            df.set_index('Date')


            new_data = yf.download("MSFT", period = '1mo')
            logging.info('New Data has been imported from drive')

            duplicates = pd.merge(df, new_data, how='inner')
            non_duplicates = new_data[~new_data.index.isin(duplicates.index)]
            df = pd.concat([df, non_duplicates], ignore_index=True)

            df.to_csv(path_data)
            logging.info('New data added to original data')
            return df

        except Exception as e:
            logging.info('Exception occured during data ingestion stage.')
            raise CustomException(e,sys) 