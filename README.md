# Google Map Scraper
Google Map Scraper using python, selenium and headless chromium. **Only support linux at the moment**.

## Prerequisite
**Miniconda or Anaconda**

**chromium**

## Installation
First time installation need to run `preinstall.sh` to install all python dependencies and checks needed applications on PATH.
```shell
chmod +x preinstall.sh
./preinstall.sh
```
Scraping can be initialized by executing `main.py` using following command and configuration respectively:
```shell
python main.py pizza
```

```
usage: main.py [-h] [--location LOCATION] [--limit LIMIT] [--output OUTPUT]
               keyword

positional arguments:
  keyword              search query in google map

optional arguments:
  -h, --help           show this help message and exit
  --location LOCATION  specific location of keyword
  --limit LIMIT        limit of search result
  --output OUTPUT      output file of scraped data
```
Result is stored as tsv (tab-separated values) format in the same location as `--output` parameter (default location is *output.tsv*).
```shell
$ head output.tsv
title   details location        website
Domino's        Stan Pizza      #02, 166 Woodlands Street 13, 525       https://www.dominos.com.sg/
Domino's Jurong Pizza   6 Jurong West Ave 1, #01-03 Jurong Green CC     https://www.dominos.com.sg/
Domino's Jurong East    Pizza   Blk, 202 Jurong East Street 21, #01-115 https://www.dominos.com.sg/
Domino's Bukit Timah    Pizza   8 Chun Tin Rd   https://www.dominos.com.sg/
```