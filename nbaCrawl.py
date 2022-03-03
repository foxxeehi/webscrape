import os
import time

import pandas
from selenium.webdriver.common.by import By

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def crawl(from_season, to_season):
    driver_path = 'c:\\chromedriver\\chromedriver.exe'

    options = Options()
    # options.headless = True
    options.add_argument("--window-size=1920,1200")

    driver = webdriver.Chrome(options=options, executable_path=driver_path)
    while from_season < to_season:
        next_season = from_season + 1
        season = str(from_season) + "-" + str(next_season)[2] + str(next_season)[3]
        driver.get(
            'https://www.nba.com/stats/leaders/?Season=' + season + '&SeasonType=Regular%20Season&PerMode=Totals')
        pages = driver.find_elements(By.XPATH, "//div[@class='stats-table-pagination__info']/select/option")
        time.sleep(1)
        numbers_of_page = int(len(pages) / 2) - 1
        column_names = []
        columns = driver.find_elements(By.XPATH, "//div[@class='nba-stat-table__overflow']/table/thead/tr/th")
        time.sleep(1)
        for column in columns:
            column_names.append(column.text)
        print("after append")
        while "" in column_names:
            column_names.remove("")
        print("after remove")
        df = pandas.DataFrame(columns=column_names)
        for i in range(numbers_of_page):
            rows = driver.find_elements(By.XPATH, "//div[@class='nba-stat-table__overflow']/table/tbody/tr")
            time.sleep(1)
            print("after sleep")
            for row in rows:
                record = row.text.split("\n")
                index = record[0]
                player_name = record[1]
                data = record[2].split()
                data.insert(0, index)
                data.insert(1, player_name)
                for index in range(len(data)):
                    if data[index] == "-":
                        data[index] = 0
                while len(data) < len(column_names):
                    data.append(0)
                df.loc[len(df.index)] = data
            driver.find_element(By.XPATH, "//a[@class='stats-table-pagination__next']").click()
        print(df)
        path = os.getcwd() + "\\csv\\all\\"
        df.to_csv(path + season + ".csv")
        from_season = from_season + 1
    driver.quit()
