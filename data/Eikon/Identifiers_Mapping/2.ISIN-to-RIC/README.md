## 2.ISIN-to-RIC Folder Contents

### 0. ConvertedPcklFiles

The folder contains three other folders of the efforts to retrieve RICs from Eikon, using Tickers and CUSIPs came with Compustat data:

* **ISIN-to-RIC.ipynb**
  
  The code takes lists of bankrupt and healthy companies' RICs and ISINs and converts RICs to ISINs and ISINs to RICs, for the further checks to make sure everything is okay.
  
* **bankrupt_ISIN2RIC.txt**
  
  The pickle file of bankrupt companies ISINs to RICs conversion.
  
* **bankrupt_RIC2ISIN.txt**

  The pickle file of bankrupt companies RICs to ISINs conversion.
  
* **healthy_ISIN2RIC.txt**

  The pickle file of healthy companies ISINs to RICs conversion.
  
* **healthy_RIC2ISIN.txt**

  The pickle file of healthy companies RICs to ISINs conversion.
  
  
### 1. 2.bankrupt_list.csv

The list of bankrupt companies, modified, after adding RICs converted from ISINs.

### 2. 2.healthy_list.csv

The list of healthy companies, modified, after adding RICs converted from ISINs.

### 3. README.md

Just read me!

### 4. pcklProcessing.ipynb

The code to read pickle files and add new RIC column to the bankrupt and healthy companies' lists.
