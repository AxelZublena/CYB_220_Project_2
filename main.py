import sys
import requests
import whois
import os

from tabulate import tabulate
from whois.parser import datetime

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

def generate_whois_table(whois_result):
    """Create whois table to be displayed"""

    # Gather meaningful information
    domain_name = whois_result.domain_name[1] if whois_result.domain_name else "Could not retrieve this information"
    registrar = whois_result.registrar or "Could not retrieve this information"
    name_servers = whois_result.name_servers
    creation_date = get_correct_date(whois_result.creation_date) 
    expiration_date = get_correct_date(whois_result.expiration_date)
    updated_date = get_correct_date(whois_result.updated_date)

    # Handle None values for name_servers
    name_servers = "Could not retrieve this information" if name_servers is None else tabulate(format_list(name_servers), tablefmt="plain") 

    # Create table
    table = [['Name', 'Number', 'Value'], 
             ["Domain Name", 1, domain_name],
             ["Registrar", 1, registrar],
             ["Name Servers", 1 if len(name_servers) == 35 else len(whois_result.name_servers), name_servers],
             ["Creation Date", 1, creation_date],
             ["Expiration Date", 1, expiration_date],
             ["Updated Date", 1, updated_date]]
    return table

def get_correct_date(date):
    """Handle None values and lists"""
    if date is None:
        # If None, return error message
        return "Could not retrieve this information"

    if type(date) == datetime:
        # If type date, it means that it is not a list. The date can be returned.
        return date
    else:
        # It is assumed that date is a list. Return the first object of the list.
        return date[0]


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

    print("\nPerforming WHOIS analysis...\n")
    w = whois.whois(url)
    # print(int(len(w.name_servers)/2))
    print(tabulate(generate_whois_table(w), headers='firstrow', tablefmt='fancy_grid'))

