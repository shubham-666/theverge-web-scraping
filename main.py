import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
from datetime import datetime
import json
import csv
import sqlite3
import datetime

url = "https://www.theverge.com/archives/1"

response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

article_links = soup.find("script", attrs={"id": "__NEXT_DATA__"})
json_object = json.loads(article_links.contents[0])
data = []
Url=(json_object['props']['pageProps']['hydration']['responses'][0]['data']['community']['frontPage']['entryGroup']['recentEntries']['results'])

# print(Url)
title=[]
author=[]
postUrl=[]
date=[]
for i in range(40) :
    title.append(Url[i]["title"])
    author.append(Url[i]["author"]["fullName"])
    postUrl.append(Url[i]["url"])
    date.append(Url[i]["publishDate"])
# print(date)
data={'title' : title, 'author name': author,'post url' :postUrl,'Date':date}
df=pd.DataFrame(data)
print(df)
df.to_csv("verge.csv")



# Import required modules


# Connecting to the geeks database
connection = sqlite3.connect('Verge.db')

# Creating a cursor object to execute
# SQL queries on a database table
cursor = connection.cursor()

# Table Definition
create_table = '''CREATE TABLE Articles(
				id INTEGER PRIMARY KEY,
				title TEXT NOT NULL,
				url TEXT NOT NULL,
				author TEXT NOT NULL,
				date DATETIME NOT NULL);
				'''

# Creating the table into our
# database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Articles'")
table_exists = cursor.fetchone()
if table_exists is not None:
    te=table_exists[0]
else:
    te=0
print(te)
if te==0:
    print(te)
    print("hey")
    cursor.execute(create_table)



def addData(x):
    with open('verge.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row
        for row in reader:
            if int(row[0])>x:
                date_str = row[4]
                date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
                row[4] = date_obj
                cursor.execute('''INSERT INTO Articles (id,title, author, url, date)
                            VALUES (?, ?, ?, ?, ?)''', row)


cursor.execute("SELECT id FROM Articles ORDER BY id DESC LIMIT 1")
last_id = cursor.fetchone()
print(last_id)

if last_id is None:
    addData(-1)
else:
    print(last_id[0])
    
    addData(last_id[0])



connection.commit()

# closing the database connection
connection.close()
# lect * from Articles;