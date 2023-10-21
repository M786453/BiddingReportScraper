import requests
from bs4 import BeautifulSoup
import json
from FileManager import write_data_into_json, create_output_dir

class ATScraper:

    def __init__(self):
        
        self.AT_UPCOMMING_SALES_URL = "https://www.armstrongteasdale.com/upcoming-sales/"

        self.data = {
                    "Trustee": [],
                    "Sale Date": [],
                    "Sale Time": [],
                    "Name": [],
                    "Case": [],
                    "Property Address": [],
                    "City": [],
                    "County": [],
                    "Bid Amount": []
                    }
        
        self.data_keys = {
                        "Sale Date":"col-date", 
                        "Sale Time":"col-time", 
                        "Name":"col-name",
                        "Case":"col-case", 
                        "Property Address":"col-address", 
                        "City":"col-city",
                        "County":"col-county",
                        "Bid Amount": "col-bid"
                        }
        
        self.output_directory_name = "AT-Scraper-Output"

        create_output_dir(self.output_directory_name)
    
    def scrape(self):

        response = requests.get(self.AT_UPCOMMING_SALES_URL)

        soup = BeautifulSoup(response.text, "html.parser")

        table_body = soup.find('tbody')

        table_rows = table_body.find_all('tr')

        for row in table_rows:

            self.data["Trustee"].append("AT, INC")

            for key_1,key_2 in self.data_keys.items():

                self.data[key_1].append(row.find('td', {'class': key_2}).text)
            
        write_data_into_json("output/" + self.output_directory_name + "/at_data", self.data)

        return "output/" + self.output_directory_name + "/at_data.xlsx"
