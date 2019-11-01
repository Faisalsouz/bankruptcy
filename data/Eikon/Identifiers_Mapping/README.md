


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

