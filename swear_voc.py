from bs4 import BeautifulSoup
import requests

# constants
WEBSITE_URL = "https://www.noswearing.com/dictionary/"
OUTFILE = "swear_voc.txt"

for i in range(26):
    c = chr(i + 97) #ascii of a-z
    website = requests.get(WEBSITE_URL + c)
    soup_scraper = BeautifulSoup(website.content, "html.parser")

    table = soup_scraper.find("table", width="650") #swear word tables containing all the swear words starting with c
    b_tags = table.find_all("b")[:-1] #remove the last tags for "more slang translators"
    
    with open(OUTFILE, "a") as f:
        [f.write(b.string + "\n") for b in b_tags]
    f.close()

