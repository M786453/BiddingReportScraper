from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
from FileManager import write_data_into_json, create_output_dir
from selenium.webdriver.chrome.options import Options


class LOGScraper:

    def __init__(self):

        self.data = list()
        
        self.data_keys = ["County", "Sale Date", "Sale Time", "Unique Document Number", "Address", "City", "Opening Bid","Auction Company", "Sale Status", "Foreclosure Status"]
        
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--headless") # Make browser headless
        
        self.driver = webdriver.Chrome(options=options) # Initializing Microsoft's Edge Webdriver

        self.REPORT_URL =  "https://www.logs.com/mo-sales-report.html" # Report Base URL

        self.output_directory_name = "LOG-Scraper-Output"

        create_output_dir(self.output_directory_name)
        
    def scrape(self):

        self.driver.get(self.REPORT_URL)

        time.sleep(5)

        iframe_src = self.driver.find_element(By.TAG_NAME, 'iframe').get_attribute('src')

        self.driver.get(iframe_src)

        time.sleep(20)

        table = self.driver.find_element(By.XPATH, "//div[@class='mid-viewport']")

        table_rows = list(table.find_elements(By.XPATH, ".//div[@role='row']"))

        for row in table_rows:

            row_dict = {
                    "Trustee": "",
                    "Sale Date": "",
                    "Sale Time": "",
                    "Unique Document Number": "",
                    "Address": "",
                    "City": "",
                    "County": "",
                    "Opening Bid": "",
                    "Auction Company":"",
                    "Sale Status": "",
                    "Foreclosure Status": ""
                    }

            row_dict["Trustee"] = "LOGS.COM"

            record_cols = list(row.find_elements(By.XPATH, ".//div[@role='gridcell']"))[1:]

            for col_index in range(len(record_cols)):

                row_dict[self.data_keys[col_index]] = record_cols[col_index].text
            
            self.data.append(row_dict)

        write_data_into_json("output/" + self.output_directory_name + "/log_data", self.data)

        return "output/" + self.output_directory_name + "/log_data.xlsx"

    