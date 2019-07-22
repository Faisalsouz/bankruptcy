"""
Accepts a list of cik and company codes separated by a space on each line.
For each line downloads the corresponding forms for a given time period. 
"""

import os
import time
from SECEdgar.crawler import SecCrawler

def get_filings():
    t1 = time.time()
    os.makedirs('10KData', exist_ok=True)			# create directory
    seccrawler = SecCrawler(os.getcwd() + '/' + '10KData') 

    with open('company_list.txt', 'r') as f:
        for i in f:
            print(i)

            companyCode = i.split()[1]      # company code
            cik = "0000" + i.split()[0]              # cik code
            date = '20010101'       # most recent report to consider(YYYYMMDD)
            count = '10'            # no of filings up to specified date

            seccrawler.filing_10Q(companyCode, cik, date, count)
            seccrawler.filing_10K(companyCode, cik, date, count)
            seccrawler.filing_8K(companyCode, cik, date, count)
            seccrawler.filing_13F(companyCode, cik, date, count)


    t2 = time.time()
    print ("Total Time taken: {0}".format(t2-t1))

if __name__ == '__main__':
    get_filings()