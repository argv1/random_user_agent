#!/usr/bin/env python3
'''
    A small script to fetch and list the most frequently used user agents.
    based on https://developers.whatismybrowser.com/useragents/explore/software_type_specific/web-browser/
'''

import csv
import pandas as pd
from   pathlib import Path
import re
import requests
import time

time_delay = 3
base_url = r'https://developers.whatismybrowser.com/useragents/explore/software_type_specific/web-browser/'
base_path = Path(r'H:\OneDrive\Programme\_current\random user agent')
file_name = base_path / 'output.csv'  
html_list = base_path / 'output.html'  
url_Headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; AFTMM Build/NS6264; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36", "Referer": "http://google.com"}

def main():
    '''
        Check whatismybrowser.com for new user agents
    '''
    user_agent_list = []

    for page in range(1,10):
        content = requests.get(f"{base_url}{page}", headers=url_Headers, timeout=None)
        user_agent_list.extend(re.findall(r'<td class="useragent"><a href=".*">(.*)</a></td>\s*<td  title=".*\>(.*)<\/td>\s*<td>(.*)</td>\s*<td>(.*)</td>', content.text))

        # politely wait
        time.sleep(time_delay)

    # write results to a csv file 
    with open(file_name, 'w', encoding="iso-8859-15") as f:
        writer = csv.writer(f , lineterminator='\n')
        writer.writerow(["User_agent", "Software", "OS", "Layout_engine"])
        for tup in user_agent_list:
            writer.writerow(tup)

    df = pd.read_csv(file_name, encoding="iso-8859-15")

    html_table = df.to_html(escape=False)
    with open(html_list, "w", encoding="utf-8") as f:
        for line in html_table:
            f.write(line)
    
if __name__  == "__main__":
    main()