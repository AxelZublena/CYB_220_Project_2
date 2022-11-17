import sys
from io import BytesIO
from lxml import etree

import requests

def sendRequest(url):
    r = requests.get(url)
    content = r.content

    parser = etree.HTMLParser()
    content = etree.parse(BytesIO(content), parser=parser)
    for link in content.findall('//a'):
        print(f"{link.get('href')} -> {link.text}")

if __name__=="__main__":
    # url = "https://nostarch.com"
    url = sys.argv[1]
    sendRequest(url)
