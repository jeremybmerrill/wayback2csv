from operator import itemgetter
import os
from glob import glob
from datetime import datetime
import csv
import json
import logging

import requests
import waybackpack
from bs4 import BeautifulSoup
from tqdm.auto import tqdm

logger = logging.getLogger(__name__)


DEFAULT_PARENT_DIR = ".wayback2csv/"
DEFAULT_COLLAPSE = "timestamp:8"  # daily


class Wayback2Csv:

    def __init__(self, user_agent, url, from_date=None, to_date=None, collapse=DEFAULT_COLLAPSE, dir=DEFAULT_PARENT_DIR):
        session = waybackpack.Session(user_agent=user_agent)
        self.dir = dir

        snapshots = waybackpack.search(url,
                                       session=session,
                                       from_date=from_date,
                                       to_date=to_date,
                                       uniques_only=True,
                                       collapse=collapse
                                       )

        timestamps = [snap["timestamp"] for snap in snapshots]

        self.pack = waybackpack.Pack(
            url,
            timestamps=timestamps,
            session=session
        )
        self.values = []

    def download(self, ignore_errors=True):
        self.pack.download_to(
            self.dir,
            no_clobber=True,
            use_tqdm=True,
            ignore_errors=ignore_errors
        )
        # self.download_live_site()

    def download_live_site(self, ignore_errors=True):
        path_head, path_tail = os.path.split(self.pack.parsed_url.path)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filedir = os.path.join(
            self.dir,
            timestamp,
            self.pack.parsed_url.netloc,
            path_head.lstrip("/")
        )
        filepath = os.path.join(filedir, path_tail)
        logger.info(
            "Fetching {0} @ {1}".format(
                self.pack.url,
                timestamp)
        )

        try:
            content = requests.get('https://' + self.pack.url).content
        except Exception as e:
            if ignore_errors == True:
                ex_name = ".".join([e.__module__, e.__class__.__name__])
                logger.warn("ERROR -- {0} @ {1} -- {2}: {3}".format(
                    self.pack.url,
                    timestamp,
                    ex_name,
                    e
                ))
                return
            else:
                raise
        try:
            os.makedirs(filedir)
        except OSError:
            pass
        with open(filepath, "wb") as f:
            logger.info("Writing to {0}\n".format(filepath))
            f.write(content)

    def parse_html(self, css_selector, number_lambda=None):
        path_head, path_tail = os.path.split(self.pack.parsed_url.path)
        for fn in tqdm(glob(os.path.join(
            self.dir,
            "*",
            self.pack.parsed_url.netloc,
            path_head.lstrip("/"),
            path_tail
        ))):
            if os.path.isdir(fn):
                continue
            with open(fn, 'r') as f:
                try:
                    html_doc = f.read()
                except UnicodeDecodeError:
                    continue
                soup = BeautifulSoup(html_doc, 'html.parser')
                followers_values = soup.select(css_selector)
                if not followers_values:
                    logger.warn(
                        "couldn't find any elements matching %s in %s", css_selector, fn)
                    continue
                followers = number_lambda(
                    followers_values[0]) if number_lambda else followers_values[0]
                try:
                    count = int(followers)
                except ValueError as e:
                    logger.warn(
                        "couldn't parse an int from %s in %s", followers, fn)
                    continue
                raw_date = fn.split("/")[1]
                scrape_date = datetime.strptime(raw_date[:8], "%Y%m%d")
                self.values.append([fn, scrape_date, count])

    def parse_json(self, path, number_lambda=None):
        path_head, path_tail = os.path.split(self.pack.parsed_url.path)
        for fn in tqdm(glob(os.path.join(
            self.dir,
            "*",
            self.pack.parsed_url.netloc,
            path_head.lstrip("/"),
            path_tail
        ))):
            if os.path.isdir(fn):
                continue
            with open(fn, 'r') as f:
                try:
                    json_doc = f.read()
                except UnicodeDecodeError:
                    continue
                try:
                    data = json.loads(json_doc)
                except json.decoder.JSONDecodeError:
                    logger.error("JSON decode error {}".format(fn))
                    continue
                count = drill_down_nested_dict(data, path)
                count = number_lambda(count) if number_lambda else count
                raw_date = fn.split("/")[1]
                scrape_date = datetime.strptime(raw_date[:8], "%Y%m%d")
                self.values.append([fn, scrape_date, count])

    def to_csv(self, outfn, extra_row_values=[]):
        with open(outfn, 'w') as outf:
            writer = csv.writer(outf)
            writer.writerow(["path", "date", "value"] +
                            [f"extra{n+1}" for n, _ in enumerate(extra_row_values)])
            for row in sorted(self.values, key=itemgetter(1)):
                writer.writerow(row + extra_row_values)


def drill_down_nested_dict(nested_dict, keys):
    for key in keys:
        nested_dict = nested_dict[key]
    return nested_dict
