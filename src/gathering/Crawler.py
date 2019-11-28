import requests
import time
import xml.etree.ElementTree as ET 
from bs4 import BeautifulSoup

class EdgarFilingCrawler:
    """
    This class can be used to crawle filings from EDGAR.
    """
    _base_url = 'https://www.sec.gov'
    _base_request_url = "http://www.sec.gov/cgi-bin/browse-edgar"
    _max_retry = None

    def __init__(self, max_retry):
        """
        Initializes a new instance.

        Args:
            max_retry: Specifies how many times each request is retried.
        """
        self._max_retry = max_retry

    
    def get_filing(self, url):
        """
        Requests and returns the filing.

        Args:
            url (str): The URL to the filing.

        Returns:
            A contract that contains the requested filing.
        """
        success = False
        result = None
        message = ''
        counter = 0
        while (not success and counter < self._max_retry):
            counter += 1
            r = requests.get(url)
            if r.status_code == 200:
                message = self._add_to_string(message, '{}. Request was successfull ({})'.format(counter, r.status_code))
                success = True
                result = r.text
            else:
                message = self._add_to_string(message, '{}. Request was not successfull ({})'.format(counter, r.status_code))
                # just wait 3 seconds
                time.sleep(3)
        return QueryResult(success, result, message)


    def check_cik_format(self, cik):
        """
        Checks the Central Index Key code.

        Args:
            cik (Union[str, int]): The Central Index Key to check.

        Returns:
            True, if the CIK has the correct format.
        """
        valid_str = isinstance(cik, str) and len(cik) == 10
        valid_int = isinstance(cik, int) and (999999999 < cik < 10**10)
        valid_type = isinstance(cik, (int, str))
        return (valid_str or valid_int) and valid_type


    def get_latest_filing_links(self, cik, priorto, filing_type, count=1):
        """
        Gets the link to the latest filing that meets the search criteria.

        Args:
            cik (Union[str, int]): Central Index Key assigned by SEC.
            priorto (str): Most recent filing to consider. Must be in form 'YYYYMMDD'.
            filing_type (str): Choose from list of valid filing types ('10-Q', '10-K', '8-K', '13-F', 'SD')
            count (int): The number of form links to retrieve.

        Returns:
            A contract that holds information about the request.
            The result is a list that contains links to the requested filings.
        """
        success = False
        message = ''
        result = []
        if self.check_cik_format(cik):
            # create the request
            params = {'action': 'getcompany', 'owner': 'exclude', 'output': 'xml', 'CIK': cik, 'type': filing_type, 'dateb': priorto, 'count': count}
            counter = 0
            while (not success and counter < self._max_retry):
                counter += 1
                r = requests.get(self._base_request_url, params=params)
                if r.status_code == 200:
                    message = self._add_to_string(message, '{}. Request was successfull ({})'.format(counter, r.status_code))
                    success = True
                    data = r.text
                    result = self._get_filing_links(data, counter, filing_type)
                else:
                    message = self._add_to_string(message, '{}. Request was not successfull ({})'.format(counter, r.status_code))
                    # just wait 3 seconds
                    time.sleep(3)
        else:
            message = self._add_to_string(message, 'CIK code has the wrong format.')
        return QueryResult(success, result, message)

    
    def _add_to_string(self, string_to_extend, string_to_add):
        """
        Adds the string to the string that should be extended as a new line.

        Parms:
            string_to_extend (str): The string that should be extended.
            string_to_add (str): The string that should be added.

        Returns:
            The extended string.
        """
        if len(string_to_extend) != 0:
            string_to_extend += '\n{}'.format(string_to_add)
        else:
            string_to_extend = string_to_add
        return string_to_extend


    def _get_filing_links(self, data, counter, filing_type):
        """
        Gets the filing links from the given data.

        Args:
            data (str): The xml-text containing the filing links.
            counter (int): The number of links to look for.
            filing_type (str): Choose from list of valid filing types ('10-Q', '10-K', '8-K', '13-F', 'SD')

        Returns:
            A list with links to the filings.
        """
        root = ET.fromstring(data)
        link_list = []
        for filing in root.findall('./results/filing'):
            if filing.find('type').text == filing_type:
                link_list.append(filing.find('filingHREF').text)
        txt_urls = [link[:link.rfind("-")] + ".txt" for link in link_list]
        if len(txt_urls) > counter:
            txt_urls = txt_urls[:counter]
        return txt_urls


class EdgarQueryCrawler:
    """
    This class can be used to crawle filings information from EDGAR using complex queries. 
    """
    _base_url = 'https://www.sec.gov'
    _base_query_url = 'https://www.sec.gov/cgi-bin/srch-edgar'
        
        
    def get_filing_list(self, search_string, first, last, start=1, count=100):
        """
        Get a list of fillings that matches the search string and lay in the given period.
        
        Args:
            search_string (str): The search string that is used to filter the results.
            first (int): The first year that should be considered (1994-today).
            last (int): The last year that should be considered (1994-today).
            start (int): The start index of fillings (default 1).
            count (int): Number of filings to retrieved (default 100, between 1 and 100).
            
        Returns:
            A contract that holds information about the query result. 
            The result is a list that contains the companies name, the URL to the filing text file, the filing date and the form type.
        """
        filing_list = []
        success = False
        params = {'text': search_string, 'first':first, 'last':last, 'start': start, 'count': count}
        print('start request with parameters {}'.format(params))
        request = requests.get(self._base_query_url, params=params)
        if request.status_code == 200:
            print('request was successful')
            html_data = request.text
            filing_list = self._create_filing_list(html_data)
            success = True
        else:
            print('request was not successful')
        return QueryResult(success, filing_list)
    
    
    def get_all_filings(self, search_string, first, last, start=1):
        """
        Searches for all documents that meet the search string and are from the specified period.
    
        Args:
            search_string (str): The search string that is used to filter the results.
            first (int): The first year that should be considered (1994-today).
            last (int): The last year that should be considered (1994-today).
            start (int): The start index of fillings (default 1).
        
        Returns:
            A list with all documents that meet the search criteria.
        """
        filing_list = []
        last_query_was_successful = True
        step = 100
        while last_query_was_successful:
            query_result = self.get_filing_list(search_string, first, last, start, step-1)
            start += step
            if query_result.success:
                if len(query_result.result) == 0:
                    last_query_was_successful = False
                else:
                    filing_list.extend(query_result.result)
            else:
                last_query_was_successful = False
        print('{} documents were found.'.format(len(filing_list)))
        return filing_list
    
    def _create_filing_list(self, data):
        """
        Creates a list of filings from the given data.
        
        Args:
            data (str): html data that contains the fillings.
            
        Returns:
            A list with all filings from the given data.
            It contains the companies name, the URL to the filing text file, the filing date and the form type.
        """
        table = self._get_table(data)
        name_list = []
        url_list = []
        type_list = []
        date_list = []
        
        for row in table.findChildren('tr'):
            cells = row.findChildren('td')
            if len(cells) == 6:
                name_list.append(cells[1].string)
                url_list.append('{}{}'.format(self._base_url, cells[2].findAll("a")[0]['href']))
                type_list.append(cells[3].string)
                date_list.append(cells[4].string)
                
        return list(zip(name_list, url_list, type_list, date_list))
        
        
    def _get_table(self, data):
        """
        Gets the table containing the required information from the specified data.
        
        Args:
            data (str): html data that contains the table.
            
        Returns:
            The table containing the required information
        """
        soup = BeautifulSoup(data, features='html.parser')
        # Since we have no other option, we must first retrieve all the tables from the document and then return the desired one.
        tables = soup.findAll("table")
        return tables[len(tables) - 2]
    
    
class QueryResult:
    """
    A contract that holds information about a query result.
    """
    success = False
    result = None
    message = ''
    
    def __init__(self, success, result, message=''):
        """
        Initializes a new instance.
        
        Args:
            success: A boolean value indicating whether the query was successful.
            result: The result of the query.
            message: The message to set.
        """
        self.success = success
        self.result = result
        self.message = message