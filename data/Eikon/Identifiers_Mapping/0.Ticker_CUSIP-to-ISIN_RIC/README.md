## 0.Ticker_CUSIP-to-ISIN_RIC Folder Contents

### 0. Lists

The folder contains 4 pickled text files including the lists of ISINs and RICs for bankupt and healthy companies.


### 1. convertedCSVfiles

The folder contains the following:

* **Bankrupt**

  This folder contains 4 csv files of converting Tickers and CUSIPs from Compustat to Eikon recognized ISINs and RICs, for 112 bankrupt companies.

* **Healthy**

  This folder contains 24 csv files of converting Tickers and CUSIPs from Compustat to Eikon recognized ISINs and RICs, for 20783 healthy companies. For each conversion, since Eikon does not accept large-batch conversion of identifiers, we needed to divide the list into smaller chunks. Though it was possible to work with 10,000-company chunks, but it seemed like with the bigger sizes of batchs, the conversions results have more mysterious missing rows. 
  
* **ConvertSymbol.ipynb**

  The code for converting symbols using Eikon methods.


### 2. 0.bankrupt_list.csv
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


### 3. 0.healthy_list.csv
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


### 4. README.md
Just Read me!

### 5. csvProcessing.ipynb
The code for reading csv files from *convertedCSVfiles* folder and merge them into two csv files of bankrupt and healthy companies, ready for the next rounds of conversions.
<br>
