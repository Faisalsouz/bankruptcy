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
