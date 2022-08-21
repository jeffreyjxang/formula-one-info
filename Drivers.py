# import libraries
import os

import numpy as np
from bs4 import BeautifulSoup

# specify the url

# query the website and return the html to the variable ‘page’
import requests
import firebase_admin

import firebase_admin
from firebase_admin import credentials, firestore
import matplotlib.pyplot as plt

cred = credentials.Certificate(os.getenv('CREDENTIALS'))
firebase_admin.initialize_app(cred)

firestore_db = firestore.client()
page = requests.get("https://www.formula1.com/en/drivers.html")

# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page.content, "html.parser")

# find each item DIV
firstnames = soup.findAll("span", attrs={"class": "d-block f1--xxs f1-color--carbonBlack"})
lastnames = soup.findAll("span", attrs={"class": "d-block f1-bold--s f1-color--carbonBlack"})
currentPoints = soup.findAll("div", attrs={"class": "f1-wide--s"})


print(len(firstnames))
counter = 0
list = []
while counter < len(firstnames):
    list.insert(counter,([firstnames[counter].text.strip() + " " + lastnames[counter].text.strip(), (str(firstnames[counter].text.strip().lower()) + "-" +
                         str(lastnames[counter].text.strip().lower())), currentPoints[counter].text.strip().lower(), counter]))
    counter = counter + 1

for i in list:
    print(i)
print(len(list))
for capital, name, currentPoints, driverIndex in list:
    page = requests.get("https://www.formula1.com/en/drivers/" + name + ".html")

    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(page.content, "html.parser")

    # find each item DIV
    if soup.find("table", attrs={"class": "stat-list"}) is not None:
        infobox = soup.find("table", attrs={"class": "stat-list"})
        topic = infobox.findAll(attrs={"class" : "text"})
        values = infobox.findAll(attrs={"class" : "stat-value"})


        infoboxkey = soup.find("table", attrs={"class": "stat-list"})
        topickey = infobox.findAll(attrs={"class" : "text"})

        values = [value.text.strip() for value in values]
        keys = [key.text.strip() for key in topickey]

        driverYOB = 2022 - int((values[8])[-4:])
        data = {
            keys[0]: values[0],
            keys[1]: values[1],
            keys[2]: values[2],
            keys[3]: values[3],
            u'Current Points': currentPoints,
            keys[4]: values[4],
            keys[5]: values[5],
            keys[6]: values[6],
            keys[7]: values[7],
            keys[8]: values[8],
            keys[9]: values[9],
            u'Driver Index': driverIndex,

        }
        x = int(driverYOB)
        y = float(values[3])
        s = 20
        print(driverYOB)
        plt.scatter(x, y, s)
        plt.annotate(capital,(x, y), fontsize = 7)
        # naming the x axis
        plt.xlabel('Age')
        # naming the y axis
        plt.ylabel('Points Scored')

        # giving a title to my graph
        plt.title('Formula 1 Points Scored vs Age')

        # function to show the plot
        firestore_db.collection(u'Drivers').document(capital).set(data)
plt.show()





