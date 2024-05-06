import pandas as pd
import numpy as np
from neuralforecast.models import NBEATS, NHITS, NBEATSx
from neuralforecast import NeuralForecast
import os
import sys
from pathlib import Path
from dataclasses import dataclass
from src.Forecasting_Stock_Prices.logger import logging
from src.Forecasting_Stock_Prices.exception import CustomException
import copy


class Model_Trainner:
    def __init__(self,df):
        self.df = df
        ''' Creating object of DataIngestionConfig class to provide path to save all artifacts at artifacts folder'''

    def initiate_model_trainning(self, h = 15, input_size = 30):
        logging.info('Model trainning started.')

        try:

            data =copy.deepcopy(self.df)
            data = data.drop(data.index[-1])
            data['ds'] = pd.to_datetime(data['Date'])
            data['unique_id'] = 1
            data['y'] = data['Adj Close']
            data.drop(columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'],axis = 1, inplace = True)
            horizon = h 
            window_size = input_size 
            logging.info('Models training started')
            models =[NBEATS(h = horizon, input_size = window_size),
                    NHITS(h = horizon, input_size = window_size)]
            nf = NeuralForecast(models = models, freq = 'D')
            nf.fit(df=data)
            y_hat_df = nf.predict()
    
            
            logging.info('Models training completed')
            return y_hat_df

        except Exception as e:
            logging.info('Exception occured during Model Training stage.')
            raise CustomException(e,sys) 