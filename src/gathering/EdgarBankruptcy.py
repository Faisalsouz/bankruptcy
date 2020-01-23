import requests
from crawler import EdgarQueryCrawler
import re


def check_bankruptcy(start = 1):
    """
    Checks if a company that has filled item 1.03 of 8-K or 8-K/A form is bankrupt.
    
    Args:
        start (int): The start index of fillings (default 1).
    
    Returns:
        A list with the company name, CIK code, bankruptcy flag, chapter of bankruptcy, the form type and date and the URL to the form.
    """
    crawler = EdgarQueryCrawler()
    search_string = r'items=1.03 AND (type=8-K OR type=8-K/A)'
    raw_list = crawler.get_all_filings(search_string, 1994, 2019, start)
    out_list = []
    for company, url, form_type, date in raw_list:
        r = requests.get(url)
        if r.status_code == 200:
            data = r.text
            bankrupt, cik, chapter = is_bankrupt(data, company)
            out_list.append((company, cik, bankrupt, chapter, form_type, date, url))
    return out_list


def is_bankrupt(document, company):
    """
    Checks whether a company that has filled in item 1.03 of form 8-K or 8-K/A is likely to be bankrupt.
    
    Args:
        data (str): The html-data that represents a 8-K or 8-K/A form.
        company (str): The company name.
        
    Returns:
        A tuple holding the information if the company is bankrupt, the CIK code and the chapter of bankruptcy.
    """ 
    chapter = _get_bankruptcy_chapter(document)
    cik = _get_cik(document)
    bankrupt = False
    if chapter != -1:
        print('The {} is bankrupt under chapter {}'.format(company, chapter))
        bankrupt = True
    else:
        print('The {} is not bankrupt'.format(company))
    return (bankrupt, cik, chapter)

    
def _get_bankruptcy_chapter(text):
    """
    Returns the bankruptcy chapter.
    
    Args:
        text (str): The text in which the chapter is to be searched for.
        
    Returns:
        The number of the chapter, if it was found, otherwise -1.
    """
    chapter = -1
    chapter_regex = r'[Cc]hapter(&nbsp;| )(7|11) (of [Tt]itle(&nbsp;| )11|of the( United States | US | U.S. | | Federal )Bankruptcy (Act|Code))'
    r = re.compile(chapter_regex)
    matches = r.findall(text.replace('\n', ' ').replace('\r', ''))
    if matches:
        chapter = matches[0][1]
    return chapter


def _get_cik(text):
    """
    Returns the central index key (cik).
    
    Args:
        text (str): The text in which the cik is to be searched for.
        
    Returns:
        The cik, if it was found, otherwise -1.
    """
    cik = -1
    cik_regex = r'CENTRAL INDEX KEY:...(\d*)'
    r = re.compile(cik_regex)
    matches = r.findall(text)
    if matches:
        cik = matches[0]
    return cik