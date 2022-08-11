from wayback2csv.wayback2csv import Wayback2Csv

from sys import argv
import json

w2c = Wayback2Csv("wayback2csv YOUR EMAIL ADDRESS HERE", "https://www.piedmont.org/emergency-room-wait-times/emergency-room-wait-times", from_date="2015")
w2c.download()
w2c.parse_html("#ctl00_cphContent_ctl00_lblPiedmontAtlanta", lambda x: x.text )
w2c.to_csv(f"piedmont_atlanta_er_wait_times_over_time.csv", ["Atlanta"])