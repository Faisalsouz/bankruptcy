## Eikon Folder Contents

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

The folder contains data downloaded using healthy companies' CIKs. One hundred of these csv files are all the historical data available on Eikon for each healthy company that has a valid CIK and are saved by the company's CIK code, and one file *healthy_data.csv*, includes financial factors/ratios of all healthy companies with a valid CIK. <br>
*Healthy data is not completely pushed to Git, because it exceeds both Github limitations on the files count and the total size of the files. Though, the data is fully uploaded on the study project's folder in OneDrive.*


### 4. data_healthy_RIC

The folder contains data downloaded using healthy companies' RICs. One hundred of these csv files are all the historical data available on Eikon for each healthy company that has a valid RIC and are saved by the company's RIC code, and one file *healthy_data.csv*, includes financial factors/ratios of all healthy companies with a valid RIC.
*Healthy data is not completely pushed to Git, because it exceeds both Github limitations on the files count and the total size of the files. Though, the data is fully uploaded on the study project's folder in OneDrive.*


### 5. GetDataWithCIKs.ipynb

The code for downloading data using companies' CIK from Eikon.

### 6. GetDataWithRICs.ipynb

The code for downloading data using companies' RIC from Eikon.

### 7. README.md

Just Read me!

### 8. eikon.cfg

The file includes Eikon API proxy code and should be read by downloader code to grant access to the database.

