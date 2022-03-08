import urllib.request
from bs4 import BeautifulSoup, formatter
import re
import requests
import hashlib
import os
from datetime import datetime

class ticket:
    def __init__(self, title, link):
        self.title = title
        self.link = link


def getTrentLink():
    page = urllib.request.urlopen('https://oceantickets.ecwid.com/')
    soup = BeautifulSoup(page, 'html.parser')
    links = soup.find_all('a', href=re.compile('TRENT-WEDNESDAY-TICKETS'))
    #links = soup.find_all(title='TRENT')
    trentLink = ''
    for link in links:
        trentLink = link.get('href')

    return trentLink

def getTickets(url):
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    tickets = []
    for EachPart in soup.findAll('a', {'class': 'grid-product__title'}):
        text = EachPart.text
        link = EachPart.get('href')
        tickets.append(ticket(text, link))
    return tickets

def formatTickets(tickets):
    ticketsString = '@here TICKETS CURRENTLY AVAILABLE\n'
    for ticket in tickets:
        ticketsString = ticketsString + ticket.title + '\n' + ticket.link + '\n\n'
    return ticketsString.replace('\n', '\\n')

def sendAlert(message):
    webhookURL = 'https://discordapp.com/api/webhooks/899006686013063242/UCOYx1YC0f1OW6TamKZNTkX36chCkCGKncXY1Bwqk2JC4tQikoUQV-9FzS3ALlHm9lIH'
    headers = {
    'Content-Type': 'application/json',
    }
    data = '{"username": "Oceanator", "content": "' + message +'"}'

    response = requests.post(webhookURL, headers=headers, data=data)
    print(response)
    print('TICKETS CHANGED AT:')
    print(datetime.now())

def checkTickets(tickets):
    file = 'hashes/' + hashString(tickets)
    if os.path.isfile(file):
        #exit program
        print('TICKETS UNCHANGED AT: ')
        print(datetime.now())
        exit()

def hashString(string):
    return  hashlib.md5(string.encode()).hexdigest()


ticketString = formatTickets(getTickets(getTrentLink()))
checkTickets(ticketString)
f = open('hashes/' + hashString(ticketString), 'x')
f.close()
sendAlert(ticketString)
sendAlert(ticketString)
sendAlert(ticketString)
sendAlert(ticketString)
sendAlert(ticketString)