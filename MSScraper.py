import requests
import json
import tabula
import pandas as pd
from FileManager import create_output_dir, write_data_into_json

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

        data = dict()

        # Loop through all pages of the PDF and convert them to Excel sheets
        pages = tabula.read_pdf(pdf_file, pages='all')

        categories = list()

        for i, df in enumerate(pages):

            local_data = dict(df.to_dict())

            if i == 0:
                
                for category in local_data:
                    try:
                        
                        data[category] = [local_data[category][key] if type(local_data[category][key]) != type(float()) else "" for key in local_data[category]]
                        categories.append(category)
                    except Exception as e:
                        print("MSScraper:", e)    
            else:
                for category in local_data:
                    try:
                        cat2 = category
                        if category == "Property Address":
                            cat2 = "Continued" # Property address have the same index in data as continued, we only want continued value

                        
                        data[cat2].extend([local_data[category][key] if type(local_data[category][key]) != type(float()) else "" for key in local_data[category]])
                    except Exception as e:
                        print("MSScraper:", e)    

        
        for category in data:

            cleaned_values = list()

            for val in data[category]:

                try:
                    if val != category and val != "Property Address":
        
                        if ("Sale Date" == category or "Continued" == category) and val != None and "/" not in val:
                            val = ""

                        cleaned_values.append(val)
                        
                except Exception as e:
                    print("Below MSScraper:", e)  

            data[category] = list(cleaned_values)

            # format output data
            formatted_data = list()
            max_length = max([len(data[cat]) for cat in data])

            for index in range(max_length):
                row_dict = dict()
                row_dict["Trustee"] = "MS Firm"
                row_dict["PropAddress"] = ""
                row_dict["PropCity"] = ""
                row_dict["PropZip"] = ""

                for cat in categories:
                    
                    try:
                        if cat == "Auction Vendor":
                            row_dict["vendor"] = data[cat][index]
                        elif cat == "Continued":
                            row_dict["continued_date"] = data[cat][index]
                        elif cat == "Bid":
                            row_dict["OpeningBid"] = data[cat][index]
                        elif cat == "Sale Date":
                            s_date = data[cat][index].split(" ")[0]
                            s_time = data[cat][index].split(" ")[1]
                            row_dict["Sale_date"] = s_date
                            row_dict["Sale_time"] = s_time
                        elif cat == "MS File #":
                            row_dict["FileNo"] = data[cat][index]
                        else:
                            row_dict[cat] = data[cat][index]
                    except:
                        row_dict["FileNo"] = ""

                if len(row_dict["FileNo"]) != 0:
                    formatted_data.append(row_dict)

            

        write_data_into_json("output/" + self.output_directory_name +  '/MS',formatted_data)

