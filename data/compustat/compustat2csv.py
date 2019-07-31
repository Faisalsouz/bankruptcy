import os
import numpy as np
import pandas as pd

# get the path to the code file
code_path = os.path.realpath(__file__)
path = code_path[:-16] # remove the code name
# set the path to the txt file directory
os.chdir(path)


# ----------------------------------------------------------------------
# chunk_1
# ----------------------------------------------------------------------
# read the text file into a dataframe
# take care of the codes' leading zeros by setting data type
data1_raw = pd.read_fwf('chunk_1.rtf', dtype={'gvkey': object})

# make a copy of the raw data, and
# drop the first blank row and reset the index
data1 = data1_raw.drop([0], axis=0).reset_index(drop=True)
# drop the last blank column
data1 = data1.drop(['Unnamed: 8'], axis=1)

# change the header for the fifth column
data1.rename(columns={'Unnamed: 4':'lia'}, inplace=True)

# make another copy of the data for cleaning, and
# drop 5 un-immediately-necessary columns
data1_clean = data1.drop(['datadate', 'fyear', 'conm', 'lia', 'dlrsn'], axis=1)

# add a column to explicitly shows the bankruptcy status
data1_clean['isBankrupt'] = np.where(data1_clean['dldte']=='.', 0, 1)

# make the headers comprehensible
data1_clean.columns = ['Compustat Code', 'Company Name',
                       'Bankruptcy Date', 'isBankrupt']


# ----------------------------------------------------------------------
# chunk_2
# ----------------------------------------------------------------------
# read the text file into a dataframe
# take care of the codes' leading zeros by setting data type
data2_raw = pd.read_fwf('chunk_2.rtf', dtype={'cik': object})

# make a copy of the raw data, and
# drop the first blank row and reset the index
data2 = data2_raw.drop([0], axis=0).reset_index(drop=True)

# make another copy of the data for cleaning, and
# drop 7 un-immediately-necessary columns
data2_clean = data2.drop(['cusip', 'exchg', 'consol', 'indfmt',
                          'datafmt', 'popsrc', 'costat', 'curcd'], axis=1)

# make the headers comprehensible
data2_clean.columns = ['Ticker', 'CIK']


# ----------------------------------------------------------------------
# Merging
# ----------------------------------------------------------------------
# merge two dataframes
data_clean = pd.concat([data1_clean.reset_index(drop=True), data2_clean.\
                        reset_index(drop=True)], axis=1)

# make the final copy, and collapse the repetitive rows,
# with the only reliable unique code
data = data_clean.groupby(['Compustat Code']).max().reset_index()


# ----------------------------------------------------------------------
# Writing
# ----------------------------------------------------------------------
# write dataframe into a csv file
data.to_csv('compustat.csv')

# make a new dataframe of healthy companies
healthy = data[data['isBankrupt'] == 0].reset_index(drop=True)
# drop the 'Bankruptcy Date' and 'isBankrupt' columns
healthy = healthy.drop(['Bankruptcy Date', 'isBankrupt'], axis=1)
# write it into a csv file
healthy.to_csv('list_healthy.csv')
print('\nWe have a list of', len(healthy), 'healthy companies')


# make a new dataframe of bankrupt companies
bankrupt = data[data['isBankrupt'] == 1].reset_index(drop=True)
# drop the 'isBankrupt' column
bankrupt = bankrupt.drop(['isBankrupt'], axis=1)
# write it into a csv file
bankrupt.to_csv('list_bankrupt.csv')
print('\nAnd another list of', len(bankrupt), 'bankrupt companies.')