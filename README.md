# house_scraping
This program helps you to find a house, scraping the web pisos.com and sending you an email with the information

You need to install the libraries:

- bs4
- requests
- lxml
- email
- unidecode

On the main.py you have to change:
 - #url variable with your search.
 - #From/To/login user mail

The idea is to put this script on a server, so that it runs every hour (or whatever time you prefer), 
and send you an email if find new results and a .txt file with the historic searches
All new searches are saved in a file and only send an email when find new results

This script is UNDER DEVELOPMENT
