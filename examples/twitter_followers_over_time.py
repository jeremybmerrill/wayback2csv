from wayback2csv.wayback2csv import Wayback2Csv

from sys import argv
import json

username = argv[1]

w2c = Wayback2Csv("wayback2csv YOUR EMAIL ADDRESS HERE", f"twitter.com/{username}", from_date="2022")
w2c.download()
w2c.parse_html(".ProfileNav-item--followers .ProfileNav-value", lambda x: x.get("data-count") if x.get("data-count") else "None")
w2c.to_csv(f"{username}_twitter_followers_over_time.csv", [username])