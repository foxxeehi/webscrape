import os
import time
import pandas
import dateConversion
from selenium.webdriver.common.by import By
import country as cy

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def find_country_and_player(target_string_list):
    first_half = ""
    country_and_player_map = {}
    countries = []
    players = []
    country_map_keys = cy.get_country_map().keys()
    for possible_country_piece in target_string_list:
        if first_half != "":
            if possible_country_piece in country_map_keys:
                countries.append(possible_country_piece)
                if first_half != "/":
                    players.append(first_half)
                first_half = ""
                continue

            possible_country = first_half + " " + possible_country_piece
            if possible_country in country_map_keys:
                countries.append(possible_country)
                first_half = ""
                continue
            else:
                players.append(first_half)
                first_half = possible_country_piece
                continue

        if possible_country_piece == "/":
            countries.append(possible_country_piece)
            continue
        if possible_country_piece in country_map_keys:
            countries.append(possible_country_piece)
            continue
        first_half = possible_country_piece

    country_and_player_map["countries"] = countries
    country_and_player_map["players"] = players
    return country_and_player_map

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
            country_player_map = find_country_and_player(record)
            player = " ".join(country_player_map["players"])
            country = " ".join(country_player_map["countries"])
            record = [rank, player, country, category, points]
            df.loc[len(df.index)] = record
        print(df)
        path = os.getcwd() + "\\csv\\badminton\\" + category + "\\"
        df.to_csv(path + from_date_string + ".csv")
        from_date = dateConversion.date_adding(from_date, 7)
    driver.quit()