import os

import pandas as pd


def extract_by_each_month(source_path, destination_path):
    all_files = os.listdir(source_path)
    extract_month = 0
    for file in all_files:
        file_name = file.removeprefix(".csv")
        current_month = file_name.split("-")[1]
        if current_month == extract_month:
            continue
        extract_month = current_month
        df = pd.read_csv(source_path + file)
        df.to_csv(destination_path + file)
