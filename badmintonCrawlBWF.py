import os
import time
from datetime import datetime

import pandas
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import dateConversion
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options
from selenium import webdriver


def crawl(category, category_full_name):
    driver_path = 'c:\\chromedriver\\chromedriver.exe'

    options = Options()
    # options.headless = True
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(options=options, executable_path=driver_path)
    # while from_date <= to_date:
    driver.get('https://bwfbadminton.com/rankings/')
    time.sleep(1)
    # WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, "//div[text()='BWF World Rankings']"))).click()
    # WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, "//div[text()='BWF World Tour Rankings']"))).click()
    # Click the Per Page dropdown to make the list visible

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[text()=10]"))).click()
    # Choose the option in the list
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[text()=100]"))).click()
    time.sleep(1)

    current_week = 'Week 9 (2022-03-01)'
    week_list = ['Week 47 (2021-11-23)', 'Week 48 (2021-11-30)', 'Week 49 (2021-12-07)',
                 'Week 50 (2021-12-14)', 'Week 51 (2021-12-21)', 'Week 52 (2021-12-28)', 'Week 1 (2022-01-04)',
                 'Week 2 (2022-01-11)', 'Week 3 (2022-01-18)', 'Week 4 (2022-01-25)', 'Week 5 (2022-02-01)',
                 'Week 6 (2022-02-08)', 'Week 7 (2022-02-15)', 'Week 8 (2022-02-22)', 'Week 9 (2022-03-01)']
    for week in week_list:

        # Click the Ranking dropdown to make the list visible
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()=" + "\"" + current_week + "\"" + "]"))).click()
        # Choose the option in the list
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()=" + "\"" + week + "\"" + "]"))).click()
        time.sleep(1)
        # Choose the option in the list
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()=\"" + category_full_name + "\"]"))).click()
        time.sleep(3)

        current_week = week
        column_names = ["Rank", "Players", "Country", "Category", "Points"]
        # ranking_event = driver.find_elements(By.XPATH, "//span[@class='ranking-tab-mobile']")
        rows = driver.find_elements(By.XPATH, "//div[@class='wrapper-ranking']/table/tbody/tr")
        df = pandas.DataFrame(columns=column_names)
        for row in rows:
            record = row.text.split("\n")
            rank = record[0]
            points = record[3].split().pop()
            country = "-"
            player = record[2]
            record = [rank, player, country, category, points]
            df.loc[len(df.index)] = record
        path = os.getcwd() + "\\csv\\badminton\\" + category + "\\"
        current_week_without_week_text = current_week.split(" ")[2]
        current_week_without_week_text = current_week_without_week_text.replace("(", "").replace(")", "")
        df.to_csv(path + current_week_without_week_text + ".csv")
    driver.quit()
