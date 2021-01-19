import argparse
import os
import warnings

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelBinarizer, KBinsDiscretizer
from sklearn.preprocessing import PolynomialFeatures
from sklearn.compose import make_column_transformer

from sklearn.exceptions import DataConversionWarning
warnings.filterwarnings(action='ignore', category=DataConversionWarning)

columns = ['Year-Month','Agency Number', 'Agency Name','Cardholder ID', 'Description', 'Amount', 'Vendor', 'Transaction_Date_mm',
           'Transaction_Date_dd', 'Transaction_Date_yy', 'Posted_Date_mm','Posted_Date_dd', 'Posted_Date_yy', 'Merchant Category Code (MCC)', 'MCC_ID', 'Recurring_Label']

def print_shape(df):
    negative_examples, positive_examples = np.bincount(df['Recurring_Label'])
    print('Data shape: {}, {} positive examples, {} negative examples'.format(df.shape, positive_examples, negative_examples))

if __name__=='__main__':
 
    input_data_path = os.path.join('/opt/ml/processing/input', 'PCARD-workshop-raw.csv')
    
    print('Reading input data from {}'.format(input_data_path))
    df = pd.read_csv(input_data_path)
    df.drop(['Posted_Date_yy', 'Transaction_Date_yy','Posted_Date_mm', 'Year-Month','Posted_Date_dd' ,'Vendor', 'Description','Agency Name','Merchant Category Code (MCC)'], axis=1, inplace=True)
    model_data = pd.get_dummies(df)
        
    train_data, validation_data, test_data = np.split(model_data.sample(frac=1, random_state=1729), [int(0.7 * len(model_data)), int(0.9 * len(model_data))])   # Randomly sort the data then split out first 70%, second 20%, and last 10%

    print('Writing train and validation data to csv...')
 
    train_features = pd.concat([train_data['Recurring_Label_Yes'], train_data.drop(['Recurring_Label_No', 'Recurring_Label_Yes'], axis=1)], axis=1)
    validation_features = pd.concat([validation_data['Recurring_Label_Yes'], validation_data.drop(['Recurring_Label_No', 'Recurring_Label_Yes'], axis=1)], axis=1)

    train_output_path = os.path.join('/opt/ml/processing/train', 'trainp.csv')
    validation_output_path = os.path.join('/opt/ml/processing/validation', 'validationp.csv')
    
        
    print('Saving training dataset to {}'.format(train_output_path))
    pd.DataFrame(train_features).to_csv(train_output_path, header=False, index=False)
    
    print('Saving validation dataset to {}'.format(validation_output_path))
    pd.DataFrame(validation_features).to_csv(validation_output_path, header=False, index=False)
