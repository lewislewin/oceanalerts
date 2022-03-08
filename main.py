from pickle import TRUE
import urllib.request
from bs4 import BeautifulSoup
import re
import requests
import hashlib
import os
from datetime import datetime

DEBUG = False
TIMEFORMAT = "%m/%d/%Y - %H:%M:%S"

class ticket:
    def __init__(self, title, link):
        self.title = title
        self.link = link

# A function to get the link for the trent wednesday tickets
# Returns a string
def getTrentLink():
    oceanWebsiteURL = 'https://oceantickets.ecwid.com/'
    ticketString = 'TRENT-WEDNESDAY-TICKETS'
    
    print('INFO: Parsing website: ' + oceanWebsiteURL)
    page = urllib.request.urlopen(oceanWebsiteURL)
    soup = BeautifulSoup(page, 'html.parser')
    links = soup.find_all('a', href=re.compile(ticketString))
    
    trentLink = ''
    for link in links:
        trentLink = link.get('href')
    if trentLink == '':
        print('INFO: No link found')
        return trentLink
    
    print('INFO: Found link: ' + trentLink)
    return trentLink

#Finds tickets in the website and returns them if they are there
def getTickets(url):
    print('INFO: Getting tickets from trent page')
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    tickets = []

    for EachPart in soup.findAll('a', {'class': 'grid-product__title'}):
        text = EachPart.text
        link = EachPart.get('href')
        tickets.append(ticket(text, link))
    
    if len(tickets) > 0:
        print('INFO: Found tickets:')
        for ticketUrl in tickets:
            print(ticketUrl.title)
    return tickets

#Formats the tickets
def formatTickets(tickets):
    print('INFO: Formatting tickets')
    ticketsString = '@here TICKETS CURRENTLY AVAILABLE\n'
    for ticket in tickets:
        ticketsString = ticketsString + ticket.title + '\n' + ticket.link + '\n\n'
    return ticketsString.replace('\n', '\\n')

#Sends an alert to the discord
def sendAlert(message):
    print('INFO: Sending alert')
    webhookURL = 'https://discordapp.com/api/webhooks/899006686013063242/UCOYx1YC0f1OW6TamKZNTkX36chCkCGKncXY1Bwqk2JC4tQikoUQV-9FzS3ALlHm9lIH'
    headers = {
    'Content-Type': 'application/json',
    }
    data = '{"username": "Oceanator", "content": "' + message +'"}'

    if not DEBUG:
        response = requests.post(webhookURL, headers=headers, data=data)
    else:
        response = "INFO: Debug mode, no data returned"

    print(response)
    print('INFO: Tickets have been updated at: ', datetime.now().strftime(TIMEFORMAT))
    print(datetime.now())

#Checks if tickets have changed
def checkTickets(tickets):
    print('INFO: Checking if tickets changed')
    file = 'hashes/' + hashString(tickets)
    if os.path.isfile(file):
        print('INFO: Tickets unchanged at: ', datetime.now().strftime(TIMEFORMAT))
        exit()

#Returns a hash of a string
def hashString(string):
    return  hashlib.md5(string.encode()).hexdigest()

def sendMultipleAlerts(ticketString, numberOfNotifications):
    
    i = 0
    while i < numberOfNotifications:
        sendAlert(ticketString)
        i += 1

ticketString = formatTickets(getTickets(getTrentLink()))
checkTickets(ticketString)

f = open('hashes/' + hashString(ticketString), 'x')
f.close()

sendMultipleAlerts(ticketString, 5)