# CYB 220 Final Project: Website analyser

## How to use
Python 3 should be used. `https://` should be present in the url.

`python main.py <url>`


## Dependencies
Use `pip install <dependency>` to install the following dependencies:
* requests
* lxml
* python-whois
* tabulate

## Features
CLI app to get information about a webpage.

### Page content:
* number of links
* number of div
* number of words
* number of file linked (css, js etc..)
* number of images

Maybe:
* colors used

### Security
* get whois info
* get ssl/tls report (https://www.ssllabs.com/ssltest/)

### Misc
* time to load
