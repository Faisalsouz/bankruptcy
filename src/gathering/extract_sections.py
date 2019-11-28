import requests
from crawler import EdgarFilingCrawler
import re
import os
import sys
import pickle
import logging
import json
import time

# define some codes
NOT_COMPLETED, SUCCESS, ERROR_NO_HREF, ERROR_NO_SECTION, ERROR_YEAR_NOT_VALID = range(5)

# prepare the logging
logger = logging.getLogger('extract_section')
logger.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

# define some regex that we are going to use
filing_date_regex = re.compile(r"date as of change:\s*(\d*)", re.M|re.I) # extracting the timestamp
form_type_regex = re.compile(r"conformed\s+submission\s+type:\s*(\S*)", re.M|re.I) # extracting the form type
href_start_regex = re.compile(r"(?<=href)(((?!href=)[\s\S])*?(discussion\s+and\s+analysis[\s\S]*?))(?=>)", re.M|re.I)
href_end_regex = re.compile(r"(?<=href)(((?!href=)[\s\S])*?(quantitative\s+and\s+qualitative[\s\S]*?))(?=>)", re.M|re.I)
href_regex = re.compile(r"(\"|')[\s\S]*?(\"|')", re.M|re.I)

def extract_section(full_text):
    """
    Extracts the relevant MD&A section and returns the extracted section contract.

    Args:
        full_text (str): The full text to extract the MD&A section from.

    Returns:
        The result object holding the extracted section.
    """
    section = ''
    extracted = False
    code = NOT_COMPLETED
    message = ''
    filing_date = ''
    form_type = ''
    
    try:
        # get the form type
        form_type = _search_pattern(full_text, form_type_regex, group=1)
        # search the filing date
        filing_date = _search_pattern(full_text, filing_date_regex, group=1)

        # search the starting and ending href
        href_start = _search_href(full_text, href_start_regex)
        href_end = _search_href(full_text, href_end_regex)

        # we just need to continue if we have found a starting and ending href
        if (href_start and href_end):
            data_regex = re.compile(r"((name|id)=\"" + re.escape(href_start) + r"(?!" + re.escape(href_start) + r")[\s\S]*?(?=(name|id)=\"" + re.escape(href_end) +r"))", re.M|re.I)	    	    	
            match = re.search(data_regex, full_text)
            if match: 
                logger.info('MD&A section was found')
                extracted = True
                code = SUCCESS
                section = _clean_section(match.group())
            else: 
                message_str = 'MD&A section was not found'
                message = _add_to_string(message, message_str)
                logger.warning(message_str)
                code = ERROR_NO_SECTION
        else:
            message_str = 'Href start and/or href end was not found.'
            message = _add_to_string(message, message_str)
            logger.warning(message_str)
            code = ERROR_NO_HREF
    except AttributeError as error:
        logger.exception('Attribute error: %s', error)
    except Exception as exception:
        logger.exception('Unknown error: %s', exception)
    return ExtractionResult(extracted, section, message=message, filing_date=filing_date, form_type=form_type, code=code)


def _search_href(text, regex):
    """
    Searches a href with the given regular expression in the text.

    Args:
        text (str): The text that contains the href.
        regex (pattern object | str): The pattern to search.

    Returns:
        The href if it was found.
    """
    href = ''
    raw_href_search = re.search(regex, text)
    if raw_href_search:
        href_search = re.search(href_regex, raw_href_search.group())
        if href_search:
            href = href_search.group()[2:-1]
    return href

def _search_pattern(text, pattern, group=0):
    """
    Searches for a pattern in the text.

    Args:
        text (str): The text in which the pattern is to be searched.
        pattern (pattern object | str): The pattern to be searched for.
        group (int): An optional group number that is returned.
    
    Returns:
        The matching group if a string was found.
    """
    match = ''
    search = re.search(pattern, text)
    if search:
        match = search.group(group)
    return match


def _check_form_type(form_type, message):
    """
    Checks the form type.

    Args:
        form_type (str): The form type to check.
        message (str): An object that holds a message.

    Returns:
        True, if the form type is valid.
    """
    is_amend = form_type.lower() == '10-k/a'
    if is_amend:
        message_str = 'Form is an amend file and therefore not processed.'
        logger.debug(message_str)
        message = _add_to_string(message, message_str)
    return not is_amend

def _clean_section(section):
    """
    Removes the html-tags from a section.

    Args:
        section (str): A section that contains html-tags.
    
    Returns:
        A clean version of the section.
    """
    section = re.sub(r"<table.*?</table>", "", section) # remove tables
    section = re.sub(r"italic.*?(?=</font)", "", section) # remove bold text and legends/notes
    section = re.sub(r"underline.*?(?=</font)", "", section) # remove underlined text
    section = re.sub(r"<.*?(?=>)", "", section) # remove html tags 
    section = re.sub(r"&[^;]*;", "", section) # remove html links/placeholder
    section = re.sub(r"\n+", "", section) # remove newlines
    section = re.sub(r"&[^;]*;", "", section) # remove html links/placeholder
    section = re.sub(r">+", " ", section) # remove unnecessary '>' around numbers
    section = re.sub(r"table of contents", "", section) # remove leftovers referencing the table of contents
    return section


def _add_to_string(string_to_extend, string_to_add):
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


class ExtractionResult:
    """
    A contract that holds information about the extraction.
    """
    extracted = False
    section = None
    message = None
    filing_date = None
    cik = None
    year = None
    form_type = None
    url = None
    code = NOT_COMPLETED

    def __init__(self, extracted='', section='', message='', filing_date='', form_type='', code=NOT_COMPLETED):
        """
        Initializes a new instance.
        
        Args:
            extracted (bool): A boolean value indicating whether the extraction was successful.
            section (str): The extracted section.
            message (str): The message to set.
            filing_date (Date | str): The filing date to set.
            form_type (str): The form type.
            code (int): Indicates the current status of the extraction.
        """
        self.extracted = extracted
        self.section = section
        self.message = message
        self.filing_date = filing_date
        self.form_type = form_type
        self.code = code


    def _check_date(self):
        """
        Checks if the filing date and the year matche.
        """
        if self.year and self.filing_date:
            if self.year != self.filing_date[:4]:
                self.code = ERROR_YEAR_NOT_VALID
                logger.warning('The year does not match the filing date for CIK {} and year {}.'.format(self.cik, self.year))
    
    def to_dict(self):
        """
        Creates a dictionary from the saved data.

        Returns:
            A dictionary with the current status of the object.
        """
        self._check_date()
        status_dict = {
            "extracted": self.extracted,
            "code": self.code,
            "message": self.message,
            "section": self.section,
            "CIK": self.cik,
            "year": self.year,
            "filing_date": self.filing_date,
            "form_type": self.form_type,
            "url": self.url
        }
        return status_dict


def _create_directory(dir_path):
    """
    Creates a directory if it does not exist.

    Args:
        dir_path (str): The directory to create.
    """
    if not os.path.exists(dir_path):
        logger.info('Create directory {}'.format(dir_path))
        os.makedirs(dir_path)
        logger.info('Created directory {}'.format(dir_path))


def _must_section_be_downloaded(cik, save_dir, retry_error_codes=set([])):
    """
    Checks whether the section must be downloaded. It must be downloaded if it was not downloaded before
    or if it was not downloaded successfully and has an error code that is in the list of provided error codes.

    Args:
        cik (str): The CIK code for which to download the section.
        save_dir (str): Saving directory of the result.
        retry_error_codes (set of ints): A set of error codes that should be downloaded again.

    Returns:
        True, if the section must be downloaded.
    """
    logger.info('Check whether the section must be downloaded.')
    file_path = '{}/{}.json'.format(save_dir, cik)
    must_be_downloaded = not os.path.isfile(file_path)
    if not must_be_downloaded:
        logger.info('The section was already downloaded, check if we need to download it again.')
        with open(file_path) as json_file:
            data = json.load(json_file)
            must_be_downloaded = data['code'] in retry_error_codes
            if must_be_downloaded:
                logger.info('We must download the section again.')
            else:
                logger.info('We do not need to download the section again.')
    else:
        logger.info('The section was not downloaded yet. Thus, we must download it now.')
    return must_be_downloaded


def _download_section(cik, date, save_dir):
    """
    Downloads the latest section for a given CIK code and date.

    Args:
        cik (str): The CIK code for which to download the section.
        date (str): The date for which to download the section (format YYYYMMDD).
        save_dir (str): Saving directory of the result.
    """
    # Create the result object
    extraction_result = ExtractionResult()
    # Create filing crawler
    crawler = EdgarFilingCrawler(10)
    year = date[:4]
    logger.info('Request filing list for CIK {} and year {}'.format(cik, year))
    # we request the 10 latest links because sometimes the filings include amend files
    request_result = crawler.get_latest_filing_links(cik, date, '10-K', count=10)
    time.sleep(1) # sleep for one second before the next request
    if not request_result.success:
        logger.warning('Request was not successful for CIK {} and year {}. Message: {}'.format(cik, year, request_result.message))
    else:
        logger.info('Request was successful')
        link_list = request_result.result
        if len(link_list) > 0:
            logger.info('Request filing for CIK {} and year {}'.format(cik, year))
            logger.debug(link_list[0])
            filing_result = crawler.get_filing(link_list[0])
            time.sleep(1) # sleep for one second before the next request
            if not filing_result.success:
                logger.warning('Request was not successful for CIK {} and year {}. Message: {}'.format(cik, year, filing_result.message))
            else:
                logger.info('Request was successful')
                logger.info('Extract section')
                extraction_result = extract_section(filing_result.result)
                if not extraction_result.extracted:
                    logger.warning('Extraction was not successful for CIK {} and year {}. Message: {}'.format(cik, year, extraction_result.message))
                else:
                    logger.info('Extracted section')
            extraction_result.url = link_list[0]
        else:
            logger.warning('No links for CIK {} in year {}'.format(cik, year))
    # save the result
    logger.info('Save result')
    extraction_result.cik = cik
    extraction_result.year = year
    file_path = '{}/{}.json'.format(save_dir, cik)
    with open(file_path, 'w') as outfile:
        json.dump(extraction_result.to_dict(), outfile)
    logger.info('Saved result ({})'.format(file_path))


def main(pickled_cik_dict_path, save_path, retry_error_codes):
    """
    Main function that requests the filings for each cik in the pickled cik dictionary for each given year.
    Also extracts the MD&A section and saves the result as a json-file.

    Args:
        pickled_cik_dict_path (str): The path to the pickled file that contains a dictionary of years and cik codes.
        save_path (str): The path where the json-files will be saved.
        retry_error_codes (list of ints): A list of error codes that should be downloaded again.
    """
    logger.info("Read the year-cik dictionary")
    # read the year cik dictionary
    with open(pickled_cik_dict_path, 'rb') as f:
        year_cik_dict = pickle.load(f)
    logger.info("Readed the year-cik dictionary")
    # download all the sections
    for year, cik_list in year_cik_dict.items():
        save_year_path = '{}/{}'.format(save_path, year)
        _create_directory(save_year_path)
        year_end_date = '{}1231'.format(year)
        for cik in cik_list:
            cik = "{:010d}".format(int(cik))
            if _must_section_be_downloaded(cik, save_year_path, set(retry_error_codes)):
                _download_section(cik, year_end_date, save_year_path)    


if __name__ == "__main__":
    # checks the provided arguments
    if (len(sys.argv) == 2 and (sys.argv[1] == "-h" or sys.argv[1] == "--help")):
        print("Usage example: python3 extract_sections.py /Users/kdoennebrink/Repositories/bankruptcy/data/Eikon/CIK_year.txt /Users/kdoennebrink/Documents/ExtractedData")
        sys.exit(0)
    if (len(sys.argv) < 3):
        print("Wrong arguments! Please provide a FULL path to the data (pickled cik file) and an output folder for the extracted sections. Optional you can define a list of error codes that must be downloaded again. Usage example: python3 extract_sections.py /Users/kdoennebrink/Repositories/bankruptcy/data/Eikon/CIK_year.txt /Users/kdoennebrink/Documents/ExtractedData")
        sys.exit(1)
    
    read_path = sys.argv[1]
    save_path = sys.argv[2]
    retry_error_codes = []
    for i in range(3, len(sys.argv)):
        retry_error_codes.append(int(sys.argv[i]))

    # create output path
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('{}/extract_sections.log'.format(save_path))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # start
    logger.info('Start the extraction')
    main(read_path, save_path, retry_error_codes)
    logger.info('Finished the extraction')