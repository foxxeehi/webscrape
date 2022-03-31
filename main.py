import os
from datetime import date

import badmintonCrawl
import badmintonCrawlBWF
import extract
import merge
import mergeBadminton
import nbaCrawl
import wikipediaBWFTitleCrawl

# Crawl data from website
# nbaCrawl.crawl(from_season=1946, to_season=1960)

# 3pts
# path = os.getcwd() + "\\csv\\3pts\\"
# merge.merge(path=path, main_file_name="1979-80", topic_column_name="3PM", player_column_name="PLAYER")

# total pts
# path = os.getcwd() + "\\csv\\all\\"
# merge.merge(path=path, main_file_name="1951-52", topic_column_name="PTS", player_column_name="PLAYER")

# Crawl badminton
# badmintonCrawl.crawl(from_date=date(year=1990, month=1, day=1),
#                      to_date=date(year=2021, month=10, day=25),
#                      category="MS")

# Crawl badminton BWF
# badmintonCrawlBWF.crawl(category="MS", category_full_name="MEN'S SINGLES")

# Extract
# source_path = os.getcwd() + "\\csv\\badminton\\XD\\"
# destination_path = os.getcwd() + "\\csv\\badminton\\XD_Extract\\"
# extract.extract_by_each_month(source_path=source_path, destination_path=destination_path)

# Ranking
# path = os.getcwd() + "\\csv\\badminton\\MS\\"
# mergeBadminton.merge(path=path, main_file_name="1990-01-01", category="MS", destination_file_name="MS")

# Crawl wikipedia Badminton Super Series title result
wiki = wikipediaBWFTitleCrawl.WikipediaBWFTitleCrawl()
wiki.crawl()
