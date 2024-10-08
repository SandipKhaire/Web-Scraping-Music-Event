import requests
import selectorlib
import smtplib,ssl
import os
import time
import sqlite3

conn = sqlite3.connect("data.db")


URL = "http://programmer100.pythonanywhere.com/tours/"


def scrape(url):
    """ Scrape the page source from the URL"""
    response = requests.get(url)
    source = response.text
    return source

def extract(source):
    extractor= selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value

def send_mail(message):
    host = "smtp.gmail.com"
    port = 465

    username = "pydata7@gmail.com"
    password=os.getenv("PY_DATA7_PASSWORD")

    receiver = "pydata7@gmail.com"
    context = ssl.create_default_context()


    with smtplib.SMTP_SSL(host,port,context=context) as server:
        server.login(username,password)
        server.sendmail(username,receiver,message)

    print("Email was sent!")

 

def store(extracted):
    row =extracted.split(",")
    row = [item.strip() for item in row]
    cursor = conn.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)",row)
    conn.commit()



def read(extracted):
    row =extracted.split(",")
    row = [item.strip() for item in row]
    band,city,date = row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM events WHERE band=? AND city=? AND date=?',(band,city,date))
    rows=cursor.fetchall()
    return rows


if __name__=="__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)
        if extracted!="No upcoming tours":
            row=read(extracted)
            if not row:
                store(extracted)
                send_mail(message="New Event is found!!")
        time.sleep(5)


        

