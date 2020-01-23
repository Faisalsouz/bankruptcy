## Eikon Folder Contents

### 0. Identifiers_Mapping

The folder contains three other folders of the efforts to retrieve RICs from Eikon, using Tickers and CUSIPs came with Compustat data:

* **0.Ticker_CUSIP-to-ISIN_RIC**
* **1.CUSIP-to-ISIN**
* **2.ISIN-to-RIC**
* **README.md**


### 1. data_bankrupt

The folder contains data downloaded using bankrupt companies' CIKs. The bankrupt CIKs list is divided into chunks of, at most, 500 companies (it makes 3 chunks) for each chunk the data for 26 financial factors were downloaded for 20 years (2000-2019), each year in one csv files. That makes 3 * 20 = 60 csv files for bankrupt companies.


### 2. data_healthy

The folder contains data downloaded using healthy companies' CIKs. The healthy CIKs list is divided into chunks of, at most, 500 companies (it makes 30 chunks) for each chunk the data for 26 financial factors were downloaded for 20 years (2000-2019), each year in one csv files. That makes 30 * 20 = 600 csv files for healthy companies.


### 3. CIK_list_bankrupt.txt

A pickle file of the CIK codes for 1103 bankrupt companies.


### 4. CIK_list_healthy.txt

A pickle file of the CIK codes for 14761 healthy companies.


### 5. GetDataWithCIKsAnnually.ipynb

The code for downloading data using companies' CIK from Eikon.


### 6. MergeCode.ipynb

The code for merging all csv files in one dataframe.


### 7. README.md

Just Read me!


### 8. eikon.cfg

The file includes Eikon API proxy code and should be read by downloader code to grant access to the database.

