#!/usr/bin/python3
# coding:utf8

import argparse
import requests
import urllib3  
from concurrent.futures import ThreadPoolExecutor, as_completed

urllib3.disable_warnings()

def fetch_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.112 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, verify=False, allow_redirects=False)
        if response.status_code == 301:
             return response.headers.get("Location")
        else:
             return None
    except requests.exceptions.ConnectionError as e:
            print(f"Error: {e}")

def main(url_target):
    DRUPAL_URL = f"{url_target}/node/"
    ids = range(1, 20000)
    urls = [f"{DRUPAL_URL}{id}" for id in ids]

    with ThreadPoolExecutor(max_workers=50) as executor:
        future_to_url = {executor.submit(fetch_url, url): url for url in urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                location = future.result()
                if location is not None:
                     print(f"{location}")
            except Exception as exc:
                 print(f"Error: {exc}")

def parseArgs():
    parser = argparse.ArgumentParser(description="Drupal - Get All URLs")
    parser.add_argument("-u", "--url", required=True, help="Drupal URL")
    return parser.parse_args()

if __name__ == '__main__':
    options = parseArgs()
    main(options.url)
