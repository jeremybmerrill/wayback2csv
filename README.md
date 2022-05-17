# wayback2csv

a module to get a set of URLs from the Internet Archive and parse out a specific datapoint to a CSV with the date.

like for getting follower counts historically from the internet archive.

e.g. 

```
from wayback2csv.wayback2csv import Wayback2Csv
from sys import argv

username = argv[1]

w2c = Wayback2Csv("waybackpack wayback2csv@example.com", f"twitter.com/{username}", from_date="2022")
w2c.download()
w2c.parse_html(".ProfileNav-item--followers .ProfileNav-value", lambda x: x.get("data-count") if x.get("data-count") else "None")
w2c.to_csv(f"data/{username}_twitter_followers_over_time.csv", [username])
```