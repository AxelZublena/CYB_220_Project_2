import sys
import requests
import whois
from tabulate import tabulate

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
    links = page.get_formated_links()
    print(f"There are {len(links)} links on the page.")

    print("\n<divs>")
    divs = page.get_divs()
    print(f"There are {len(divs)} divs on the page.")

    print("\n<paragraphs>")
    paragraphs = page.get_paragraphs()
    print(f"There are {len(paragraphs)} paragraphs on the page.")

    print("\n<words>")
    words = page.get_words()
    print(f"There are approximately {len(words)} words on the page.")

    print("\n<files>")
    files = page.get_linked_files()
    print(f"There are {len(files)} files linked on the page.")

    print("\n<images>")
    images = page.get_images()
    print(f"There are {len(images)} images linked on the page.")

    print(tabulate(generate_table(links, divs, paragraphs, words, files, images), 
                   headers='firstrow', 
                   tablefmt='fancy_grid'))

def generate_table(links, divs, paragraphs, words, files, images):
    table = [['Stat', 'Number', 'List'], 
             ["<link>", len(links), tabulate(itemize_list(links), tablefmt="plain")], 
             ["<div>", len(divs), ""], 
             ["<p>", len(paragraphs), ""], 
             ["Words", len(words), ""], 
             ["Linked Files", len(files), tabulate(itemize_list(files), tablefmt="plain")], 
             ["Images", len(images), tabulate(itemize_list(images), tablefmt="plain")]]
    return table

def itemize_list(list):
    if len(list )< 1:
        return list

    final_list = []
    for item in list:
        final_list.append([item])

    return final_list

if __name__=="__main__":
    # url = "https://nostarch.com"
    url = sys.argv[1]
    page = getPage(url)
    if page != 0:
        process(page)

    # print("\nPerforming WHOIS analysis...")
    # w = whois.whois(url)
    # print(w.name_servers)
    # print(w.expiration_date)

