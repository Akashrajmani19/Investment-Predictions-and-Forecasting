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

    def data_ingestion(self):
        logging.info('Data ingestion started.')

        try:
            # Importing data from data folder
            data_address = self.ticker+".csv"
            path_data = os.path.join('data',data_address)
            df = pd.read_csv(path_data)
            logging.info('Data has been imported from drive')
            df['Date'] = pd.to_datetime(df['Date'])
            


            new_data = yf.download(self.ticker, period = '6mo')
            new_data = new_data.reset_index()
            logging.info('New Data has been imported from drive')


            combined_data = pd.concat([df, new_data])

            # Remove duplicates based on timestamp
            combined_data.drop_duplicates(subset='Date', inplace=True)  # Replace 'timestamp_column' with your actual timestamp column name

            # Sort the combined data based on timestamp
            combined_data.sort_values(by='Date', inplace=True)  # Replace 'timestamp_column' with your actual timestamp column name
            df = combined_data.ffill()
            df.to_csv(path_data)
            logging.info('New data added to original data')
            return df

        except Exception as e:
            logging.info('Exception occured during data ingestion stage.')
            raise CustomException(e,sys) 