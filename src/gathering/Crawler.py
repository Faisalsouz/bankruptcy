import requests
from bs4 import BeautifulSoup

class EdgarQueryCrawler:
    """
    This class can be used to crawle filings information from EDGAR using complex queries. 
    """
    _base_url = 'https://www.sec.gov';
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
    
    def __init__(self, success, result):
        """
        Initializes a new instance.
        
        Args:
            success: A boolean value indicating whether the query was successful.
            result: The result of the query.
        """
        self.success = success
        self.result = result