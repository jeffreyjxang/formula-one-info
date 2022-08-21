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
page = requests.get("https://www.formula1.com/en/teams.html")

# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page.content, "html.parser")

# find each item DIV
teamName = soup.findAll("span", attrs={"class": "f1-color--black"})
firstNames = soup.findAll("span", attrs={"class": "first-name f1--xs d-block d-lg-inline"})
lastNames = soup.findAll("span", attrs={"class": "last-name f1-uppercase f1-bold--xs d-block d-lg-inline"})
currentPoints = soup.findAll("div", attrs={"class": "f1-wide--s"})

print(len(teamName))
counter = 0
list = []
while counter < len(teamName):
    officialName = teamName[counter].text.strip()
    adjustedName = teamName[counter].text.strip().replace(" ", "-")
    currentPointsStr = currentPoints[counter].text.strip().lower()
    driverOne = firstNames[counter * 2].text.strip() + " " + lastNames[counter * 2].text.strip()
    driverTwo = firstNames[(counter + 1) * 2 - 1].text.strip() + " " + lastNames[(counter + 1) * 2 - 1].text.strip()
    list.insert(counter, [officialName, adjustedName, driverOne, driverTwo, currentPointsStr, counter])
    counter = counter + 1

for i in list:
    print(i)
print(len(list))
for officialName, adjustedName, driverOne, driverTwo, currentPointsStr, teamIndex in list:
    page = requests.get("https://www.formula1.com/en/teams/" + adjustedName + ".html")

    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(page.content, "html.parser")

    # find each item DIV
    if soup.find("table", attrs={"class": "stat-list"}) is not None:
        infobox = soup.find("table", attrs={"class": "stat-list"})
        topic = infobox.findAll(attrs={"class": "text"})
        values = infobox.findAll(attrs={"class": "stat-value"})

        infoboxkey = soup.find("table", attrs={"class": "stat-list"})
        topickey = infobox.findAll(attrs={"class": "text"})

        values = [value.text.strip() for value in values]
        keys = [key.text.strip() for key in topickey]

        data = {
            keys[0]: values[0],
            keys[1]: values[1],
            keys[2]: values[2],
            keys[3]: values[3],
            keys[4]: values[4],
            keys[5]: values[5],
            keys[6]: values[6],
            keys[7]: values[7],
            keys[8]: values[8],
            keys[9]: values[9],
            keys[10]: values[10],

        }
        for i in range(11):
            print(keys[i])
            print(values[i])
        driverYOB = 2022 - int(values[6])
        x = int(driverYOB)
        if values[7] == "N/A":
            y=0
        else:
            y = float(values[7])
        s = 20
        print(driverYOB)
        plt.scatter(x, y, s)
        plt.annotate(officialName, (x, y), fontsize=7)
        # naming the x axis
        plt.xlabel('Age')
        # naming the y axis
        plt.ylabel('Constructors Championships Won')

        # giving a title to my graph
        plt.title('Formula 1 Championships vs Age')

        # function to show the plot
        firestore_db.collection(u'Teams').document(officialName).set(data)
plt.show()
