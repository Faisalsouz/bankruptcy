import os
import pandas as pd
import pickle

# read the Compustat-extracted lists of
# healthy and bankrupt companies
# ----------------------------------------------------------------------
# set the path for reading the Compustat lists
path = 'D:\\studyproject\\bankruptcy\\data\\compustat\\' # for win decomment this line
# path = '/Users/user/Documents/Bankruptcy/bankruptcy/data/compustat/' # for mac decomment this line

# set the path for reading the csv files
# --------------- for win ---------------
path_b = 'convertedCSVfiles\\bankrupt\\'
path_h = 'convertedCSVfiles\\healthy\\'
# --------------- for mac ---------------
# path_b = './convertedCSVfiles/bankrupt/'
# path_h = './convertedCSVfiles/healthy/'
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# 1. Merging Bankrupt Companies Data
# ----------------------------------------------------------------------

# read the bankrupt list
bankrupt = pd.read_csv(str(path + 'list_bankrupt.csv'), dtype=object)

# remove the glitch column
bankrupt = bankrupt.drop(['Unnamed: 0'], axis=1)


# ----------------------------------------------------------------------
# work with ISIN codes converted from CUSIP
# ----------------------------------------------------------------------
# set the path

# read the bankrupt companies CUSIP to ISIN convert-table csv file
bankrupt_csp2isn = pd.read_csv(path_b + 'bankrupt_csp2isn.csv', dtype=object)
bankrupt_csp2isn.rename(columns={'Unnamed: 0':'CUSIP'}, inplace=True)

# check the compatibility of CUSIP columns in two dataframe, before merging
for i in range(len(bankrupt)):
    if bankrupt.iloc[i][5] != bankrupt_csp2isn.iloc[i][0]:
        print('WARNING: There is inconsistency at row:', i)


# ----------------------------------------------------------------------
## 1.1. ISIN
# ----------------------------------------------------------------------
# work with ISIN codes converted from Ticker
# ----------------------------------------------------------------------
# read the bankrupt companies Ticker to ISIN convert-table csv file
bankrupt_tic2isn = pd.read_csv(path_b + 'bankrupt_tic2isn.csv', dtype=object)
bankrupt_tic2isn.rename(columns={'Unnamed: 0':'Ticker'}, inplace=True)

# check the compatibility of Ticker columns in two dataframe, before merging
for i in range(len(bankrupt)):
    if bankrupt.iloc[i][4] != bankrupt_tic2isn.iloc[i][0]:
        print('WARNING: There is inconsistency at row:', i)



# ----------------------------------------------------------------------
# attach the ISIN columns to the bankrupt dataframe
bankrupt['csp2ISIN'] = bankrupt_csp2isn['ISIN']
bankrupt['tic2ISIN'] = bankrupt_tic2isn['ISIN']
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# merge the two ISIN columns
# ----------------------------------------------------------------------
# add a single column for ISIN, and
bankrupt['ISIN'] = ''
# a column to indicate there was inconsistency in converting symbols
bankrupt['ISINc'] = ''

for index, row in bankrupt.iterrows():
    # in case of conflicts
    if row['csp2ISIN'] != row['tic2ISIN']:

        # in case csp2ISN is NAN
        if row['csp2ISIN'] != row['csp2ISIN']:
            # in case both are NAN values
            if row['tic2ISIN'] != row['tic2ISIN']:
                # enter NAN as the ISIN value
                row['ISIN'] = row['csp2ISIN']
                # but no real inconsistency
                row['ISINc'] = 0

            # in case only csp2ISIN is NAN
            else:
                # fill ISIN with tic2ISIN
                row['ISIN'] = row['tic2ISIN']
                # and mark it as an inconsistency
                row['ISINc'] = 1

        # in case csp2ISIN is non-NAN value
        else:
            # in case tic2ISIN is NAN
            if row['tic2ISIN'] != row['tic2ISIN']:
                # fill ISIN with csp2ISIN
                row['ISIN'] = row['csp2ISIN']
                # and mark it as an inconsistency
                row['ISINc'] = 1

            # in case both are non-NAN values
            else:
                # fill ISIN with both
                row['ISIN'] = str(row['csp2ISIN']) + ' - ' + str(row['tic2ISIN'])
                # and mark it as a serious inconsistency
                row['ISINc'] = 3

    # in case of consistency
    else:
        # fill ISIN with the value
        row['ISIN'] = row['csp2ISIN']
        # and it's consistent
        row['ISINc'] = 0


# check the number of inconsistency cases
inconsistency = len(bankrupt) - bankrupt['ISINc'].value_counts()[0]
print(inconsistency, 'case(s) of inconsistency!')
# check for serious cases of inconsistency
if 3 in bankrupt['ISINc'].value_counts().index:
    print(bankrupt['ISINc'].value_counts()[3], 'are serious!')
else:
    print('But none is serious.')

# check the number of successful conversion to RIC
print('\nAnd now we have', len(bankrupt) - bankrupt['ISIN'].isna().sum(), 'bankrupt company with ISIN code.')

# remove the extra *ISIN columns
bankrupt = bankrupt.drop(['csp2ISIN', 'tic2ISIN'], axis=1)

# ----------------------------------------------------------------------
## 1.2. RIC
# ----------------------------------------------------------------------
# work with RIC codes converted from CUSIP
# ----------------------------------------------------------------------
# read the bankrupt companies CUSIP to RIC convert-table csv file
bankrupt_csp2ric = pd.read_csv(path_b + 'bankrupt_csp2ric.csv', dtype=object)
bankrupt_csp2ric.rename(columns={'Unnamed: 0':'CUSIP'}, inplace=True)

# check the compatibility of CUSIP columns in two dataframe, before merging
for i in range(len(bankrupt)):
    if bankrupt.iloc[i][5] != bankrupt_csp2ric.iloc[i][0]:
        print('WARNING: There is inconsistency at row:', i)


# ----------------------------------------------------------------------
# work with RIC codes converted from Ticker
# ----------------------------------------------------------------------
# read the bankrupt companies Ticker to ISIN convert-table csv file
bankrupt_tic2ric = pd.read_csv(path_b + 'bankrupt_tic2ric.csv', dtype=object)
bankrupt_tic2ric.rename(columns={'Unnamed: 0':'Ticker'}, inplace=True)

# check the compatibility of Ticker columns in two dataframe, before merging
for i in range(len(bankrupt)):
    if bankrupt.iloc[i][4] != bankrupt_tic2ric.iloc[i][0]:
        print('WARNING: There is inconsistency at row:', i)


# ----------------------------------------------------------------------
# attach the RIC columns to the bankrupt dataframe
bankrupt['csp2RIC'] = bankrupt_csp2ric['RIC']
bankrupt['tic2RIC'] = bankrupt_tic2ric['RIC']
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# merge the two RIC columns
# ----------------------------------------------------------------------
# add a single column for RIC, and
bankrupt['RIC'] = ''
# a column to indicate there was inconsistency in converting symbols
bankrupt['RICc'] = ''

for index, row in bankrupt.iterrows():
    # in case of conflicts
    if row['csp2RIC'] != row['tic2RIC']:

        # in case csp2RIC is NAN
        if row['csp2RIC'] != row['csp2RIC']:
            # in case both are NAN values
            if row['tic2RIC'] != row['tic2RIC']:
                # enter NAN as the RIC value
                row['RIC'] = row['csp2RIC']
                # but no real inconsistency
                row['RICc'] = 0

            # in case only csp2RIC is NAN
            else:
                # fill RIC with tic2RIC
                row['RIC'] = row['tic2RIC']
                # and mark it as an inconsistency
                row['RICc'] = 1

        # in case csp2RIC is non-NAN value
        else:
            # in case tic2RIC is NAN
            if row['tic2RIC'] != row['tic2RIC']:
                # fill RIC with csp2RIC
                row['RIC'] = row['csp2RIC']
                # and mark it as an inconsistency
                row['RICc'] = 1

            # in case both are non-NAN values
            else:
                # fill RIC with both
                row['RIC'] = str(row['csp2RIC']) + ' - ' + str(row['tic2RIC'])
                # and mark it as a serious inconsistency
                row['RICc'] = 3

    # in case of consistency
    else:
        # fill RIC with the value
        row['RIC'] = row['csp2RIC']
        # and it's consistent
        row['RICc'] = 0


# check the number of inconsistency cases
inconsistency = len(bankrupt) - bankrupt['RICc'].value_counts()[0]
print(inconsistency, 'case(s) of inconsistency!')
# check for serious cases of inconsistency
if 3 in bankrupt['RICc'].value_counts().index:
    print(bankrupt['RICc'].value_counts()[3], 'are serious!')
else:
    print('But none is serious.')

# check the number of successful conversion to RIC
print('\nAnd now we have', len(bankrupt) - bankrupt['RIC'].isna().sum(), 'bankrupt company with RIC code.')

# remove the extra *ISIN columns
bankrupt = bankrupt.drop(['csp2RIC', 'tic2RIC'], axis=1)



# ----------------------------------------------------------------------
# 2. Merging Healthy Companies Data
# ----------------------------------------------------------------------
# read the healthy list
healthy = pd.read_csv(str(path + 'list_healthy.csv'), dtype=object)

# remove the glitch column
healthy = healthy.drop(['Unnamed: 0'], axis=1)

# ----------------------------------------------------------------------
## 2.1. ISIN
# ----------------------------------------------------------------------
# read and merge ISIN codes converted from CUSIP
# ----------------------------------------------------------------------
# read the healthy companies CUSIP to ISIN conversion csv files
healthy_csp2isn = [pd.read_csv(path_h + 'healthy_csp2isn{}.csv'.format(i+1), dtype=object) for i in range(6)]
# merge them
healthy_csp2isn = pd.concat([healthy_csp2isn[i] for i in range(6)])
# clean the resulted dataframe
healthy_csp2isn.rename(columns={'Unnamed: 0':'CUSIP', 'ISIN':'csp2ISIN'}, inplace=True)
# and remove that extra uninformative column
healthy_csp2isn = healthy_csp2isn.drop(['error'], axis=1)
# first-merge CUSIP-to-ISIN dataframe with the healthy list
healthy = healthy.merge(healthy_csp2isn, how='left', on=['CUSIP'])

# ----------------------------------------------------------------------
# read and merge ISIN codes converted from Ticker
# ----------------------------------------------------------------------
# read the healthy companies Ticker to ISIN conversion csv files
healthy_tic2isn = [pd.read_csv(path_h + 'healthy_tic2isn{}.csv'.format(i+1), dtype=object) for i in range(6)]
# merge them
healthy_tic2isn = pd.concat([healthy_tic2isn[i] for i in range(6)])
# clean the resulted dataframe
healthy_tic2isn.rename(columns={'Unnamed: 0':'Ticker', 'ISIN':'tic2ISIN'}, inplace=True)
# and remove that extra uninformative column
healthy_tic2isn = healthy_tic2isn.drop(['error'], axis=1)
# second merge Ticker-to-ISIN dataframe with the first-merged healthy list
healthy = healthy.merge(healthy_tic2isn, on=['Ticker'], how='left')

# ----------------------------------------------------------------------



# ----------------------------------------------------------------------
# merge the two ISIN columns
# ----------------------------------------------------------------------
# add a single column for ISIN, and
healthy['ISIN'] = ''
# a column to indicate there was inconsistency in converting symbols
healthy['ISINc'] = ''

for index, row in healthy.iterrows():
    # in case of conflicts
    if row['csp2ISIN'] != row['tic2ISIN']:

        # in case csp2ISN is NAN
        if row['csp2ISIN'] != row['csp2ISIN']:
            # in case both are NAN values
            if row['tic2ISIN'] != row['tic2ISIN']:
                # enter NAN as the ISIN value
                row['ISIN'] = row['csp2ISIN']
                # but no real inconsistency
                row['ISINc'] = 0

            # in case only csp2ISIN is NAN
            else:
                # fill ISIN with tic2ISIN
                row['ISIN'] = row['tic2ISIN']
                # and mark it as an inconsistency
                row['ISINc'] = 1

        # in case csp2ISIN is non-NAN value
        else:
            # in case tic2ISIN is NAN
            if row['tic2ISIN'] != row['tic2ISIN']:
                # fill ISIN with csp2ISIN
                row['ISIN'] = row['csp2ISIN']
                # and mark it as an inconsistency
                row['ISINc'] = 1

            # in case both are non-NAN values
            else:
                # fill ISIN with both
                row['ISIN'] = str(row['csp2ISIN']) + ' - ' + str(row['tic2ISIN'])
                # and mark it as a serious inconsistency
                row['ISINc'] = 3

    # in case of consistency
    else:
        # fill ISIN with the value
        row['ISIN'] = row['csp2ISIN']
        # and it's consistent
        row['ISINc'] = 0


# check the number of inconsistency cases
inconsistency = len(healthy) - healthy['ISINc'].value_counts()[0]
print(inconsistency, 'case(s) of inconsistency!')
# check for serious cases of inconsistency
if 3 in healthy['ISINc'].value_counts().index:
    print(healthy['ISINc'].value_counts()[3], 'are serious!')
else:
    print('But none is serious.')

# check the number of successful conversion to ISIN
print('\nAnd now we have', len(healthy) - healthy['ISIN'].isna().sum(), 'bankrupt company with ISIN code.')


# remove the extra *ISIN columns
healthy = healthy.drop(['csp2ISIN', 'tic2ISIN'], axis=1)



# ----------------------------------------------------------------------
## 2.2. RIC

# ----------------------------------------------------------------------
# read and merge RIC codes converted from CUSIP
# ----------------------------------------------------------------------
# read the healthy companies CUSIP to RIC convert-table csv files
healthy_csp2ric = [pd.read_csv(path_h + 'healthy_csp2ric{}.csv'.format(i+1), dtype=object) for i in range(6)]
# merge them
healthy_csp2ric = pd.concat([healthy_csp2ric[i] for i in range(6)])
# clean the resulted dataframe
healthy_csp2ric.rename(columns={'Unnamed: 0':'CUSIP', 'RIC':'csp2RIC'}, inplace=True)
# and remove that extra uninformative column
healthy_csp2ric = healthy_csp2ric.drop(['error'], axis=1)
# first-merge CUSIP-to-RIC dataframe with the healthy list
healthy = healthy.merge(healthy_csp2ric, how='left', on=['CUSIP'])

# ----------------------------------------------------------------------
# read and merge RIC codes converted from Ticker
# ----------------------------------------------------------------------
# read the healthy companies Ticker to RIC conversion csv files
healthy_tic2ric = [pd.read_csv(path_h + 'healthy_tic2ric{}.csv'.format(i+1), dtype=object) for i in range(6)]
# merge them
healthy_tic2ric = pd.concat([healthy_tic2ric[i] for i in range(6)])
# clean the resulted dataframe
healthy_tic2ric.rename(columns={'Unnamed: 0':'Ticker', 'RIC':'tic2RIC'}, inplace=True)
# and remove that extra uninformative column
healthy_tic2ric = healthy_tic2ric.drop(['error'], axis=1)
# second merge Ticker-to-RIC dataframe with the first-merged healthy list
healthy = healthy.merge(healthy_tic2ric, on=['Ticker'], how='left')
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# merge the two RIC columns
# ----------------------------------------------------------------------
# add a single column for RIC, and
healthy['RIC'] = ''
# a column to indicate there was inconsistency in converting symbols
healthy['RICc'] = ''

for index, row in healthy.iterrows():
    # in case of conflicts
    if row['csp2RIC'] != row['tic2RIC']:

        # in case csp2RIC is NAN
        if row['csp2RIC'] != row['csp2RIC']:
            # in case both are NAN values
            if row['tic2RIC'] != row['tic2RIC']:
                # enter NAN as the ISIN value
                row['RIC'] = row['csp2RIC']
                # but no real inconsistency
                row['RICc'] = 0

            # in case only csp2RIC is NAN
            else:
                # fill RIC with tic2RIC
                row['RIC'] = row['tic2RIC']
                # and mark it as an inconsistency
                row['RICc'] = 1

        # in case csp2RIC is non-NAN value
        else:
            # in case tic2RIC is NAN
            if row['tic2RIC'] != row['tic2RIC']:
                # fill RIC with csp2RIC
                row['RIC'] = row['csp2RIC']
                # and mark it as an inconsistency
                row['RICc'] = 1

            # in case both are non-NAN values
            else:
                # fill RIC with both
                row['RIC'] = str(row['csp2RIC']) + ' - ' + str(row['tic2RIC'])
                # and mark it as a serious inconsistency
                row['RICc'] = 3

    # in case of consistency
    else:
        # fill RIC with the value
        row['RIC'] = row['csp2RIC']
        # and it's consistent
        row['RICc'] = 0


# check the number of inconsistency cases
inconsistency = len(healthy) - healthy['RICc'].value_counts()[0]
print(inconsistency, 'case(s) of inconsistency!')
# check for serious cases of inconsistency
if 3 in healthy['RICc'].value_counts().index:
    print(healthy['RICc'].value_counts()[3], 'are serious!')
else:
    print('But none is serious.')

# check the number of successful conversion to RIC
print('\nAnd now we have', len(healthy) - healthy['RIC'].isna().sum(), 'bankrupt company with RIC code.')


# remove the extra *RIC columns
healthy = healthy.drop(['csp2RIC', 'tic2RIC'], axis=1)



# ----------------------------------------------------------------------
# save the final lists of companies
# ----------------------------------------------------------------------
# save the final csv files of bankrupt and healthy companies
bankrupt.to_csv('final_bankrupt_list.csv')
healthy.to_csv('final_healthy_list.csv')


# ----------------------------------------------------------------------
# extract and save 4 lists of RICs and ISINs for bankrupt and healthy companies
# ----------------------------------------------------------------------

# create a folder to save the list-pickles
os.mkdir('Lists')

# ISIN list for bankrupt companies
bankrupt_ISIN = bankrupt.ISIN[bankrupt['ISINc'] != 3].dropna().to_list()
# handle serious conflict cases which include more than one code
for index, row in bankrupt.iterrows():
    if row['ISINc'] == 3:
        bankrupt_ISIN.append(row['ISIN'][:row['ISIN'].find(' - ')])
        bankrupt_ISIN.append(row['ISIN'][row['ISIN'].find(' - ') + 3:])
# and save the list
with open('Lists/bankrupt_ISIN.txt', 'wb') as f:
    pickle.dump(bankrupt_ISIN, f)


# create RIC list for bankrupt companies
bankrupt_RIC = bankrupt.RIC[bankrupt['RICc'] != 3].dropna().to_list()
# handle serious conflict cases which include more than one code
for index, row in bankrupt.iterrows():
    if row['RICc'] == 3:
        bankrupt_RIC.append(row['RIC'][:row['RIC'].find(' - ')])
        bankrupt_RIC.append(row['RIC'][row['RIC'].find(' - ') + 3:])
# and save the list
with open('Lists/bankrupt_RIC.txt', 'wb') as f:
    pickle.dump(bankrupt_RIC, f)


# ISIN list for healthy companies
healthy_ISIN = healthy.ISIN[healthy['ISINc'] != 3].dropna().to_list()
# handle serious conflict cases which include more than one code
for index, row in healthy.iterrows():
    if row['ISINc'] == 3:
        healthy_ISIN.append(row['ISIN'][:row['ISIN'].find(' - ')])
        healthy_ISIN.append(row['ISIN'][row['ISIN'].find(' - ') + 3:])
# and save the list
with open('Lists/healthy_ISIN.txt', 'wb') as f:
    pickle.dump(healthy_ISIN, f)


# RIC list for healthy companies
healthy_RIC = healthy.RIC[healthy['RICc'] != 3].dropna().to_list()
# handle serious conflict cases which include more than one code
for index, row in healthy.iterrows():
    if row['RICc'] == 3:
        healthy_RIC.append(row['RIC'][:row['RIC'].find(' - ')])
        healthy_RIC.append(row['RIC'][row['RIC'].find(' - ') + 3:])
# and save the list
with open('Lists/healthy_RIC.txt', 'wb') as f:
    pickle.dump(healthy_RIC, f)
