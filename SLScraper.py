import requests
from bs4 import BeautifulSoup
import PyPDF2
import re
from FileManager import write_data_into_excel, create_output_dir

class SLScraper:

    def __init__(self):

        self.BASE_URL = "https://www.southlaw.com"

        self.SL_DOWNLOAD_URL = self.BASE_URL + "/download/"

        self.file_names = list()

        self.data = {
                    "Trustee": [],
                    "Sale Date": [],
                    "Sale Time": [],
                    "Continued Date/Time":[],
                    "County": [],
                    "Civil Case No.": [],
                    "Firm File#": [],
                    "Opening Bid": [],
                    "Property Address": [],
                    "Property City": [],
                    "Property Zip": [],
                    "Sale Location":[]
                    }
    
        self.keys = ["Property Address", "Property City", "Property Zip", "Sale Date", "Sale Time", "Continued Date/Time", "Opening Bid", "Sale Location", "Civil Case No.","Firm File#"]
        
        self.output_directory_name = "SL-Scraper-Output"

        create_output_dir(self.output_directory_name)

    def scrape(self):

        response = requests.get(self.SL_DOWNLOAD_URL)

        soup = BeautifulSoup(response.text, 'html.parser')

        files_headings = soup.find_all('h4')

        files_links = [self.BASE_URL + heading.find('a')['href'] for heading in files_headings]

        self.download_pdfs(files_links)

        for filename in self.file_names:
            
            self.read_pdfs(filename)
        
        write_data_into_excel("output/" + self.output_directory_name + '/sl_data',self.data)

        return "output/" + self.output_directory_name + '/sl_data.xlsx'
        
    

    def download_pdfs(self, links):

        for lnk in links:
            
            response = requests.get(lnk)

            file_name = "output/" + self.output_directory_name + "/" + lnk.split("/")[-1]

            self.file_names.append(file_name)

            with open(file_name, "wb") as out:

                out.write(response.content)
            


    def update_data(self, record, county):

        self.data["Trustee"].append("SOUTHLAW")
        self.data["County"].append(county)
        for c_index in range(len(self.keys)):
            self.data[self.keys[c_index]].append(record[c_index])


    def read_pdfs(self, filename):

            # Extracting Sales data from pdf of SouthLaw Corp

            with open(filename, "rb") as pdf_file:

                pdf = PyPDF2.PdfReader(pdf_file)

                num_pages = len(pdf.pages)

                for page_num in range(num_pages):

                    page = pdf.pages[page_num]
                    
                    page_lines = page.extract_text().split("\n")[11:-4]

                    record = list()
                    
                    for line_no in range(len(page_lines)):
                        
                        line_parts = page_lines[line_no].split(" ")

                        if line_no == 0: # There is county at first line_no of every page
                            county = page_lines[line_no]

                        if len(line_parts) > 1:

                            if "/" not in line_parts[0]:

                                if re.match('\d', page_lines[line_no].split(" ")[0]): # Check whether the line is property address or not, this will help to identify the start of new record

                                    if len(record) > 0:
                                        current_record = record
                                        if re.match('\D', current_record[-1]):
                                                current_record = current_record[:-1] # Removing heading from record, as it is the heading of next new record. The heading of current record is added first.

                                        if len(current_record) > 0 and len(current_record) < 10: # If there are less no of columns in record than 10, it means a column is missing
                                            
                                            if "/" in current_record[5]:
                                                current_record.insert(8, "")
                                            else:
                                                current_record.insert(5, "")
                                        
                                        if line_no != 1: # If this is line_no 1, then it is not a record
                                            self.update_data(current_record, county)
                                            

                                    # Check whether current line is record heading (county) or not
                                    if re.match('\D', record[-1]):
                                        county = record[-1]
                                        
                                    record = list() # clear the record list for new record
                                
                        elif line_no == len(page_lines) - 1:
                            
                            if len(record) < 10: # If there are less no of columns in record than 10, then it means Continued Date/Time column missing, add empty string in place of it
                                
                                if "/" in record[5]:
                                    record.insert(8, "")
                                else:
                                    record.insert(5, "")
                            
                            # For last line, update record
                            record.append(page_lines[line_no])

                            #Update data
                            self.update_data(record, county)
                        
                                   
                        
                        record.append(page_lines[line_no])
            