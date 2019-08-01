## Compustat Raw Data

### 1. chunk_1.rtf
The file includes 175019 rows of Compustat raw data of 'International and North America companies' for the columns:

* **gvkey**

    The Global Company Key or GVKEY is a unique six-digit number key assigned to each company (issue, currency, index) in the Capital IQ Compustat database. It is a company (issue, currency, index) identifier similar to a TICKER symbol. It represents the primary key for a company that is an index constituent.
    
* **datadate**

     It refers to the period in which the financial activity occurred. Though, all those financial activity columns are missing in the data file that we have. 
     
* **fyear**

    Financial year

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
     * 07: Other (no longer files with SEC among other possible reasons), but pricing continues
     * 09: Now a private company
     * 10: Other (no longer files with SEC among other reasons)
     * 11: Agency governing settlement of securities' trading inactivated the issue's Local Settlement Code because the issue matured, 
        expired or was called. No successor settlement code was established.
     * 12: Agency governing settlement of securities' trading inactivated the issue's Local Settlement Code. A successor settlement 
        code was established; issue was changed for another, as in a par value change.
     * 13: Price source for the SEDOL was no longer available. Issue now identified under different SEDOL.
     * 14: Fully paid issue was replaced or partly paid issue was replaced by a subsequent installment. Successor settlement code was established.
     
* **conm**


### 2. chunk_2.rtf
The file includes the same 175019 rows of Compustat raw data, but for the following columns:
* **tic**
* **cusip**
* **cik**
* **exchg**
* **consol**
* **indfmt**
* **datafmt**
* **popsrc**
* **curcd**
* **costat**


### 3. raw_data.txt
This is the parent file of the first two.
