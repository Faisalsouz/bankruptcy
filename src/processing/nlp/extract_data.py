import re, os
import sys

text_start = re.compile(r"(?<=href)(((?!href=)[\s\S])*?(discussion\s+and\s+analysis[\s\S]*?))(?=>)")
text_end = re.compile(r"(?<=href)(((?!href=)[\s\S])*?(quantitative[\s\S]*?))(?=>)")

# regex for extracting the timestamp
date_regex_t = re.compile(r"date as of change:\s*(\d*)")
# regex to check file type: amends should be excluded since they
# do not contain the relevant section
amend_regex = re.compile(r"conformed\submission\stype:\s*10-k/a")


'''
Folder structure:

_Company CIK
|
-- SEC access number
	|
	-- 10K
		|
		-- SEC access number - yy - xxx.txt
	|
	-- 10Q
		|
		--- SEC access number - yy - xxx.txt

'''


def extract_data(read_path, save_path):
	"""
    Extracts the relevant MD&A sections from the 10-K/10-Q forms
    :param read_path: path to the data folder
    :param save_path: path to folder in which the extracted data should be saved
    """

	# save log file on same level as folders of the extracted data (not in the folder!)
	log_path = "{}/log.txt".format(save_path[:save_path.rfind("/", 0, len(save_path)-1)])
	# clean log file on start
	open(log_path, 'w').close()
	
	for cik in os.listdir(read_path): # cik = folder with company specific files
		if (cik[0] == '.'):
			continue	
		for d in os.listdir(read_path + cik): # d = directory with short SEC access number
			if (d[0] == '.'):
				continue	
			for subdir in os.listdir(read_path + cik + "/" + d): # subdir = either 10k or 10q
				if (subdir[0] == '.'):
					continue
				for data_dir in os.listdir(read_path + cik + "/" + d + "/" + subdir): # text files
					if (data_dir[0] == '.'):
						continue

					filepath = read_path + cik + "/"  + d + "/" + subdir + "/" + data_dir
					try:
						# read in file and avoid complications by making everything lowercase
						file = open(filepath, 'rb').read().decode('utf-8').lower()

						# exclude amend files
						filetype = re.search(amend_regex, file)
						if (filetype):
							continue

						# look for the date
						date_matches = re.search(date_regex_t, file)

						href_start = re.search(r"(\"|')[\s\S]*?(\"|')", re.search(text_start, file).group()).group()[2:-1]
						href_end = re.search(r"(\"|')[\s\S]*?(\"|')", re.search(text_end, file).group()).group()[2:-1]
						

						data_regex = re.compile(r"name=" + r"\"" + \
							re.escape(href_start) + r"(?!" + href_start + \
							r")[\s\S]*?(?=name="+ r"\"" + re.escape(href_end) +r")")
						
						# if a match was found, start cleaning the section from html tags
						match = re.search(data_regex, file)
						if (match): 
							file = match.group() # match is a tuple -> join will make it a string
							####
							# CLEAN THE SECTIONS FROM UNNECESSARY CONTENT
							####
							file = re.sub(r"<table.*?</table>", "", file); # remove tables
							file = re.sub(r"italic.*?(?=</font)", "", file); # remove bold text and legends/notes
							file = re.sub(r"underline.*?(?=</font)", "", file); # remove underlined text
							file = re.sub(r"<.*?(?=>)", "", file); # remove html tags 
							file = re.sub(r"&[^;]*;", "", file); # remove html links/placeholder
							file = re.sub(r"\n+", "", file) # remove newlines
							file = re.sub(r"&[^;]*;", "", file); # remove html links/placeholder
							file = re.sub(r">+", " ", file); # remove unnecessary '>' around numbers
							file = re.sub(r"table of contents", "", file); # remove leftovers referencing the table of contents
							
							# save results in file (name format CIK_date.txt)
							out_file = open("{}/{}/{}_{}.txt".format(save_path, subdir, cik, date_matches.group(1)), "w") 
							out_file.write(file)
							out_file.close()

					except:
						# save filenames that were not be able to be processed
						log_file = open(log_path, "a") 
						log_file.write("{}/{}_{}\n".format(subdir, cik, date_matches.group(1)))
						log_file.close()



if __name__ == "__main__":
	# check provided args via command line
	# in case there are 3 arguments (python script path, read and destionation path)
	if len(sys.argv) < 2:
		print("Missing arguments! \nPlease provide a FULL path to the data directory and an optional destination folder for the extracted files.\n"\
			"\nUsage example: python3 extract_data.py /Users/Anna/Documents/Data/ /Users/Anna/Documents/ExtractedData/\n")
		sys.exit(1)
	if (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
		print("\nUsage example: python3 extract_data.py /Users/Anna/Documents/Data/ /Users/Anna/Documents/ExtractedData/\n")
		sys.exit(0)

	read_path = ""
	save_path = ""

	if (len(sys.argv) == 2):
		read_path = sys.argv[1]
		save_path = read_path[:read_path.rfind("/", 0, len(read_path)-1)] + "/ExtractedData/"
		print("No destination folder provided. Extracted data will be saved in {}".format(save_path))
	elif (len(sys.argv) == 3):
		read_path = sys.argv[1]
		save_path = sys.argv[2]

	extract_data(read_path, save_path)
