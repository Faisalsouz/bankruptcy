import eikon as ek  # the Eikon Python wrapper package
import numpy as np
import pandas as pd
import cufflinks as cf
import configparser as cp


## Connecting to Eikon Data API
# ----------------------------------------------------------------------
# This code sets the app_id to connect to the Eikon Data API Proxy
# which needs to be running locally. It requires the previously created
# text file eikon.cfg to be in the current working directory.

cfg = cp.ConfigParser()
cfg.read('eikon.cfg')

ek.set_app_key(cfg['eikon']['app_id']) #set_app_id function being deprecated

## Converting Symbols
# read data for bankrupt and healthy companies
# read the list of bankrupt companies
bankrupt = pd.read_csv('bankrupt.csv') # check for the path
healthy = pd.read_csv('healthy.csv') # check for the path

# get the tickers
bankrupt_ticker = bankrupt['Ticker'].tolist()
healthy_ticker = healthy['Ticker'].tolist()

# get CUSIP
bankrupt_cusip = bankrupt['CUSIP'].tolist()
healthy_cusip = healthy['CUSIP'].tolist()

# print(len(set(bankrupt_ticker)))      # output: 112
# print(len(set(bankrupt_cusip)))       # output: 112
# print(len(set(healthy_ticker)))       # output: 20708
# print(len(set(healthy_cusip)))        # output: 20766

# ======================================================================
# Bankrupt Companies
# ======================================================================
# ----------------------------------------------------------------------
### Bankrupt: Ticker to RIC
# ----------------------------------------------------------------------
# convert tickers to RIC
bankrupt_tic2ric = ek.get_symbology(bankrupt_ticker, from_symbol_type='ticker',
                                    to_symbol_type='RIC')

# checking the length of the resulted df
# print(len(bankrupt_tic2ric))      # output: 112

# write the results as a csv file
bankrupt_tic2ric.to_csv('bankrupt_tic2ric.csv')

# check the number of unique RICs obtained
# print(len(set(bankrupt_tic2ric.RIC.to_list()))) # output: 58


# ----------------------------------------------------------------------
### Bankrupt: Ticker to ISIN
# ----------------------------------------------------------------------
# convert Tickers to ISIN
bankrupt_tic2isn = ek.get_symbology(bankrupt_ticker, from_symbol_type='ticker',
                                    to_symbol_type='ISIN')

# checking the length of the resulted df
# print(len(bankrupt_tic2isn))      # output: 112

# write the results as a csv file
bankrupt_tic2isn.to_csv('bankrupt_tic2isn.csv')

# check the number of unique ISINs obtained
# print(len(set(bankrupt_tic2isn.ISIN.to_list())))    # output: 96


# ----------------------------------------------------------------------
### Bankrupt: CUSIP to RIC
# ----------------------------------------------------------------------
# convert CUSIP to RIC
bankrupt_csp2ric = ek.get_symbology(bankrupt_cusip, from_symbol_type='CUSIP',
                                    to_symbol_type='RIC')

# checking the length of the resulted df
# print(len(bankrupt_csp2ric))      # output: 112

# write the results as a csv file
bankrupt_csp2ric.to_csv('bankrupt_csp2ric.csv')

# check the number of unique RICs obtained
# print(len(set(bankrupt_csp2ric.RIC.to_list())))   # output: 7


# ----------------------------------------------------------------------
### Bankrupt: CUSIP to ISIN
# ----------------------------------------------------------------------
# convert CUSIP to ISIN
bankrupt_csp2isn = ek.get_symbology(bankrupt_cusip, from_symbol_type='CUSIP',
                                    to_symbol_type='ISIN')

# checking the length of the resulted df
# print(len(bankrupt_tic2isn))      # output: 112

# write the results as a csv file
bankrupt_csp2isn.to_csv('bankrupt_csp2isn.csv')

# check the number of unique ISINs obtained
# print(len(set(bankrupt_tic2isn.ISIN.to_list())))  # output: 96


# ======================================================================
# Healthy Companies
# ======================================================================
# ----------------------------------------------------------------------
### Preprocessing healthy lists for NANs and length
# ----------------------------------------------------------------------
# make lists of Tickers and CUSIPs without NANs
h_tic = healthy['Ticker'].dropna().tolist()
h_csp = healthy['CUSIP'].dropna().tolist()

# divide healthy Tickers list to 4000-ticker chunks
# cause Eikon does not convert a 20,000 length list
# last chunk includes only 761 Tickers
h_tic1 = h_tic[:4000]
h_tic2 = h_tic[4000:8000]
h_tic3 = h_tic[8000:12000]
h_tic4 = h_tic[12000:16000]
h_tic5 = h_tic[16000:20000]
h_tic6 = h_tic[20000:]


# divide healthy CUSIPs list to 4000-CUSIP chunks
# cause Eikon does not convert a 20,000 length list
# last chunk includes only 765 CUSIPs
h_csp1 = h_csp[:4000]
h_csp2 = h_csp[4000:8000]
h_csp3 = h_csp[8000:12000]
h_csp4 = h_csp[12000:16000]
h_csp5 = h_csp[16000:20000]
h_csp6 = h_csp[20000:]

# ----------------------------------------------------------------------
### Healthy: Ticker to RIC
# ----------------------------------------------------------------------
# convert Tcikers to RIC - Part I
healthy_tic2ric1 = ek.get_symbology(h_tic1, from_symbol_type='ticker',
                                    to_symbol_type='RIC')

# write the results to a csv file
healthy_tic2ric1.to_csv('healthy_tic2ric1.csv')

# check the number of converted Tickers
# compared to the number of unique RICs obtained
# print(len(healthy_tic2ric1))                      # output: 4000
# print(len(set(healthy_tic2ric1.RIC.to_list())))   # output: 928
# ----------------------------------------------------------------------
# convert Tcikers to RIC - Part II
healthy_tic2ric2 = ek.get_symbology(h_tic2, from_symbol_type='ticker',
                                    to_symbol_type='RIC')

# write the results to a csv file
healthy_tic2ric2.to_csv('healthy_tic2ric2.csv')

# check the number of converted Tickers
# compared to the number of unique RICs obtained
# print(len(healthy_tic2ric2))                      # output: 3998
# print(len(set(healthy_tic2ric2.RIC.to_list())))   # output: 530
# ----------------------------------------------------------------------
# convert Tcikers to RIC - Part III
healthy_tic2ric3 = ek.get_symbology(h_tick3, from_symbol_type='ticker',
                                    to_symbol_type='RIC')

# write the results to a csv file
healthy_tic2ric3.to_csv('healthy_tic2ric3.csv')

# check the number of converted Tickers
# compared to the number of unique RICs obtained
# print(len(healthy_tic2ric3))                      # output: 3997
# print(len(set(healthy_tic2ric3.RIC.to_list())))   # output: 460
# ----------------------------------------------------------------------
# convert Tcikers to RIC - Part IV
healthy_tic2ric4 = ek.get_symbology(h_tic4, from_symbol_type='ticker',
                                    to_symbol_type='RIC')

# write the results to a csv file
healthy_tic2ric4.to_csv('healthy_tic2ric4.csv')

# check the number of converted Tickers
# compared to the number of unique RICs obtained
# print(len(healthy_tic2ric4))                      # output: 4000
# print(len(set(healthy_tic2ric4.RIC.to_list())))   # output: 763
# ----------------------------------------------------------------------
# convert Tcikers to RIC - Part V
healthy_tic2ric5 = ek.get_symbology(h_tic5, from_symbol_type='ticker',
                                    to_symbol_type='RIC')

# write the results to a csv file
healthy_tic2ric5.to_csv('healthy_tic2ric5.csv')

# check the number of converted Tickers
# compared to the number of unique RICs obtained
# print(len(healthy_tic2ric5))                      # output: 3999
# print(len(set(healthy_tic2ric5.RIC.to_list())))   # output: 705
# ----------------------------------------------------------------------
# convert Tcikers to RIC - Part VI
healthy_tic2ric6 = ek.get_symbology(h_tic6, from_symbol_type='ticker',
                                    to_symbol_type='RIC')

# write the results to a csv file
healthy_tic2ric6.to_csv('healthy_tic2ric6.csv')

# check the number of converted Tickers
# compared to the number of unique RICs obtained
# print(len(healthy_tic2ric6))                      # output: 761
# print(len(set(healthy_tic2ric6.RIC.to_list())))   # output: 123


# ----------------------------------------------------------------------
### Healthy: Ticker to ISIN
# ----------------------------------------------------------------------
# convert Tcikers to ISIN - Part I
healthy_tic2isn1 = ek.get_symbology(h_tic1, from_symbol_type='ticker',
                                    to_symbol_type='ISIN')

# write the results to a csv file
healthy_tic2isn1.to_csv('healthy_tic2isn1.csv')

# check the number of converted Tickers
# compared to the number of unique ISINs obtained
# print(len(healthy_tic2isn1))                      # output: 4000
# print(len(set(healthy_tic2isn1.ISIN.to_list())))  # output: 2355
# ----------------------------------------------------------------------
# convert Tcikers to ISIN - Part II
healthy_tic2isn2 = ek.get_symbology(h_tic2, from_symbol_type='ticker',
                                    to_symbol_type='ISIN')

# write the results to a csv file
healthy_tic2isn2.to_csv('healthy_tic2isn2.csv')

# check the number of converted Tickers
# compared to the number of unique ISINs obtained
# print(len(healthy_tic2isn2))                      # output: 3998
# print(len(set(healthy_tic2isn2.ISIN.to_list())))  # output: 2136
# ----------------------------------------------------------------------
# convert Tcikers to ISIN - Part III
healthy_tic2isn3 = ek.get_symbology(h_tic3, from_symbol_type='ticker',
                                    to_symbol_type='ISIN')

# write the results to a csv file
healthy_tic2isn3.to_csv('healthy_tic2isn3.csv')

# check the number of converted Tickers
# compared to the number of unique ISINs obtained
# print(len(healthy_tic2isn3))                      # output: 3997
# print(len(set(healthy_tic2isn3.ISIN.to_list())))  # output: 2414
# ----------------------------------------------------------------------
# convert Tcikers to ISIN - Part IV
healthy_tic2isn4 = ek.get_symbology(h_tic4, from_symbol_type='ticker',
                                    to_symbol_type='ISIN')

# write the results to a csv file
healthy_tic2isn4.to_csv('healthy_tic2isn4.csv')

# check the number of converted Tickers
# compared to the number of unique ISINs obtained
# print(len(healthy_tic2isn4))                      # output: 4000
# print(len(set(healthy_tic2isn4.ISIN.to_list())))  # output: 2338
# ----------------------------------------------------------------------
# convert Tcikers to ISIN - Part V
healthy_tic2isn5 = ek.get_symbology(h_tic5, from_symbol_type='ticker',
                                    to_symbol_type='ISIN')

# write the results to a csv file
healthy_tic2isn5.to_csv('healthy_tic2isn5.csv')

# check the number of converted Tickers
# compared to the number of unique ISINs obtained
# print(len(healthy_tic2isn5))                      # output: 3999
#print(len(set(healthy_tic2isn5.ISIN.to_list())))   # output: 2259
# ----------------------------------------------------------------------
# convert Tcikers to ISIN - Part VI
healthy_tic2isn6 = ek.get_symbology(h_tic6, from_symbol_type='ticker',
                                    to_symbol_type='ISIN')

# write the results to a csv file
healthy_tic2isn6.to_csv('healthy_tic2isn6.csv')

# check the number of converted Tickers
# compared to the number of unique ISINs obtained
# print(len(healthy_tic2isn6))                      # output: 761
# print(len(set(healthy_tic2isn6.ISIN.to_list())))  # output: 418


# ----------------------------------------------------------------------
### Healthy: CUSIP to RIC
# ----------------------------------------------------------------------
# convert CUSIP to RIC - Part I
healthy_csp2ric1 = ek.get_symbology(h_csp1, from_symbol_type='CUSIP',
                                    to_symbol_type='RIC')

# write the results to a csv file
healthy_csp2ric1.to_csv('healthy_csp2ric1.csv')

# check the number of converted CUSIPs
# compared to the number of unique RICs obtained
# print(len(healthy_csp2ric1))                      # output: 4000
# print(len(set(healthy_csp2ric1.RIC.to_list())))   # output: 2113
# ----------------------------------------------------------------------
# convert CUSIP to RIC - Part II
healthy_csp2ric2 = ek.get_symbology(h_csp2, from_symbol_type='CUSIP',
                                    to_symbol_type='RIC')

# write the results to a csv file
healthy_csp2ric2.to_csv('healthy_csp2ric2.csv')

# check the number of converted CUSIPs
# compared to the number of unique RICs obtained
# print(len(healthy_csp2ric2))                      # output: 4000
# print(len(set(healthy_csp2ric2.RIC.to_list())))   # output: 1662
# ----------------------------------------------------------------------
# convert CUSIP to RIC - Part III
healthy_csp2ric3 = ek.get_symbology(h_csp3, from_symbol_type='CUSIP',
                                    to_symbol_type='RIC')

# write the results to a csv file
healthy_csp2ric3.to_csv('healthy_csp2ric3.csv')

# check the number of converted CUSIPs
# compared to the number of unique RICs obtained
# print(len(healthy_csp2ric3))                      # output: 4000
# print(len(set(healthy_csp2ric3.RIC.to_list())))   # output: 1831
# ----------------------------------------------------------------------
# convert CUSIP to RIC - Part IV
healthy_csp2ric4 = ek.get_symbology(h_csp4, from_symbol_type='CUSIP',
                                    to_symbol_type='RIC')

# write the results to a csv file
healthy_csp2ric4.to_csv('healthy_csp2ric4.csv')

# check the number of converted CUSIPs
# compared to the number of unique RICs obtained
# print(len(healthy_csp2ric4))                      # output: 4000
# print(len(set(healthy_csp2ric4.RIC.to_list())))   # output: 1499
# ----------------------------------------------------------------------
# convert CUSIP to RIC - Part V
healthy_csp2ric5 = ek.get_symbology(h_csp5, from_symbol_type='CUSIP',
                                    to_symbol_type='RIC')

# write the results to a csv file
healthy_csp2ric5.to_csv('healthy_csp2ric5.csv')

# check the number of converted CUSIPs
# compared to the number of unique RICs obtained
# print(len(healthy_csp2ric5))                      # output: 4000
# print(len(set(healthy_csp2ric5.RIC.to_list())))   # output: 1363
# ----------------------------------------------------------------------
# convert CUSIP to RIC - Part VI
healthy_csp2ric6 = ek.get_symbology(h_csp6, from_symbol_type='CUSIP',
                                    to_symbol_type='RIC')

# write the results to a csv file
healthy_csp2ric6.to_csv('healthy_csp2ric6.csv')

# check the number of converted CUSIPs
# compared to the number of unique RICs obtained
# print(len(healthy_csp2ric6))                      # output: 765
# print(len(set(healthy_csp2ric6.RIC.to_list())))   # output: 362


# ----------------------------------------------------------------------
### Healthy: CUSIP to ISIN
# ----------------------------------------------------------------------
# convert CUSIP to ISIN - Part I
healthy_csp2isn1 = ek.get_symbology(h_csp1, from_symbol_type='CUSIP',
                                    to_symbol_type='ISIN')

# write the results to a csv file
healthy_csp2isn1.to_csv('healthy_csp2isn1.csv')

# check the number of converted CUSIPs
# compared to the number of unique ISINs obtained
# print(len(healthy_tic2isn1))                      # output: 4000
# print(len(set(healthy_tic2isn1.ISIN.to_list())))  # output: 2355
# ----------------------------------------------------------------------
# convert CUSIP to ISIN - Part II
healthy_csp2isn2 = ek.get_symbology(h_csp2, from_symbol_type='CUSIP',
                                    to_symbol_type='ISIN')

# write the results to a csv file
healthy_csp2isn2.to_csv('healthy_csp2isn2.csv')

# check the number of converted CUSIPs
# compared to the number of unique ISINs obtained
# print(len(healthy_tic2isn2))                      # output: 3998
# print(len(set(healthy_tic2isn2.ISIN.to_list())))  # output: 2136
# ----------------------------------------------------------------------
# convert CUSIP to ISIN - Part III
healthy_csp2isn3 = ek.get_symbology(h_csp3, from_symbol_type='CUSIP',
                                    to_symbol_type='ISIN')

# write the results to a csv file
healthy_csp2isn3.to_csv('healthy_csp2isn3.csv')

# check the number of converted CUSIPs
# compared to the number of unique ISINs obtained
# print(len(healthy_tic2isn3))                      # output: 3997
# print(len(set(healthy_tic2isn3.ISIN.to_list())))  # output: 2414
# ----------------------------------------------------------------------
# convert CUSIP to ISIN - Part IV
healthy_csp2isn4 = ek.get_symbology(h_csp4, from_symbol_type='CUSIP',
                                    to_symbol_type='ISIN')

# write the results to a csv file
healthy_csp2isn4.to_csv('healthy_csp2isn4.csv')

# check the number of converted CUSIPs
# compared to the number of unique ISINs obtained
# print(len(healthy_tic2isn4))                      # output: 4000
# print(len(set(healthy_tic2isn4.ISIN.to_list())))  # output: 2338
# ----------------------------------------------------------------------
# convert CUSIP to ISIN - Part V
healthy_csp2isn5 = ek.get_symbology(h_csp5, from_symbol_type='CUSIP',
                                    to_symbol_type='ISIN')

# write the results to a csv file
healthy_csp2isn5.to_csv('healthy_csp2isn5.csv')

# check the number of converted CUSIPs
# compared to the number of unique ISINs obtained
# print(len(healthy_tic2isn5))                      # output: 3999
# print(len(set(healthy_tic2isn5.ISIN.to_list())))  # output: 2259
# ----------------------------------------------------------------------
# convert CUSIP to ISIN - Part VI
healthy_csp2isn6 = ek.get_symbology(h_csp6, from_symbol_type='CUSIP',
                                    to_symbol_type='ISIN')

# write the results to a csv file
healthy_csp2isn6.to_csv('healthy_csp2isn6.csv')

# check the number of converted CUSIPs
# compared to the number of unique ISINs obtained
# print(len(healthy_tic2isn6))                      # output: 761
# print(len(set(healthy_tic2isn6.ISIN.to_list())))  # output: 418
