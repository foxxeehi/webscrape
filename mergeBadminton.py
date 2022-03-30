import os

import pandas
import pandas as pd

from country import get_country_map, get_country_image, correct_country

def normalize_string(target):
    return target.replace(" ", "").lower()

def merge(path, main_file_name, category, destination_file_name):
    country_column_name = "Country"
    country_image_column_name = "Image"
    player_column_name = "Players"
    topic_column_name = "Points"
    main_df = pd.read_csv(path + main_file_name + ".csv")
    player1s = main_df[player_column_name].tolist()
    # country1s = main_df[country_column_name].apply(
    #     lambda row: correct_country(country=row)
    # )
    country1s = main_df[country_column_name]
    country_image1s = country1s.apply(
        lambda row: get_country_image(country_name=row)
    ).tolist()
    country1s = country1s.tolist()
    # remove chinese in player name for main file
    # for player1_index in range(len(player1s)):
    #     player1s[player1_index] = player1s[player1_index].replace(" Chinese", "")
    main_topic_column = main_df[topic_column_name].tolist()
    column_names = [country_column_name, country_image_column_name, player_column_name,
                    main_file_name]
    revised_main_df = pandas.DataFrame(list(zip(country1s, country_image1s, player1s, main_topic_column)),
                                       columns=column_names)
    all_files = os.listdir(path)
    all_files.remove(main_file_name + ".csv")
    file_index = 1
    for file in all_files:
        # player1s = revised_main_df[player_column_name].tolist()
        player1s = revised_main_df[player_column_name].apply(
            lambda row: normalize_string(row)
        ).tolist()
        new_added_year_topic_column = [0] * len(player1s)

        next_df = pd.read_csv(path + file)
        player2s = next_df[player_column_name].tolist()
        next_topic_column = next_df[topic_column_name].tolist()
        new_players = []

        player_2_index = 0
        for player2 in player2s:
            if not isinstance(player2, str):
                continue
            # player2 = player2.replace(" Chinese", "")
            normalized_player2 = normalize_string(player2)
            # if player2 in player1s:
            if normalized_player2 in player1s:
                player2_in_player1s_index = player1s.index(normalized_player2)
                new_added_year_topic_column[player2_in_player1s_index] = next_topic_column[player_2_index]
            else:
                country2s = next_df[country_column_name].apply(
                    lambda row: correct_country(country=row)
                )
                print(file)
                country_image2s = country2s.apply(
                    lambda row: get_country_image(country_name=row)
                ).tolist()
                country2s = country2s.tolist()
                new_players.append([country2s[player_2_index]])
                new_players[len(new_players) - 1].append(country_image2s[player_2_index])
                new_players[len(new_players) - 1].append(player2)
                for i in range(file_index):
                    new_players[len(new_players) - 1].append(0)
                new_players[len(new_players) - 1].append(next_topic_column[player_2_index])
                print(new_players)
            player_2_index = player_2_index + 1

        # for player1_index in range(len(player1s)):
        #     if new_added_year_topic_column[player1_index] == 0:
        #         new_added_year_topic_column[player1_index] = main_topic_column[player1_index]
        # file_name = file.split("-")[0]
        # file_name will look like 1990-01
        file_name = file.removesuffix(".csv")
        revised_main_df[file_name] = new_added_year_topic_column
        for new_player in new_players:
            revised_main_df.loc[len(revised_main_df.index)] = new_player
        file_index = file_index + 1
    revised_main_df.to_csv(destination_file_name + ".csv")
