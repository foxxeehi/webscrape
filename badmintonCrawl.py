import os
import time
import pandas
import dateConversion
from selenium.webdriver.common.by import By

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def crawl(from_date, to_date, category):
    driver_path = 'c:\\chromedriver\\chromedriver.exe'

    options = Options()
    # options.headless = True
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(options=options, executable_path=driver_path)
    while from_date <= to_date:
        from_date_string = dateConversion.date_to_string(from_date)
        driver.get(
            'https://badmintonstatistics.net/Rankings?date=' + from_date_string + '&category=' + category + '&country=%&page=1&pagesize=100')
        time.sleep(1)
        rows = driver.find_elements(By.XPATH, "//div[@class='reportcontainer']/table/tbody/tr")
        time.sleep(1)
        column_names = rows[0].text.split()
        df = pandas.DataFrame(columns=column_names)
        rows.pop(0)
        for row in rows:
            record = row.text.split()
            rank = record.pop(0)
            points = record.pop()
            category = record.pop()
            # There might be two countries for doubles
            if record[len(record) -1] is in country.

            country = record.pop()
            player = " ".join(record)
            record = [rank, player, country, category, points]
            df.loc[len(df.index)] = record
        print(df)
        path = os.getcwd() + "\\csv\\badminton\\" + category + "\\"
        df.to_csv(path + from_date_string + ".csv")
        from_date = dateConversion.date_adding(from_date, 7)
    driver.quit()
