import sys
import requests

from page import Page 

def sendRequest(url):
    r = requests.get(url)
    content = r.content

    page = Page(content)

    print("<links>")
    links = page.get_links()
    print(f"There are {len(links)} links on the page.")
    for link in links:
        print(f"{link.get('href')} -> {link.text}")

    print("\n<divs>")
    divs = page.get_divs()
    print(f"There are {len(divs)} divs on the page.")

    print("\n<paragraphs>")
    paragraphs = page.get_paragraphs()
    print(f"There are {len(paragraphs)} paragraphs on the page.")

    print("\n<words>")
    words = page.get_words()
    print(f"There are approximately {len(words)} words on the page.")
    print(words)

if __name__=="__main__":
    # url = "https://nostarch.com"
    url = sys.argv[1]
    sendRequest(url)
