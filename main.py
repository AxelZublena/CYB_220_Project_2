import sys
import requests
import whois
import os
from tabulate import tabulate

from page import Page 

def get_page(url):
    """
    Send HTTP GET request to specified URL, 
    create Page object with the response
    """
    try:
        r = requests.get(url)
        if r.status_code == 200:
            content = r.content
            return Page(content, r.elapsed)
        else:
            raise Exception("HTTP request did not return 200")
    except Exception as e:
        print("Page could not be reached.")
        return 0


def analyse_page(page):
    """Gather the statistics and display a table about a page"""
    links = page.get_formated_links()
    divs = page.get_divs()
    paragraphs = page.get_paragraphs()
    words = page.get_words()
    files = page.get_linked_files()
    images = page.get_images()
    elapsed_time = page.get_elapsed_time()

    print(tabulate(generate_stat_table(links, divs, paragraphs, words, files, images, elapsed_time), 
                   headers='firstrow', 
                   tablefmt='fancy_grid'))

def generate_stat_table(links, divs, paragraphs, words, files, images, elapsed_time):
    """Create statistics table to be displayed"""
    table = [['Stat', 'Number', 'List'], 
             ["<a>", len(links), tabulate(format_list(links), tablefmt="plain")], 
             ["<div>", len(divs), ""], 
             ["<p>", len(paragraphs), ""], 
             ["Words", len(words), ""], 
             ["Linked Files", len(files), tabulate(format_list(files), tablefmt="plain")], 
             ["Images", len(images), tabulate(format_list(images), tablefmt="plain")],
             ["Server response time", elapsed_time, ""]]
    return table

def format_list(list):
    """
    Put every item of a list into a list.
    Essentially creating a list of list of length 1.
    If item is too long, return a short version by cutting it in half.
    """
    final_list = []
    for item in list:
        # Get width of the CLI to calculate the max length authorized
        cli_width = os.get_terminal_size().columns
        
        if len(item) > cli_width/3:
            # If text is too long to be displayed: create shorter version
            new_item = item[0:int(cli_width/4)] + " ... " + item[len(item)-int(cli_width/6):]
            final_list.append([new_item])
        else:
            # If text is not too long to be displayed: do nothing
            final_list.append([item])

    return final_list

if __name__=="__main__":
    url = sys.argv[1]

    print(f"\nAcquiring statistics about {url}...\n")
    page = get_page(url)
    if page != 0:
        analyse_page(page)

    print("\nPerforming WHOIS analysis...")
    w = whois.whois(url)
    print(w.name_servers)
    print(w.expiration_date)

    print(os.get_terminal_size().columns)

