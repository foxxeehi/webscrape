import time
import pandas
import country
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


class WikipediaBWFTitleCrawl:
    MS_title = "MS_title"
    MS_title_supplement = "MS_title_supplement"
    padding_count = 0
    player_title_count_map = {}
    driver_path = 'c:\\chromedriver\\chromedriver.exe'
    options = Options()
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(options=options, executable_path=driver_path)

    def __init__(self, from_year=2007, to_year=2022):
        self.from_year = from_year
        self.to_year = to_year
        column_name_list = ["country", "image", "player"]
        column_name_supplement_list = ["tour", "winner"]
        self.df_map = {self.MS_title: pandas.DataFrame(columns=column_name_list),
                       self.MS_title_supplement: pandas.DataFrame(columns=column_name_supplement_list)}
        self.olympic_years = [2008, 2012, 2016, 2020]

    def crawl(self):
        while self.from_year <= 2017:
            # Super Series
            self.driver.get(
                'https://en.wikipedia.org/wiki/' + str(self.from_year) + '_BWF_Super_Series')
            self.__crawl_superseries_goldprix()
            # Grand Prix and Grand Prix Gold Series
            self.driver.get(
                'https://en.wikipedia.org/wiki/' + str(self.from_year) + '_BWF_Grand_Prix_Gold_and_Grand_Prix')
            self.__crawl_superseries_goldprix()

            # Olympic and world championship
            if self.from_year in self.olympic_years:
                self.driver.get(
                    'https://en.wikipedia.org/wiki/' + 'Badminton_at_the_' + str(self.from_year) + '_Summer_Olympics')
                self.__crawl_olympic_and_championship('Summer Olympics')
            else:
                self.driver.get(
                    'https://en.wikipedia.org/wiki/' + str(self.from_year) + '_BWF_World_Championships')
                self.__crawl_olympic_and_championship('BWF_World_Championships')
            self.from_year = self.from_year + 1
        while self.from_year <= self.to_year:
            # World Tour Super
            self.driver.get(
                'https://en.wikipedia.org/wiki/' + str(self.from_year) + '_BWF_World_Tour')
            self.__crawl_world_tour()

            # Olympic and world championship
            if self.from_year in self.olympic_years:
                self.driver.get(
                    'https://en.wikipedia.org/wiki/' + 'Badminton_at_the_' + str(self.from_year) + '_Summer_Olympics')
                self.__crawl_olympic_and_championship('Summer Olympics')
            else:
                if self.from_year == 2022:
                    break
                self.driver.get(
                    'https://en.wikipedia.org/wiki/' + str(self.from_year) + '_BWF_World_Championships')
                self.__crawl_olympic_and_championship('BWF_World_Championships')
            self.from_year = self.from_year + 1
        self.__save_to_csv()
        self.driver.quit()

    def __save_to_csv(self):
        for event, df in self.df_map.items():
            df.to_csv(event + ".csv")

    def __update_supplement_df(self, tour_winner_pair):
        self.df_map[self.MS_title_supplement].loc[
            len(self.df_map[self.MS_title_supplement].index)] = tour_winner_pair

    def __crawl_superseries_goldprix(self):
        schedule_table = self.driver.find_elements(By.XPATH, "//div[@class='mw-parser-output']/table[@class='wikitable']")[0]
        schedule_table_body = schedule_table.find_element_by_tag_name("tbody")
        schedule_rows = schedule_table_body.find_elements_by_tag_name("tr")
        schedule_rows.pop(0)  # get rid of title row
        schedule_rows.pop(0)  # get rid of start and finish
        result_table = self.driver.find_elements(By.XPATH, "//div[@class='mw-parser-output']/table[@class='wikitable']")[1]
        table_body = result_table.find_element_by_tag_name("tbody")
        tour_rows = table_body.find_elements_by_tag_name("tr")
        tour_rows.pop(0)  # get rid of title row
        time.sleep(1)
        index = 0
        for tour in tour_rows:
            schedule_elements = schedule_rows[index].find_elements_by_tag_name("td")
            tour_name = str(self.from_year) + " " + schedule_elements[1].text
            elements = tour.find_elements_by_tag_name("td")
            player = elements[1].text
            country_name = elements[1].find_element_by_tag_name("span").find_element_by_tag_name("a").accessible_name
            country_image = country.get_country_image(country_name)
            self.__update_supplement_df([tour_name, player])
            # update player_title_count_map
            if player in self.player_title_count_map:
                self.player_title_count_map[player] = self.player_title_count_map[player] + 1
            else:
                self.player_title_count_map[player] = 1
            if player not in self.df_map[self.MS_title]["player"].tolist():
                # add new player
                new_player = [country_name, country_image, player]
                for i in range(self.padding_count):
                    new_player.append(0)
                self.df_map[self.MS_title].loc[len(self.df_map[self.MS_title].index)] = new_player
            # add new tour column
            new_column_values = []
            for player in self.df_map[self.MS_title]["player"]:
                new_column_values.append(self.player_title_count_map[player])
            self.df_map[self.MS_title][tour_name] = new_column_values
            self.padding_count = self.padding_count + 1
            index = index + 1

    def __crawl_world_tour(self):
        result_tables = self.driver.find_elements(By.XPATH,
                                                  "//div[@class='mw-parser-output']/table[@class='wikitable']")
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
            tour_name = ""
            player = ""
            country_name = ""
            country_image = ""
            while index < len(tour_rows):
                elements = tour_rows[index].find_elements_by_tag_name("td")
                # The first tournament in the date
                if len(elements) == 4:
                    # check if the tournament is canceled or not by checking player's name
                    if len(elements[2].find_elements_by_tag_name("a")) < 1:
                        index = index + 10
                        continue
                    if self.from_year >= 2020:
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
                    if self.from_year >= 2020:
                        tour_name = elements[0].find_elements_by_tag_name("a")[2].get_attribute("title")
                    else:
                        tour_name = elements[0].find_elements_by_tag_name("a")[1].get_attribute("title")
                    player = elements[1].find_elements_by_tag_name("a")[1].get_attribute("title")
                    country_name = elements[1].find_elements_by_tag_name("a")[0].get_attribute("title")
                    country_image = country.get_country_image(country_name)
                tour_name = tour_name.replace(" (badminton)", "")
                self.__update_supplement_df([tour_name, player])
                # update player_title_count_map
                if player in self.player_title_count_map:
                    self.player_title_count_map[player] = self.player_title_count_map[player] + 1
                else:
                    self.player_title_count_map[player] = 1
                if player not in self.df_map[self.MS_title]["player"].tolist():
                    # add new player
                    new_player = [country_name, country_image, player]
                    for i in range(self.padding_count):
                        new_player.append(0)
                    self.df_map[self.MS_title].loc[len(self.df_map[self.MS_title].index)] = new_player
                # add new tour column
                new_column_values = []
                for player in self.df_map[self.MS_title]["player"]:
                    new_column_values.append(self.player_title_count_map[player])
                self.df_map[self.MS_title][tour_name] = new_column_values
                self.padding_count = self.padding_count + 1
                index = index + 10

    def __crawl_olympic_and_championship(self, tour_name):
        result_table = self.driver.find_element(By.XPATH,
                                                "//div[@class='mw-parser-output']/table[@class='wikitable "
                                                "plainrowheaders']")
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
        revised_tour_name = str(self.from_year) + " " + tour_name
        if self.from_year in self.olympic_years:
            player = elements[1].find_element_by_tag_name("a").accessible_name
            country_name = elements[1].find_elements_by_tag_name("a")[1].accessible_name
            country_image = country.get_country_image(country_name)
        else:
            player = elements[1].find_elements_by_tag_name("a")[1].accessible_name
            country_name = elements[1].find_elements_by_tag_name("a")[0].accessible_name
            country_image = country.get_country_image(country_name)
        self.__update_supplement_df([revised_tour_name, player])
        # update player_title_count_map
        if player in self.player_title_count_map:
            self.player_title_count_map[player] = self.player_title_count_map[player] + 1
        else:
            self.player_title_count_map[player] = 1
        if player not in self.df_map[self.MS_title]["player"].tolist():
            # add new player
            new_player = [country_name, country_image, player]
            for i in range(self.padding_count):
                new_player.append(0)
            self.df_map[self.MS_title].loc[len(self.df_map[self.MS_title].index)] = new_player
        # add new tour column
        new_column_values = []
        for player in self.df_map[self.MS_title]["player"]:
            new_column_values.append(self.player_title_count_map[player])
        self.df_map[self.MS_title][revised_tour_name] = new_column_values
        self.padding_count = self.padding_count + 1
