## Compustat Folder Contents

### 0. README.md
Just Read me!

### 1. chunk_1.rtf
The file includes 175019 rows of Compustat raw data of 'International and North America companies' for this 7 columns:

* **gvkey**

    The Global Company Key or GVKEY is a unique six-digit number key assigned to each company (issue, currency, index) in the Capital IQ Compustat database. It is a company (issue, currency, index) identifier similar to a TICKER symbol. It represents the primary key for a company that is an index constituent.
    
* **datadate**

     It refers to the period in which the financial activity occurred. Though, all those financial activity columns are missing in the data file that we have. 
     
* **fyear**

    The fiscal year that the company is in at the time of _datadate_
    
* **conml**
    
    Company legal name
    
* **dldte**

    The company deletion date. So it turned out that _deletion_ does not necessarily mean bankruptcy. The process of adding/saving company's data might be stopped due to several reasons. The reason is explained under the neighboring column _drrsn_. 
    
* **dlrsn**

    The deletion reason: the reason Copmustat stopped recording / lack the company's data.
    
     _dlsn_ codes:
     * 01: Acquisition or merger
     * **02: Bankruptcy**
     * 03: Liquidation
     * 04: Reverse acquisition (1983 forward)
     * 05: No longer fits original format (1978 forward)
     * 06: Leveraged buyout (1982 forward)
     * 07: Other (no longer files with 'The Securities and Exchange Commission' among other possible reasons), but pricing continues
     * 09: Now a private company
     * 10: Other (no longer files with 'The Securities and Exchange Commission' among other reasons)
     * 11: Agency governing settlement of securities' trading inactivated the issue's Local Settlement Code because the issue matured, 
        expired or was called. No successor settlement code was established.
     * 12: Agency governing settlement of securities' trading inactivated the issue's Local Settlement Code. A successor settlement 
        code was established; issue was changed for another, as in a par value change.
     * 13: Price source for the SEDOL was no longer available. Issue now identified under different SEDOL.
     * 14: Fully paid issue was replaced or partly paid issue was replaced by a subsequent installment. Successor settlement code was established.
     
* **conm**

    Company name


### 2. chunk_2.rtf
The file includes the same 175019 rows of Compustat raw data, but for the following 10 columns:

* **tic**

    Issue trading ticker (TICI): the stock symbol or simply the abbreviation used to uniquely identify the company.

* **cusip**

    The 9-character alphanumeric CUSIP code identifies any North American security for the purposes of facilitating clearing and settlement of trades. The CUSIP distribution system is owned by the American Bankers Association and is operated by Standard & Poor's. The CUSIP Service Bureau acts as the National numbering agency (NNA) for North America, and the CUSIP serves as the National Securities Identification Number for products issued from both the United States and Canada.
    For working with financial database we need CUSIP.

* **cik**

    The Central Index Key or CIK is a 10-digit number used on the Securities and Exchange Commission's computer systems to identify corporations and individuals who have filed disclosure with the SEC (The Securities and Exchange Commission: a U.S. government agency that oversees securities transactions, activities of financial professionals and mutual fund trading to prevent fraud and intentional deception).
    The CIK can be used to search for company or fund filings on EDGAR, the Electronic Data-Gathering, Analysis, and Retrieval system of submissions by companies and others who are required by law to file forms with the U.S. Securities and Exchange Commission.

* **exchg**

    Stock exchange: the stock market that lists and trades the company's shares.
    
    See [Compustat Stock Exchange Codes](https://uvalibraryfeb.files.wordpress.com/2016/02/stock-exchange-codes-compustat.pdf).

* **consol**

     The variable that indicates the level of consolidation. Here, I guess, it means the level of aggregation of financial statements. Although, we only have code C for this column, so it might be the case that we don't need to worry much about this column. Here are the codes for 'consol' column in Compustat:
     
    | CONSOL  | Meaning                   | Company Population                        |
    | ------- | ------------------------- | ----------------------------------------- |
    | C       | Consolidated              | International and North America companies |
    | I       | Issue-Level Fundamentals  | International companies                   |
    | N       | Non-Consolidated          | International companies                   |
    | P       | Pre-FASB                  | North America companies                   |
    | D       | Pre-Divestiture           | North America companies                   |
    | E       | Post-Divestiture          | North America companies                   |
    | R       | Pro-Forma                 | North America companies                   |    

* **indfmt**

    Industry Format: Indicates whether a company reports in Financial Services or Industrial Format. This must be checked when using the query form on the WRDS website in order to retrieve any financial services firms (e.g. banks).
    
     _indfmt_ codes:
     * FS: Financial Services (includes banks, insurance companies, broker/dealers, real estate and other financial services)
     * INDL: Industrial (includes companies reporting manufacturing, retail, construction and other commercial operations other than financial services)

* **datafmt**

    Data Format code, that indicates how the data is collected and presented, with Standardized (STD) being the common and useful type.
    * STD annual rows are unrestated and quarterly rows are restated.
    * SUMM_STD annual rows come from the summary tables in an annual report and will contain any restatements. Companies typically include up to 10 previous years in these summary tables, and so there will typically be up to 10 years of SUMM_STD rows, after which they are dropped from the database. The STD (as initially reported / unrestated) rows remain permanently. Unrestated quarterly data can be found in a separate product, named "Unrestated Quarterly".
    * PRE_AMENDS: Standardized data collected from the latest annual filing
    * PRE_AMENDSS: Standardized summary data collected prior to company amendment 

* **popsrc**

    Population Source: This item indicates the geographical population source of the data.
    * D: Domestic (North America: U.S. and Canadian companies)
    * I = International (non-U.S. and non-Canadian companies)
    So all we have for this column is surely D.

* **curcd**

    It identifies the reporting currency for a company at each time period. In this column we mainly have USD (US dollar) and a few CAD (Canadian dollar).

* **costat**

    Postal code character: the postal code or zip code of the company’s corporate headquarters or home office. 


### 3. raw_data.txt
This is the parent file of the previous two.


### 4. compustat2csv.[py,ipynb]
Code for making those csv files out of the raw data.
The notebook version, which delivers a more visually comprehensible version of the code, is available only on _notebook_ branch.


### 5. compustat.csv
This csv file is a clean version of Compustat data, including following columns:
   * **Identifier**: gvkey
   * **Company**: comnl, the legal name of company
   * **Data Deletion Date**: dldte
   * **Deletion Reason**: dlrsn
   * **isBankrupt**: This is a column added to the data to, based on the _dlrsn_ content, explicitly shows whether the company went bankrupt (1) or not (0).
   * **CUSIP** cusip
   * **Ticker**: tic
   * **CIK**: cik


### 6. list_bankrupt.csv
A child of _compustat.csv_, including the data of its **112 bankrupt companies.**


### 7. list_healthy.csv
A child of _compustat.csv_, including the data of its **20783 healthy companies.**
