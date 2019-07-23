import os
import numpy as np
import pandas as pd

# get the path to the code file
code_path = os.path.realpath(__file__)
path = code_path[:-16] # remove the code name
# set the path to the txt file directory
os.chdir(path)

# read the text file into a dataframe
# drop the first two blank rows and
# use the third one as the header
data_raw = pd.read_fwf('raw_data.txt', header=3)

# make a copy of the raw data, and
# drop one more blank row and reset the index
data = data_raw.drop([0], axis=0).reset_index(drop=True)

# change the header for the fifth column
data.rename(columns={'Unnamed: 4':'lia'}, inplace=True)

# make another copy of the data for cleaning, and
# drop four un-immediately-necessary columns
data_clean = data.drop(['datadate', 'fyear', 'conm', 'lia'], axis=1)

# collapse the repetitive rows
data_clean = data_clean.groupby(['gvkey']).max().reset_index()

# add a column to explicitly shows the bankruptcy status
data_clean['isBankrupt'] = np.where(data_clean['dldte']=='.', 0, 1)

# replace the remained NaNs in the dataframe
data_clean['dlrsn'].fillna('00', inplace = True)

# make the headers comprehensible
data_clean.columns = ['Gov. Code', 'Company Name', 'Bankruptcy Date',
                      'Bankruptcy Reason', 'isBankrupt']

# write dataframe into a csv file
data_clean.to_csv('data_clean.csv')
