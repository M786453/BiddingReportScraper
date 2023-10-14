import requests
from bs4 import BeautifulSoup
import json
from FileManager import write_data_into_excel, create_output_dir

class CTScraper:

    def __init__(self):

        self.CT_URL = "https://www.centretrustee.com/listproperties.php"

        self.data = {
                    "Trustee": [],
                    "Sale Date": [],
                    "Sale Time": [],
                    "County": [],
                    "File Number": [],
                    "Address": [],
                    "Opening Bid": [],
                    "Comments": []
                    }
        
        self.data_keys = ["Sale Date", "Sale Time", "County", "File Number", "Address", "Opening Bid", "Comments"]

        self.output_directory_name = "CT-Scraper-Output"

        create_output_dir(self.output_directory_name)

    def scrape(self):

        response = requests.get(self.CT_URL)
        
        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find_all('table')[1]

        table_rows = list(table.find_all('tr'))[1:]

        for row in table_rows:

            self.data["Trustee"].append("CENTRE TRUSTEE CORP")

            cols = row.find_all('td')

            for c_index in range(len(cols)):
                self.data[self.data_keys[c_index]].append(cols[c_index].text.strip().replace('\xa0',' '))
        
        # Writing data into excel
        write_data_into_excel("output/" + self.output_directory_name + "/ct_data", self.data) 

        return "output/" + self.output_directory_name + "/ct_data.xlsx"



