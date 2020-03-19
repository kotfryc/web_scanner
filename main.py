import requests
from bs4 import BeautifulSoup
# from requests_html import HTMLSession
import concurrent.futures
import time
import urllib3
import requests
import random
headers = {
    "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}
urllib3.disable_warnings()


def valid_link_rules(link_to_vlaidate):
    if 'http' in link_to_vlaidate and '#' not in link_to_vlaidate and len(link_to_vlaidate) > 8:
        return True
    else:
        return False


def finde_links(page_to_inspepkt):
    print(page_to_inspepkt)
    intern_links = []
    out_links = []
    link_list_temp = []
    page = requests.get(page_to_inspepkt, headers=headers, timeout=30, verify=False)
    soup = BeautifulSoup(page.content, 'html.parser', from_encoding="iso-8859-1")
    links = soup.find_all('a')
    url_front = page_to_inspepkt.split('//')[0] + '//'
    url_base = url_front + page_to_inspepkt.split('/')[2]  # str glowna
    for link in soup.find_all('a'):
        # print(link)
        link_str = str(link.get('href'))
        link_str = link_str.replace(' ', '')
        if '#' not in link_str and 'None' not in link_str and len(link_str) > 9:
            # print(link_str)
            if 'http' in link_str:
                # print(link_str)
                link_list_temp.append(link_str)
            else:
                if link_str[0] == '/':
                    link_list_temp.append(url_base + link_str)
                else:
                    link_list_temp.append(url_base + '/' + link_str)
                # print(link_str)

    # print(link_list_temp)
    for clear_link in link_list_temp:
        # if url_base in clear_link:
        if (clear_link[:len(url_base)]) == url_base:
            intern_links.append(clear_link)
        else:
            out_links.append(clear_link)
    return [intern_links, page_to_inspepkt, out_links]


def url_filter(url):
    if '/tag/' not in url and 'ajaxstarrater' not in url and '#' not in url \
            and '.jpg' not in url and '.png' not in url and '/tagi/' not in url \
            and 'tag,' not in url and 'action=premium' not in url \
            and 'javascript' not in url and 'wp-login.php' not in url \
            and 'feed/' not in url and 'twitter' not in url \
            and 'facebook' not in url and '.jpeg' not in url and '.gif' not in url:
        return True
    else:
        return False


def requests_check(domain):
    try:
        r = requests.get(domain, headers=headers, timeout=15, verify=False)
        if r.status_code < 600:
            return True
        r.raise_for_status()
    except Exception:
        return False
    else:
        return True


def cravler(base_url, treads=80):
    url_list_to_check = [base_url]
    url_list_to_check_temporary = []
    url_checked_list = []
    out_going_urls = []
    while len(url_list_to_check) != 0:
        if len(url_list_to_check) < treads:
            url_list_to_check_temporary = url_list_to_check
            url_list_to_check = []
        else:
            url_list_to_check_temporary = url_list_to_check[0:treads]
            url_list_to_check = url_list_to_check[treads:]
        # print(url_list_to_check_temporary)
        # print(url_list_to_check_temporary)

        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = executor.map(finde_links, url_list_to_check_temporary)
            for result in results:
                for intern_link in result[0]:
                    if intern_link not in url_checked_list and url_filter(
                            intern_link) and intern_link not in url_list_to_check_temporary and intern_link not in url_list_to_check:
                        url_list_to_check.append(intern_link)
                        # print(url_list_to_check)
                for out_link in result[2]:
                    if out_link[:4] == 'http' and out_link.find('.') != -1:
                        # print(out_link)
                        out_link = out_link.split('//')[0] + '//' + out_link.split('//')[1].split('/')[0]
                        if out_link not in out_going_urls:
                            out_going_urls.append(out_link)
        url_checked_list.extend(url_list_to_check_temporary)
        print(f'url sprawdzone {len(url_checked_list)}')
        print(f' url do sprawdzenia {len(url_list_to_check)}')
        #time.sleep(random.randint(10,25))


    return [url_checked_list, out_going_urls]


start = time.perf_counter()
#ccc = cravler('http://badbox.pl/', 50)
#ccc = cravler('http://biznes-katalog.com.pl/', 50)
#ccc = cravler('https://www.oferujemyprace.pl/', 50)

#ccc = cravler('http://www.boincatpoland.org', 200)
ccc = cravler('http://www.reklamowy.biz/', 30)
for c in ccc[0]:
    print(c)

print(30 * '*')
for b in ccc[1]:
    if not requests_check(b):
        print(b)
    else:
        continue

print(30 * '*')

finish = time.perf_counter()
print(f'Finished in {round(finish - start, 2)} second(s)')
print(30 * '*')
