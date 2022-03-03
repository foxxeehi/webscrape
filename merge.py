import os

import pandas
import pandas as pd


def merge(path, main_file_name, topic_column_name, player_column_name):
    main_df = pd.read_csv(path + main_file_name + ".csv")
    player1s = main_df[player_column_name].tolist()
    main_topic_column = main_df[topic_column_name].tolist()
    column_names = [player_column_name, main_file_name]
    revised_main_df = pandas.DataFrame(list(zip(player1s, main_topic_column)), columns=column_names)
    all_files = os.listdir(path)
    all_files.remove(main_file_name + ".csv")
    #main_topic_column = revised_main_df[main_file_name].tolist()
    file_index = 1
    for file in all_files:
        player1s = revised_main_df[player_column_name].tolist()
        new_added_year_topic_column = [0] * len(player1s)

        next_df = pd.read_csv(path + file)
        player2s = next_df[player_column_name].tolist()
        next_topic_column = next_df[topic_column_name].tolist()
        new_players = []

        player_2_index = 0
        for player2 in player2s:
            if player2 in player1s:
                player2_in_player1s_index = player1s.index(player2)
                new_added_year_topic_column[player2_in_player1s_index] = main_topic_column[player2_in_player1s_index] + next_topic_column[player_2_index]
            else:
                new_players.append([player2])
                for i in range(file_index):
                    new_players[len(new_players) - 1].append(0)
                new_players[len(new_players) - 1].append(next_topic_column[player_2_index])
                print(new_players)
            player_2_index = player_2_index + 1

        for player1_index in range(len(player1s)):
            if new_added_year_topic_column[player1_index] == 0:
                new_added_year_topic_column[player1_index] = main_topic_column[player1_index]
        revised_main_df[file.removesuffix(".csv")] = new_added_year_topic_column
        for new_player in new_players:
            revised_main_df.loc[len(revised_main_df.index)] = new_player
        main_topic_column = revised_main_df[file.removesuffix(".csv")].tolist()
        file_index = file_index + 1
    revised_main_df.to_csv("total_pts.csv")
