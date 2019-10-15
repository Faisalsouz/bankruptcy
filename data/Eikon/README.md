## Eikon Folder Contents

### 0. Lists

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

### 8. final_bankrupt_list.csv
A list of 112 bankrupt companies, based in North America, including the following columns:
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

### 9. final_healthy_list.csv
A list of, supposedly, 20783 healthy companies, based in North America, including the columns listed below; however, the number of rows exceeded 21,000, for some wierd reasons that I'm not aware of yet, but I have to and will find about.
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
