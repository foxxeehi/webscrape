import time
import pandas
import country
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


class WikipediaBWFTitleCrawl:
    image = "<img src=\"https://res.cloudinary.com/bwf/t_96_player_profile/v1604894628/assets/players/thumbnail/6926" \
            "\" width=\"450\" height=\"450\" /><h2>Winner: Peter Gade<h2> "
    MS_title = "MS_title"
    MS_title_supplement = "MS_title_supplement"
    MD_title = "MD_title"
    MD_title_supplement = "MD_title_supplement"
    WS_title = "WS_title"
    WS_title_supplement = "WS_title_supplement"
    WD_title = "WD_title"
    WD_title_supplement = "WD_title_supplement"
    XD_title = "XD_title"
    XD_title_supplement = "XD_title_supplement"
    padding_count_map = {MS_title: 0, MD_title: 0, WS_title: 0, WD_title: 0, XD_title: 0}
    player_title_count_map = {}
    driver_path = 'c:\\chromedriver\\chromedriver.exe'
    options = Options()
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(options=options, executable_path=driver_path)

    def __init__(self, from_year=2007, to_year=2022):
        self.from_year = from_year
        self.to_year = to_year
        column_name_list = ["country", "image", "player"]
        column_name_supplement_list = ["tour", "winner", "image"]
        self.df_map = {self.MS_title: pandas.DataFrame(columns=column_name_list),
                       self.MD_title: pandas.DataFrame(columns=column_name_list),
                       self.WS_title: pandas.DataFrame(columns=column_name_list),
                       self.WD_title: pandas.DataFrame(columns=column_name_list),
                       self.XD_title: pandas.DataFrame(columns=column_name_list),
                       self.MS_title_supplement: pandas.DataFrame(columns=column_name_supplement_list),
                       self.MD_title_supplement: pandas.DataFrame(columns=column_name_supplement_list),
                       self.WS_title_supplement: pandas.DataFrame(columns=column_name_supplement_list),
                       self.WD_title_supplement: pandas.DataFrame(columns=column_name_supplement_list),
                       self.XD_title_supplement: pandas.DataFrame(columns=column_name_supplement_list)}
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
                self.__crawl_olympic()
            else:
                self.driver.get(
                    'https://en.wikipedia.org/wiki/' + str(self.from_year) + '_BWF_World_Championships')
                self.__crawl_championship()
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
                self.__crawl_olympic()
            else:
                if self.from_year == 2022:
                    break
                self.driver.get(
                    'https://en.wikipedia.org/wiki/' + str(self.from_year) + '_BWF_World_Championships')
                self.__crawl_championship()
            self.from_year = self.from_year + 1
        self.__save_to_csv()
        self.driver.quit()

    def __save_to_csv(self):
        for event, df in self.df_map.items():
            df.to_csv(event + ".csv")

    def __get_event_name_superseries_goldprix_by_index(self, event_index):
        switcher = {
            0: self.MS_title,
            1: self.WS_title,
            2: self.MD_title,
            3: self.WD_title,
            4: self.XD_title
        }
        return switcher.get(event_index)

    def __get_event_supplement_name_superseries_goldprix_by_index(self, event_index):
        switcher = {
            0: self.MS_title_supplement,
            1: self.WS_title_supplement,
            2: self.MD_title_supplement,
            3: self.WD_title_supplement,
            4: self.XD_title_supplement
        }
        return switcher.get(event_index)

    def __get_event_name_olympic_by_index(self, event_index):
        switcher = {
            0: self.MS_title,
            1: self.MD_title,
            2: self.WS_title,
            3: self.WD_title,
            4: self.XD_title
        }
        return switcher.get(event_index)

    def __get_event_supplement_name_olympic_by_index(self, event_index):
        switcher = {
            0: self.MS_title_supplement,
            1: self.MD_title_supplement,
            2: self.WS_title_supplement,
            3: self.WD_title_supplement,
            4: self.XD_title_supplement
        }
        return switcher.get(event_index)

    def __get_event_name_by_index_champion_and_world_tour(self, event_index):
        switcher = {
            0: self.MS_title,
            2: self.WS_title,
            4: self.MD_title,
            6: self.WD_title,
            8: self.XD_title
        }
        return switcher.get(event_index)

    def __get_event_supplement_name_by_index_champion_and_world_tour(self, event_index):
        switcher = {
            0: self.MS_title_supplement,
            2: self.WS_title_supplement,
            4: self.MD_title_supplement,
            6: self.WD_title_supplement,
            8: self.XD_title_supplement
        }
        return switcher.get(event_index)

    def __get_event_rows(self):
        result_table = self.driver.find_element(By.XPATH,
                                                "//div[@class='mw-parser-output']/table[@class='wikitable "
                                                "plainrowheaders']")
        table_body = result_table.find_element_by_tag_name("tbody")
        event_rows = table_body.find_elements_by_tag_name("tr")
        event_rows.pop(0)  # get rid of title row
        return event_rows

    def __normalize_name(self, name):
        redundant_names = [" (page does not exist)", " (badminton)"]
        for redundant_name in redundant_names:
            name = name.replace(redundant_name, "")
        return name

    def __is_player_in_collection(self, player, collection, event_name):
        if player in collection:
            return [True, player]
        else:
            if event_name == self.MS_title or event_name == self.WS_title:
                return [False, player]
            else:
                player_swap_list = player.split("/")
                player_swap = player_swap_list[1] + "/" + player_swap_list[0]
                print("player_swap:" + player_swap)
                if player_swap in collection:
                    return [True, player_swap]
        return [False, player]

    def __crawl_superseries_goldprix(self):
        schedule_table = self.driver.find_elements(
            By.XPATH,
            "//div[@class='mw-parser-output']/table[@class='wikitable']")[0]
        schedule_table_body = schedule_table.find_element_by_tag_name("tbody")
        schedule_rows = schedule_table_body.find_elements_by_tag_name("tr")
        schedule_rows.pop(0)  # get rid of title row
        schedule_rows.pop(0)  # get rid of start and finish
        result_table = self.driver.find_elements(
            By.XPATH,
            "//div[@class='mw-parser-output']/table[@class='wikitable']")[1]
        table_body = result_table.find_element_by_tag_name("tbody")
        tour_rows = table_body.find_elements_by_tag_name("tr")
        tour_rows.pop(0)  # get rid of title row
        time.sleep(1)
        schedule_table_index = 0
        for tour in tour_rows:
            schedule_elements = schedule_rows[schedule_table_index].find_elements_by_tag_name("td")
            tour_name = str(self.from_year) + " " + schedule_elements[1].text
            event_columns = tour.find_elements_by_tag_name("td")
            event_columns.pop(0)  # get rid of tour column
            event_index = 0
            while event_index < len(event_columns):
                event_name = self.__get_event_name_superseries_goldprix_by_index(event_index)
                event_supplement_name = self.__get_event_supplement_name_superseries_goldprix_by_index(event_index)
                event = event_columns[event_index]
                self.__update_superseries_goldprix(tour_name, event, event_name, event_supplement_name)
                event_index = event_index + 1
            schedule_table_index = schedule_table_index + 1

    def __crawl_world_tour(self):
        result_tables = self.driver.find_elements(
            By.XPATH,
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
            tour_index = 0
            tour_name = ""
            player = ""
            country_name = ""
            country_image = ""
            while tour_index < len(tour_rows):
                event_index = 0
                while event_index < 9:
                    event_name = self.__get_event_name_by_index_champion_and_world_tour(event_index)
                    event_supplement_name = self.__get_event_supplement_name_by_index_champion_and_world_tour(
                        event_index)
                    elements = tour_rows[tour_index + event_index].find_elements_by_tag_name("td")
                    if event_name == self.MS_title:
                        # The first tournament in the date
                        if len(elements) == 4:
                            # check if the tournament is canceled or not by checking player's name
                            if len(elements[2].find_elements_by_tag_name("a")) < 1:
                                # index = index + 10
                                # continue
                                break
                            if self.from_year >= 2020:
                                tour_name = elements[1].find_elements_by_tag_name("a")[2].get_attribute("title")
                            else:
                                tour_name = elements[1].find_elements_by_tag_name("a")[1].get_attribute("title")
                            player = elements[2].find_elements_by_tag_name("a")[1].get_attribute("title")
                            country_name = elements[2].find_elements_by_tag_name("a")[0].get_attribute("title")
                            country_image = country.get_country_image(country_name)
                        # The second - last tournament in the date
                        if len(elements) == 3:
                            # check if the tournament is canceled or not by checking player's name
                            if len(elements[1].find_elements_by_tag_name("a")) < 1:
                                # index = index + 10
                                # continue
                                break
                            if self.from_year >= 2020:
                                tour_name = elements[0].find_elements_by_tag_name("a")[2].get_attribute("title")
                            else:
                                tour_name = elements[0].find_elements_by_tag_name("a")[1].get_attribute("title")
                            player = elements[1].find_elements_by_tag_name("a")[1].get_attribute("title")
                            country_name = elements[1].find_elements_by_tag_name("a")[0].get_attribute("title")
                            country_image = country.get_country_image(country_name)
                    if event_name == self.WS_title:
                        # check if the tournament is canceled or not by checking player's name
                        if len(elements[0].find_elements_by_tag_name("a")) < 1:
                            break
                        player = elements[0].find_elements_by_tag_name("a")[1].get_attribute("title")
                        country_name = elements[0].find_elements_by_tag_name("a")[0].get_attribute("title")
                        country_image = country.get_country_image(country_name)
                    if event_name == self.WD_title or event_name == self.MD_title or event_name == self.XD_title:
                        # check if the tournament is canceled or not by checking player's name
                        if len(elements[0].find_elements_by_tag_name("a")) < 1:
                            break
                        player1 = elements[0].find_elements_by_tag_name("a")[1].get_attribute("title")
                        player2 = elements[0].find_elements_by_tag_name("a")[3].get_attribute("title")
                        player = player1 + "/" + player2
                        country_name = elements[0].find_elements_by_tag_name("a")[0].get_attribute("title")
                        country_image = country.get_country_image(country_name)
                    player = self.__normalize_name(player)
                    tour_name = self.__normalize_name(tour_name)

                    self.__update_data_frame(tour_name, player, event_name, event_supplement_name, country_name,
                                             country_image)
                    event_index = event_index + 2
                tour_index = tour_index + 10

    def __crawl_olympic(self):
        event_rows = self.__get_event_rows()
        time.sleep(1)
        tour_name = str(self.from_year) + " " + 'Summer Olympics'
        event_index = 0
        while event_index < len(event_rows):
            event_name = self.__get_event_name_olympic_by_index(event_index)
            event_supple_name = self.__get_event_supplement_name_olympic_by_index(event_index)
            gold_medal = event_rows[event_index].find_elements_by_tag_name("td")[1]
            self.__update_olympic(tour_name, gold_medal, event_name, event_supple_name)
            event_index = event_index + 1

    def __crawl_championship(self):
        event_rows = self.__get_event_rows()
        time.sleep(1)
        tour_name = str(self.from_year) + " " + "BWF_World_Championships"
        event_index = 0
        while event_index < len(event_rows):
            event_name = self.__get_event_name_by_index_champion_and_world_tour(event_index)
            event_supple_name = self.__get_event_supplement_name_by_index_champion_and_world_tour(event_index)
            gold_medal = event_rows[event_index].find_elements_by_tag_name("td")[1]
            self.__update_championship(tour_name, gold_medal, event_name, event_supple_name)
            event_index = event_index + 2

    def __update_supplement_df(self, tour_winner_image_triple, event_supplement_name):
        self.df_map[event_supplement_name].loc[
            len(self.df_map[event_supplement_name].index)] = tour_winner_image_triple

    def __update_superseries_goldprix(self, tour_name, event, event_name, event_supplement_name):
        if event_name == self.MS_title or event_name ==self.WS_title:
            player = event.text
        else:
            player = event.text
            if "\n" in player:
                player = player.split("\n")
                player = player[0] + "/" + player[1]
            else:
                player = player.split("/")
                player = player[0].removesuffix(" ") + "/" + player[1].removeprefix(" ")
                print("player:" + player)
            # print("event:" + event_name)
            # print("tour:" + tour_name)
            # player1 = event.find_elements_by_tag_name("a")[1].get_attribute("title")
            # player2 = event.find_elements_by_tag_name("a")[3].get_attribute("title")
            # player = player1 + "/" + player2
        player = self.__normalize_name(player)
        country_name = event.find_element_by_tag_name("span").find_element_by_tag_name("a").accessible_name
        country_image = country.get_country_image(country_name)
        self.__update_data_frame(tour_name, player, event_name, event_supplement_name, country_name, country_image)

    def __update_championship(self, tour_name, gold_medal, event_name, event_supple_name):
        elements = gold_medal.find_elements_by_tag_name("a")
        if event_name == self.MS_title or event_name == self.WS_title:
            player = elements[1].accessible_name
            country_name = elements[0].accessible_name
            country_image = country.get_country_image(country_name)
            self.__update_data_frame(tour_name, player, event_name, event_supple_name, country_name, country_image)
        else:
            player1 = elements[1].accessible_name
            player2 = elements[3].accessible_name
            player = player1 + "/" + player2
            country_name = elements[0].accessible_name
            country_image = country.get_country_image(country_name)
            self.__update_data_frame(tour_name, player, event_name, event_supple_name, country_name, country_image)

    def __update_olympic(self, tour_name, gold_medal, event_name, event_supple_name):
        elements = gold_medal.find_elements_by_tag_name("a")
        if event_name == self.MS_title or event_name == self.WS_title:
            player = elements[0].accessible_name
            country_name = elements[1].accessible_name
            country_image = country.get_country_image(country_name)
        else:
            player1 = elements[0].accessible_name
            player2 = elements[1].accessible_name
            player = player1 + "/" + player2
            country_name = elements[2].accessible_name
            country_image = country.get_country_image(country_name)
        self.__update_data_frame(tour_name, player, event_name, event_supple_name, country_name, country_image)

    def __update_data_frame(self, tour_name, player, event_name, event_supplement_name, country_name, country_image):
        self.__update_supplement_df([tour_name, player, self.image], event_supplement_name)
        # update player_title_count_map
        is_player_in_collection = self.__is_player_in_collection(player, self.player_title_count_map, event_name)
        if is_player_in_collection[0]:
            player = is_player_in_collection[1]
            self.player_title_count_map[player] = self.player_title_count_map[player] + 1
        else:
            self.player_title_count_map[player] = 1
            # add new player
            new_player = [country_name, country_image, player]
            for i in range(self.padding_count_map[event_name]):
                new_player.append(0)
            self.df_map[event_name].loc[len(self.df_map[event_name].index)] = new_player
        # add new tour column
        new_column_values = []
        for player in self.df_map[event_name]["player"]:
            new_column_values.append(self.player_title_count_map[player])
        self.df_map[event_name][tour_name] = new_column_values
        self.padding_count_map[event_name] = self.padding_count_map[event_name] + 1
