import time
import pandas
import country
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


def crawl(from_year=2007, to_year=2022):
    driver_path = 'c:\\chromedriver\\chromedriver.exe'
    options = Options()
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(options=options, executable_path=driver_path)
    padding_count = [0]
    player_title_count_map = {}
    column_name_list = ["country", "image", "player"]
    men_single_df = pandas.DataFrame(columns=column_name_list)
    olympic_years = [2008, 2012, 2016, 2020]
    while from_year <= 2017:
        # Super Series
        driver.get(
            'https://en.wikipedia.org/wiki/' + str(from_year) + '_BWF_Super_Series')
        crawl_superseries_goldprix(driver, from_year, padding_count, player_title_count_map,
                                   men_single_df)
        # GrandPrix Series
        driver.get(
            'https://en.wikipedia.org/wiki/' + str(from_year) + '_BWF_Grand_Prix_Gold_and_Grand_Prix')
        crawl_superseries_goldprix(driver, from_year, padding_count, player_title_count_map,
                                   men_single_df)
        # Olympic world championship
        if from_year in olympic_years:
            driver.get(
                'https://en.wikipedia.org/wiki/' + 'Badminton_at_the_' + str(from_year) + '_Summer_Olympics')
            crawl_olympic_and_championship(driver, from_year, padding_count, player_title_count_map,
                          men_single_df)
        else:
            driver.get(
                'https://en.wikipedia.org/wiki/' + str(from_year) + '_BWF_World_Championships')
            crawl_olympic_and_championship(driver, from_year, padding_count, player_title_count_map,
                                           men_single_df)
        from_year = from_year + 1
    while from_year <= to_year:
        # World Tour Super
        driver.get(
            'https://en.wikipedia.org/wiki/' + str(from_year) + '_BWF_World_Tour')
        crawl_world_tour(driver, from_year, padding_count, player_title_count_map,
                         men_single_df)
        # Olympic and world championship
        if from_year in olympic_years:
            driver.get(
                'https://en.wikipedia.org/wiki/' + 'Badminton_at_the_' + str(from_year) + '_Summer_Olympics')
            crawl_olympic_and_championship(driver, from_year, padding_count, player_title_count_map,
                                           men_single_df)
        else:
            if from_year == 2022:
                continue
            driver.get(
                'https://en.wikipedia.org/wiki/' + str(from_year) + '_BWF_World_Championships')
            crawl_olympic_and_championship(driver, from_year, padding_count, player_title_count_map,
                                           men_single_df)
        from_year = from_year + 1
    men_single_df.to_csv("MS_title" + ".csv")
    driver.quit()


def crawl_superseries_goldprix(driver, from_year, padding_count, player_title_count_map, men_single_df):
    time.sleep(1)
    schedule_table = driver.find_elements(By.XPATH, "//div[@class='mw-parser-output']/table[@class='wikitable']")[0]
    schedule_table_body = schedule_table.find_element_by_tag_name("tbody")
    schedule_rows = schedule_table_body.find_elements_by_tag_name("tr")
    schedule_rows.pop(0)  # get rid of title row
    schedule_rows.pop(0)  # get rid of start and finish
    result_table = driver.find_elements(By.XPATH, "//div[@class='mw-parser-output']/table[@class='wikitable']")[1]
    table_body = result_table.find_element_by_tag_name("tbody")
    tour_rows = table_body.find_elements_by_tag_name("tr")
    tour_rows.pop(0)  # get rid of title row
    time.sleep(1)
    index = 0
    for tour in tour_rows:
        schedule_elements = schedule_rows[index].find_elements_by_tag_name("td")
        title = schedule_elements[1].text
        elements = tour.find_elements_by_tag_name("td")
        revised_tour_name = str(from_year) + " " + title
        player = elements[1].text
        country_name = elements[1].find_element_by_tag_name("span").find_element_by_tag_name("a").accessible_name
        country_image = country.get_country_image(country_name)
        # update player_title_count_map
        if player in player_title_count_map:
            player_title_count_map[player] = player_title_count_map[player] + 1
        else:
            player_title_count_map[player] = 1
        if player not in men_single_df["player"].tolist():
            # add new player
            new_player = [country_name, country_image, player]
            for i in range(padding_count[0]):
                new_player.append(0)
            men_single_df.loc[len(men_single_df.index)] = new_player
        # add new tour column
        new_column_values = []
        for player in men_single_df["player"]:
            new_column_values.append(player_title_count_map[player])
        men_single_df[revised_tour_name] = new_column_values
        padding_count[0] = padding_count[0] + 1
        index = index + 1


def crawl_world_tour(driver, from_year, padding_count, player_title_count_map, men_single_df):
    result_tables = driver.find_elements(By.XPATH, "//div[@class='mw-parser-output']/table[@class='wikitable']")
    for table in result_tables:
        table_body = table.find_element_by_tag_name("tbody")
        tour_rows = table_body.find_elements_by_tag_name("tr")
        schema = tour_rows.pop(0)  # get rid of title row
        columns = schema.find_elements_by_tag_name("th")
        # check if the table is the tournament table
        if len(columns) < 1:
            continue
        else:
            first_column = schema.find_element_by_tag_name("th").text
            if first_column != "Date":
                continue
        time.sleep(1)
        index = 0
        while index < len(tour_rows):
            elements = tour_rows[index].find_elements_by_tag_name("td")
            # The first tournament in the date
            if len(elements) == 4:
                # check if the tournament is canceled or not by checking player's name
                if len(elements[2].find_elements_by_tag_name("a")) < 1:
                    index = index + 10
                    continue
                if from_year >= 2020:
                    tour_name = elements[1].find_elements_by_tag_name("a")[2].get_attribute("title")
                else:
                    tour_name = elements[1].find_elements_by_tag_name("a")[1].get_attribute("title")
                player = elements[2].find_elements_by_tag_name("a")[1].get_attribute("title")
                country_name = elements[2].find_elements_by_tag_name("a")[0].get_attribute("title")
                country_image = country.get_country_image(country_name)
            # The second - last tournament in the date
            if len(elements) == 3:
                if len(elements[1].find_elements_by_tag_name("a")) < 1:
                    index = index + 10
                    continue
                if from_year >= 2020:
                    tour_name = elements[0].find_elements_by_tag_name("a")[2].get_attribute("title")
                else:
                    tour_name = elements[0].find_elements_by_tag_name("a")[1].get_attribute("title")
                player = elements[1].find_elements_by_tag_name("a")[1].get_attribute("title")
                country_name = elements[1].find_elements_by_tag_name("a")[0].get_attribute("title")
                country_image = country.get_country_image(country_name)
            # update player_title_count_map
            if player in player_title_count_map:
                player_title_count_map[player] = player_title_count_map[player] + 1
            else:
                player_title_count_map[player] = 1
            if player not in men_single_df["player"].tolist():
                # add new player
                new_player = [country_name, country_image, player]
                for i in range(padding_count[0]):
                    new_player.append(0)
                men_single_df.loc[len(men_single_df.index)] = new_player
            # add new tour column
            new_column_values = []
            for player in men_single_df["player"]:
                new_column_values.append(player_title_count_map[player])
            men_single_df[tour_name.replace(" (badminton)", "")] = new_column_values
            padding_count[0] = padding_count[0] + 1
            index = index + 10


def crawl_olympic_and_championship(driver, from_year, padding_count, player_title_count_map, men_single_df):
    result_table = driver.find_element(By.XPATH, "//div[@class='mw-parser-output']/table[@class='wikitable plainrowheaders']")
    table_body = result_table.find_element_by_tag_name("tbody")
    tour_rows = table_body.find_elements_by_tag_name("tr")
    tour_rows.pop(0)  # get rid of title row
    time.sleep(1)
    # tour_rows[0] is men's singles
    # tour_rows[1] is men's doubles
    # tour_rows[2] is women's singles
    # tour_rows[3] is women's doubles
    # tour_rows[4] is mixed doubles
    elements = tour_rows[0].find_elements_by_tag_name("td")
    revised_tour_name = str(from_year) + " Summer Olympics"
    player = elements[1].find_element_by_tag_name("a").accessible_name
    country_name = elements[1].find_elements_by_tag_name("a")[1].accessible_name
    country_image = country.get_country_image(country_name)
    # update player_title_count_map
    if player in player_title_count_map:
        player_title_count_map[player] = player_title_count_map[player] + 1
    else:
        player_title_count_map[player] = 1
    if player not in men_single_df["player"].tolist():
        # add new player
        new_player = [country_name, country_image, player]
        for i in range(padding_count[0]):
            new_player.append(0)
        men_single_df.loc[len(men_single_df.index)] = new_player
    # add new tour column
    new_column_values = []
    for player in men_single_df["player"]:
        new_column_values.append(player_title_count_map[player])
    men_single_df[revised_tour_name] = new_column_values
    padding_count[0] = padding_count[0] + 1