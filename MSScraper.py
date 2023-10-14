import requests
import json
import tabula
import pandas as pd
from FileManager import create_output_dir

class MSScraper:

    def __init__(self):
        
        self.MS_PDF_URL = "https://www.msfirm.com/bids/bidsonline.pdf"

        self.output_directory_name = "MS-Scraper-Output"

        create_output_dir(self.output_directory_name)


    def scrape(self):

        pdf_response = requests.get(self.MS_PDF_URL)

        with open("output/" + self.output_directory_name + "/MS.pdf", "wb") as ms:
            ms.write(pdf_response.content)
        
        self.pdf_to_excel()
    
        return "output/" + self.output_directory_name + '/output.xlsx'
    
    def pdf_to_excel(self):

        # Read the PDF file
        pdf_file = "output/" + self.output_directory_name +  '/MS.pdf'

        # Create an empty Excel writer object
        excel_writer = pd.ExcelWriter("output/" + self.output_directory_name + '/output.xlsx', engine='xlsxwriter')

        # Loop through all pages of the PDF and convert them to Excel sheets
        pages = tabula.read_pdf(pdf_file, pages='all')

        for i, df in enumerate(pages):
            df.to_excel(excel_writer, sheet_name=f'Page_{i+1}', index=False)

        # Save the Excel file
        excel_writer._save()