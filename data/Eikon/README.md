## Eikon Folder Contents

### 0. convertedCSVfiles

The folder contains the following:

* **Bankrupt**

  This folder contains 4 csv files of converting Tickers and CUSIPs from Compustat to ISINs and RICs from Eikon, for 112 bankrupt companies.

* **Healthy**

  This folder contains 24 csv files of converting Tickers and CUSIPs from Compustat to ISINs and RICs from Eikon, for 20783 healthy companies. For each conversion, since Eikon does not accept large-batch conversion of identifiers, we needed to divide the list to smaller chunks. Though it was possible to work with 10,000-company chunks, but it seemed like with the bigger sizes of batchs, the conversions results have more mysterious missing rows. 
  
* **ConvertSymbol.[py,ipynb]**

  The code for converting symbols using Eikon methods.
<br>

### 1-2. GetData.[py,ipynb]
The file includes 175019 rows of Compustat raw data of 'International and North America companies' for this 7 columns:

### 3. README.md
Just Read me!


### 4-5. csvProcessing.[py,ipynb]
### 6. eikon.cfg
### 7. final_bankrupt_list.csv
### 8. final_healthy_list.csv
