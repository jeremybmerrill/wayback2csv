from wayback2csv.wayback2csv import Wayback2Csv

from sys import argv
import json

username = argv[1]

w2c = Wayback2Csv("wayback2csv YOUR EMAIL ADDRESS HERE", f"twitter.com/{username}", from_date="2022")
w2c.download()

# you can use multiple parsing strategies if files differ in format!

# some older (2022) Twitter files include the follower count in this div.
w2c.parse_html(".ProfileNav-item--followers .ProfileNav-value", lambda x: x.get("data-count") if x.get("data-count") else "None")


# some newer (2023) Twitter files instead include the follower count in JSON, which is extracted here.
def parse_json(json_el):
    try:
        return json.loads(json_el.text)["author"]["interactionStatistic"][0]["userInteractionCount"]
    except:
        print(json.loads(json_el.text))
        return 'None'
w2c.parse_html_xpath("//script[contains(text(), 'userInteractionCount')]", parse_json)
w2c.to_csv(f"{username}_twitter_followers_over_time.csv", [username])
