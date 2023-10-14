import pandas as pd
import os

def write_data_into_excel(filename,data):
            df = pd.DataFrame(data)
            writer = pd.ExcelWriter(filename + '.xlsx', engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Sheet1', index=False)
            writer._save()

def create_output_dir(bot_name):
    
    if not os.path.exists("output"):
        os.mkdir("output")
    
    if not os.path.exists("output/"+bot_name):
        os.mkdir("output/"+bot_name)
    
