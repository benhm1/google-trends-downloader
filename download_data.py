import os
import csv
import time
import string
import datetime
import argparse
import urllib.parse
from selenium import webdriver

from normalize import normalize_directory

def parse_args():
    parser = argparse.ArgumentParser(description='Download daily trends from Google Trends')
    parser.add_argument('--start_year', type=int)
    parser.add_argument('--start_month', type=int)
    parser.add_argument('--start_day', type=int)

    parser.add_argument('--end_year',  nargs='?', type=int, default=datetime.date.today().year )
    parser.add_argument('--end_month', nargs='?', type=int, default=datetime.date.today().month)
    parser.add_argument('--end_day',   nargs='?', type=int, default=datetime.date.today().day  )

    parser.add_argument('--query', type=str)

    args = parser.parse_args()
    return args

def get_selenium(output_dir):
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.panel.shown", False)
    profile.set_preference("browser.helperApps.neverAsk.openFile","text/csv,application/vnd.ms-excel")
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv,application/vnd.ms-excel")
    profile.set_preference("browser.download.folderList", 2);
    profile.set_preference("browser.download.dir", os.path.join( os.getcwd(), output_dir ) )
    driver = webdriver.Firefox(firefox_profile=profile)
    return driver

def do_it():
    args = parse_args()

    dirname = ''.join( [ x for x in args.query if x in string.ascii_letters + string.digits + ' ' ] )
    dirname = dirname.replace(' ', '_')
    dirname = f'data_{dirname}'

    if os.path.exists(dirname):
        print(f"Directory {dirname} already exists! Rename it and re-run.")
        return 

    os.mkdir(dirname)

    driver = get_selenium(dirname)

    query_str = urllib.parse.quote(args.query)

    start_date = datetime.date(args.start_year, args.start_month, args.start_day)
    end_date = datetime.date(args.end_year, args.end_month, args.end_day)

    print(f'Getting data between {start_date} and {end_date}.')
    print(f'Query String: "{args.query}"')
    print(f'Writing intermediate CSV files to {dirname}')

    cur_start = start_date
    while cur_start < end_date:
        cur_end = cur_start  + datetime.timedelta(days = 75)
        if cur_end > end_date:
            cur_end = end_date

        url = (f'https://trends.google.com/trends/explore?'
               f'date={cur_start.year}-{cur_start.month}-{cur_start.day}%20'
               f'{cur_end.year}-{cur_end.month}-{cur_end.day}'
               f'&geo=US&q={query_str}')
                

        print(f'\tGetting {cur_start} --> {cur_end}')
        print(f'\t\t{url}')

        while 1:
            attempts = 0
            if attempts > 0:
                print(f'Attempt {attempts + 1} / 4')
            try:
                driver.get(url)
                time.sleep(2)
                driver.find_element_by_class_name('export').click()
                time.sleep(1)
                break
            except:
                attempts += 1
                if attempts > 3:
                    break

                print(f"Something went wrong! Trying again.")
                time.sleep(5)
                
        if cur_end >= end_date:
            break

        cur_start += datetime.timedelta(days = 45)

    normalized = normalize_directory(dirname)
    output = os.path.join(dirname, 'normalized.csv')
    with open(output, 'w', newline='') as csvfile:
        outwriter = csv.writer(csvfile, delimiter=' ',
                               quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for val in normalized:
            outwriter.writerow(val)

    print(f"Wrote normalized data to {output}")

    driver.quit()

if __name__ == '__main__':
    do_it()
