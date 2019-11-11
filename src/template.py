import pandas as pd
import numpy as np

base_path = '/Users/Anna/Documents/bankruptcy/data/Eikon/'

df_brankrupt = pd.read_csv(base_path+'data_bankrupt_CIK/bankrupt_data1.csv')
df_healthy = pd.read_csv(base_path+'data_healthy_CIK/healthy_chunk01_fields1.csv')

print('\nExample Entry of a healthy company:\n', df_healthy.loc[0])

# TODO: read in textual data
#df_b['Mean Embedding'] = pd.Series(DATA, index=df_b.index)