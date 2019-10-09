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
The code for downlinad historical timeseries and financial data for the companies in the two _bankrupt_ and _healthy_ lists from Thomson Reuters Eikon.
<br>

### 3. README.md
Just Read me!
<br>

### 4-5. csvProcessing.[py,ipynb]
The code for reading csv files from *convertedCSVfiles* folder and merge them into two final csv files of bankrupt and healthy companies, including following columns:
   * **Identifier**: gvkey
   * **Company**: comnl, the legal name of company
   * **Data Deletion Date**: dldte
   * **Deletion Reason**: dlrsn
   * **Ticker**: tic
   * **CUSIP**: cusip
   * **CIK**: cik
   * **ISIN**: ISIN (International Securities Identification Number) code 
   * **ISINc**: Conflict-check between the two ways of retrieving ISIN code; that is, by converting Ticker and by converting CUSIP
      * 0: No conflict! Both ways resulted in the same value; either a valid code or NAN
      * 1: Conflict! One conversion resulted in a NAN and we obtained a valid code from the other.
      * 3: Serious conflict! Both conversion returned a valid ISIN code but the codes are different.
   * **RIC**: Eikon's RIC (Reuters Instrument Code)
   * **RICc**: Conflict-check between the two ways of retrieving RIC; that is, by converting Ticker and by converting CUSIP
      * 0: No conflict! Both ways resulted in the same value; either a valid code or NAN
      * 1: Conflict! One conversion resulted in a NAN and we obtained a valid code from the other.
      * 3: Serious conflict! Both conversion returned a valid RIC but the codes are different.
<br>

### 6. eikon.cfg
something
<br>

### 7. final_bankrupt_list.csv
something
<br>

### 8. final_healthy_list.csv
