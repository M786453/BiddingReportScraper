from flask import Flask, send_file
from ATScraper import ATScraper
from CTScraper import CTScraper
from EPScraper import EPScraper
from LOGScraper import LOGScraper
from MSScraper  import MSScraper 
from SLScraper  import SLScraper 
import schedule
from threading import Thread
import time

app = Flask(__name__)

@app.route('/at')
def at_scraper():
    
    return send_file("output/AT-Scraper-Output/at_data.xlsx")

@app.route('/ct')
def ct_scraper():

    return send_file("output/CT-Scraper-Output/ct_data.xlsx")


@app.route('/ep')
def ep_scraper():

    return send_file("output/EP-Scraper-Output/ep_data.xlsx")


@app.route('/log')
def log_scraper():

    return send_file("output/LOG-Scraper-Output/log_data.xlsx")

@app.route('/ms')
def ms_scraper():

    return send_file('output/MS-Scraper-Output/output.xlsx')

@app.route('/sl')
def sl_scraper():

    return send_file('output/SL-Scraper-Output/sl_data.xlsx')

def scraping():
    try:
        ATScraper().scrape()
    except Exception as e:
        print("ATScraper:", e)

    try:
        CTScraper().scrape()
    except Exception as e:
        print("CTScraper:", e)

    try:
        EPScraper().scrape()
    except Exception as e:
        print("EPScraper:", e)

    try:
        LOGScraper().scrape()
    except Exception as e:
        print("LOGScraper:", e)

    try:
        MSScraper().scrape()
    except Exception as e:
        print("MSScraper:", e)

    try:
        SLScraper().scrape()
    except Exception as e:
        print("SLScraper:",e)

def scraping_thread():

    Thread(target=scraping).start()

def schedule_script():
    while True:
        schedule.run_pending()
        time.sleep(1)

schedule.every().day.at("01:00").do(scraping_thread) # Run everyday at 1:00AM

if __name__ == "__main__":
    Thread(target=scraping_thread).start()
    Thread(target=schedule_script).start()
    app.run()