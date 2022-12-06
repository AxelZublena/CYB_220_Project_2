import sys
import requests
import whois
from page import Page 

def getPage(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            content = r.content
            return Page(content)
        else:
            raise Exception("HTTP request did not return 200")
    except Exception as e:
        print("Page could not be reached.")
        return 0


def process(page):
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
    # print(words)

    print("\n<files>")
    files = page.get_linked_files()
    print(f"There are {len(files)} files linked on the page.")
    print(files)

    print("\n<images>")
    images = page.get_images()
    print(f"There are {len(images)} images linked on the page.")
    print(images)

if __name__=="__main__":
    # url = "https://nostarch.com"
    url = sys.argv[1]
    page = getPage(url)
    if page != 0:
        process(page)

    print("\nPerforming WHOIS analysis...")
    w = whois.whois(url)
    print(w.name_servers)
    print(w.expiration_date)

