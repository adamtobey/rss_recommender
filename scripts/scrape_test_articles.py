from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import json

hnpage = urlopen("https://hckrnews.com/").read()
page = bs(hnpage)
links = page.find_all("a", "link")
urls = [link['href'] for link in links]
out = {
    'urls': urls
}

with open('test_urls.json', 'w') as outfile:
    outfile.write(json.dumps(out))
