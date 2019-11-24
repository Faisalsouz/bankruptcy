import requests
from crawler import EdgarFilingCrawler
import re
import os
import sys
import pickle
import logging
import json

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
date_regex_t = re.compile(r"date as of change:\s*(\d*)") # extracting the timestamp
amend_regex = re.compile(r"conformed\ssubmission\stype:\s*10-k/a") # regex to check file type: amends should be excluded since they do not contain the relevant section
text_start = re.compile(r"(?<=href)(((?!href=)[\s\S])*?(discussion\s+and\s+analysis[\s\S]*?))(?=>)")
text_end = re.compile(r"(?<=href)(((?!href=)[\s\S])*?(quantitative\s+and\s+qualitative[\s\S]*?))(?=>)")

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
    message = ''
    # to avoid later problems we transform everything to lower case
    full_text = full_text.lower()
    # check if the filling is of type amend
    is_amend = re.search(amend_regex, full_text)
    if is_amend:
        logging.debug('Form is an amend file and therefore not processed.')
        message = _add_to_string(message, 'Form is an amend file and therefore not processed.')
    else:
        try:
            # look for the date
            date_matches = re.search(date_regex_t, full_text)
            message = _add_to_string(message, 'Date of filing: {}'.format(date_matches.group(1)))
            # find the section
            href_start = re.search(r"(\"|')[\s\S]*?(\"|')", re.search(text_start, full_text).group()).group()[2:-1]
            href_end = re.search(r"(\"|')[\s\S]*?(\"|')", re.search(text_end, full_text).group()).group()[2:-1]
            data_regex = re.compile(r"((name|id)=\"" + re.escape(href_start) + r"(?!" + re.escape(href_start) + r")[\s\S]*?(?=(name|id)=\"" + re.escape(href_end) +r"))")		    	
            # if a match was found, start cleaning the section from html tags
            match = re.search(data_regex, full_text)
            if match: 
                logging.info('MD&A section was found')
                extracted = True
                section = match.group() # match is a tuple -> join will make it a string
                section = _clean_section(section)
            else: 
                logging.warning('MD&A section was not found')
        except:
            logging.error('Error during extraction: {}'.format(sys.exc_info()[0]))


    return ExtractionResult(extracted, section, message)


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
    cik = None
    year = None
    form_type = None
    url = None

    def __init__(self, extracted, section, message=''):
        """
        Initializes a new instance.
        
        Args:
            extracted: A boolean value indicating whether the extraction was successful.
            section: The extracted section.
            message: The message to set.
        """
        self.extracted = extracted
        self.section = section
        self.message = message

    
    def to_dict(self):
        """
        Creates a dictionary from itself.

        Returns:
            A dictionary with the current status of the object.
        """
        status_dict = {
            "extracted": self.extracted,
            "message": self.message,
            "section": self.section,
            "CIK": self.cik,
            "year": self.year,
            "form_type": self.form_type,
            "url": self.url
        }
        return status_dict


def main(pickled_cik_dict_path, save_path):
    """
    Main function that requests the filings for each cik in the pickled cik dictionary for each given year.
    Also extracts the MD&A section and saves the result as a json-file.

    Args:
        pickled_cik_dict_path (str): The path to the pickled file that contains a dictionary of years and cik codes.
        save_path (str): The path where the json-files will be saved.
    """
    logging.info("Read the year-cik dictionary")
    # read the year cik dictionary
    with open(pickled_cik_dict_path, 'rb') as f:
        year_cik_dict = pickle.load(f)
    logging.info("Readed the year-cik dictionary")
    
    # Create filing crawler
    crawler = EdgarFilingCrawler(10)

    for year, cik_list in year_cik_dict:
        save_year_path = '{}/{}'.format(save_path, year)
        if not os.path.exists(save_year_path):
            logging.info('Create output directory {}'.format(save_year_path))
            os.makedirs(save_year_path)
            logging.info('Created output directory {}'.format(save_year_path))
        year_end_date = '{}1231'.format(year)
        for cik in cik_list:
            cik = "{:010d}".format(cik)
            logging.info('Request filing list for CIK {} and year {}'.format(cik, year))
            request_result = crawler.get_latest_filing_links(cik, year_end_date, '10-K')
            if not request_result.success:
                logging.warning('Request was not successful for CIK {} and year {}. Message: {}'.format(cik, year, request_result.message))
            else:
                logging.info('Request was successful')
                link_list = request_result.result
                if len(link_list) > 0:
                    logging.info('Request filing for CIK {} and year {}'.format(cik, year))
                    filing_result = crawler.get_filing(link_list[0])
                    if not filing_result.success:
                        logging.warning('Request was not successful for CIK {} and year {}. Message: {}'.format(cik, year, filing_result.message))
                    else:
                        logging.info('Request was successful')
                        logging.info('Extract section')
                        extraction_result = extract_section(filing_result.result)
                        if not extraction_result.extracted:
                            logging.warning('Extraction was not successful for CIK {} and year {}. Message: {}'.format(cik, year, extraction_result.message))
                        else:
                            logging.info('Extracted section')
                            logging.info('Save section')
                            extraction_result.cik = cik
                            extraction_result.year = year
                            extraction_result.url = link_list[0]
                            extraction_result.form_type = "10-K"
                            file_path = '{}/{}.json'.format(save_year_path, cik)
                            with open(file_path, 'w') as outfile:
                                json.dump(extraction_result.to_dict(), outfile)
                            logging.info('Saved section ({})'.format(file_path))
                else:
                    logging.warning('No links for CIK {} in year {}'.format(cik, year))


    # TODO: Request filing
    # TODO: Extract MD&A section
    # TODO: Save result
    


if __name__ == "__main__":
    # checks the provided arguments
    if len(sys.argv) != 3:
        print("Wrong arguments! Please provide a FULL path to the data (pickled cik file) and an output folder for the extracted sections. Usage example: python3 extract_section.py /Users/Kai/Repositories/bankruptcy/data/Eikon/CIK_year.txt /Users/Kai/Documents/ExtractedData")
        sys.exit(1)
    if (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
        print("Usage example: python3 extract_section.py /Users/Kai/Repositories/bankruptcy/data/Eikon/CIK_year.txt /Users/Kai/Documents/ExtractedData")
        sys.exit(0)
    
    read_path = sys.argv[1]
    save_path = sys.argv[2]

    # create file handler which logs even debug messages
    fh = logging.FileHandler('{}/extract_sections.log'.format(save_path))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    fh.setFormatter(formatter)

    # start
    logging.info('Start the extraction')
    main(read_path, save_path)
    logging.info('Finished the extraction')