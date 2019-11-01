## Eikon Folder Contents (under construction...)

### 0. Identifiers_Mapping

The folder contains three other folders of the efforts to retrieve RICs from Eikon, using Tickers and CUSIPs came with Compustat data:

* **0.Ticker_CUSIP-to-ISIN_RIC**
* **1.CUSIP-to-ISIN**
* **2.ISIN-to-RIC**
* **README.md**


### 1. data_bankrupt_CIK

The folder contains data downloaded using bankrupt companies' CIKs. One hundred of these csv files are all the historical data available on Eikon for each bankrupt company that has a valid CIK and are saved by the company's CIK code, and one file *bankrupt_data.csv*, includes financial factors/ratios of all bankrupt companies with a valid CIK.


### 2. data_bankrupt_RIC

The folder contains data downloaded using bankrupt companies' RICs. One hundred of these csv files are all the historical data available on Eikon for each bankrupt company that has a valid RIC and are saved by the company's RIC code, and one file *bankrupt_data.csv*, includes financial factors/ratios of all bankrupt companies with a valid RIC.


### 3. data_healthy_CIK

The folder contains data downloaded using healthy companies' CIKs. One hundred of these csv files are all the historical data available on Eikon for each healthy company that has a valid CIK and are saved by the company's CIK code, and one file *healthy_data.csv*, includes financial factors/ratios of all healthy companies with a valid CIK.

### 4. data_healthy_RIC

The folder contains data downloaded using healthy companies' RICs. One hundred of these csv files are all the historical data available on Eikon for each healthy company that has a valid RIC and are saved by the company's RIC code, and one file *healthy_data.csv*, includes financial factors/ratios of all healthy companies with a valid RIC.


### 5. GetDataWithCIKs.ipynb

### 6. GetDataWithRICs.ipynb

### 7. README.md

### 8. eikon.cfg



The folder contains 4 pickled text files including the lists of ISINs and RICs for bankupt and healthy companies.


### 1. convertedCSVfiles

The folder contains the following:

* **Bankrupt**

  This folder contains 4 csv files of converting Tickers and CUSIPs from Compustat to Eikon recognized ISINs and RICs, for 112 bankrupt companies.

* **Healthy**

  This folder contains 24 csv files of converting Tickers and CUSIPs from Compustat to Eikon recognized ISINs and RICs, for 20783 healthy companies. For each conversion, since Eikon does not accept large-batch conversion of identifiers, we needed to divide the list into smaller chunks. Though it was possible to work with 10,000-company chunks, but it seemed like with the bigger sizes of batchs, the conversions results have more mysterious missing rows. 
  
* **ConvertSymbol.[py,ipynb]**

  The code for converting symbols using Eikon methods.
<br>

### 2-3. GetData.[py,ipynb]
The code for downloading historical timeseries and financial data, from Thomson Reuters Eikon, for the companies listed in the two final _bankrupt_ and _healthy_ files.
<br>

### 4. README.md
Just Read me!
<br>

### 5-6. csvProcessing.[py,ipynb]
The code for reading csv files from *convertedCSVfiles* folder and merge them into two final csv files of bankrupt and healthy companies, ready to be used for downloading financial data from Eikon.
<br>

### 7. eikon.cfg
Administrative stuff; the file is required to be read by the code to permit the user getting data from Eikon API.
<br>

