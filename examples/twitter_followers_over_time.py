from waybackrucksack.waybackrucksack import WaybackRucksack

from sys import argv

username = argv[1]

wbrs = WaybackRucksack("waybackrucksack YOUR EMAIL ADDRESS HERE", f"twitter.com/{username}", from_date="2022")
wbrs.download()
wbrs.parse_html(".ProfileNav-item--followers .ProfileNav-value", lambda x: x.get("data-count") if x.get("data-count") else "None")
wbrs.to_csv(f"{username}_twitter_followers_over_time.csv", [username])