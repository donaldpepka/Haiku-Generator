from bs4 import BeautifulSoup, SoupStrainer
import requests


# takes in url as string; returns html of page as a bs4 object
def get_html(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    soup = soup.find('article')
    return soup

"""Need some way to remove all the extra lines"""
# takes in url as string; returns a list containing each haiku on the page as a string
def get_haikus(url):
    soup = get_html(url)
    haikus = []
    for code in soup.find_all("p", class_="haiku"):
        haiku = ""
        next_line = code
        while next_line.next_element != "\n":
            try:
                next = next_line.next_element
                haiku = haiku + " " + next
            except TypeError:
                haiku = ""
                break
            next_line = next_line.findNext('br')
        haiku = haiku.replace("\n", "").replace("\r", "")
        haikus.append(haiku)
    return haikus


# takes in url as string; returns a list containing each link on the page as a string
def get_links(url):
    base = "http://www.tempslibres.org/tl/tlphp/"
    links = []

    # get partial haiku links
    soup = get_html(url)
    for link in soup.find_all('a'):
        if link.has_attr('href'):
            links.append(link['href'])

    # fix links, so that each link in haiku_links is a true url.
    for i in range(len(links)):
        links[i] = base + links[i]
    return links


database_url = "http://www.tempslibres.org/tl/tlphp/dbauteursl.php?lang=en&lg=e"
haiku_links = get_links(database_url)
all_authors = []
all_haikus = []

for link in haiku_links:
    print(link)
    all_authors.append(get_haikus(link))
for author in all_authors:
    for haiku in author:
        all_haikus.append(haiku)


# write final scraped data to Haikus.csv, one haiku per line.
with open('Haikus.csv', 'w', encoding="utf8") as output:
    for haiku in all_haikus:
        output.write(haiku+'\n')
