from wayback2csv.wayback2csv import Wayback2Csv

from sys import argv
import json

w2c = Wayback2Csv("wayback2csv YOUR EMAIL ADDRESS HERE", "http://www.costco.com/.product.100018645.html", from_date="2015")
w2c.download()
w2c.parse_html(".your-price .currency", lambda x: x.text.replace("$", '').replace(",", '') )
w2c.to_csv(f"costco_couch_price_over_time.csv", ["Costco Couch"])