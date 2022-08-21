# import libraries

from bs4 import BeautifulSoup

# specify the url

# query the website and return the html to the variable ‘page’
import requests



page = requests.get("https://www.formula1.com/en/drivers.html")

# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page.content, "html.parser")

# find each item DIV
firstnames = soup.findAll("span", attrs={"class": "d-block f1--xxs f1-color--carbonBlack"})
lastnames = soup.findAll("span", attrs={"class": "d-block f1-bold--s f1-color--carbonBlack"})

print(len(firstnames))
counter = 0
list = []
while counter < len(firstnames):
    list.insert(counter,[firstnames[counter].text.strip() + " " + lastnames[counter].text.strip(), (str(firstnames[counter].text.strip().lower()) + "-" +
                         str(lastnames[counter].text.strip().lower()))])
    counter = counter + 1

for i in list:
    print(i)
print(len(list))
for capital, name in list:
    page = requests.get("https://www.formula1.com/en/drivers/" + name + ".html")

    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(page.content, "html.parser")

    # find each item DIV
    if soup.find("table", attrs={"class": "stat-list"}) is not None:
        infobox = soup.find("table", attrs={"class": "stat-list"})
        topic = infobox.findAll(attrs={"class" : "text"})
        values = infobox.findAll(attrs={"class" : "stat-value"})
        combinedString = str(capital + str(": "))
        counter = 0
        while (counter < len(topic)):
            combinedString += "\n " + topic[counter].text.strip()  + ": " + values[counter].text.strip()
            counter = counter + 1

        print(combinedString)
