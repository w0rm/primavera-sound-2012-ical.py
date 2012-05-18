#!/usr/bin/env python
# coding: utf-8

import urllib
from datetime import datetime, timedelta
import pytz
import vobject
from BeautifulSoup import BeautifulSoup

url = "http://sanmiguelprimaverasound.es/programacion?lang=en"
soup = BeautifulSoup(urllib.urlopen(url).read()) 

tz = pytz.utc
cal = vobject.newFromBehavior('vcalendar')
cal.add('prodid').value = '-//Andrey Kuzmin//goo.gl/fNwV1//'

content = soup.find("div", {"class": "full-width"})

for day_list in content.findAll("dt", {"class": "title"}):
    weekday, month, date = day_list.text.split()
    date = int(date) 
    month = dict(May=5,June=6)[month] 
    
    artists_list = day_list.findNextSibling("dd")
    for artist in artists_list.findAll("tr"):
        if artist.find("td", {"class": "artista"}):
            title = artist.find("td", {"class": "artista"}).text
            if not title:
                continue
            
            venue = artist.find("td", {"class": "sala"}).text
            time = artist.find("td", {"class": "hora"}).text
            
            event = cal.add('vevent')
            event.add('summary').value =  '%s at %s' % (title, venue)
            event.add('location').value = venue
            
            if time:
                hours, minutes = time.split(":")[:2]
                hours = int(hours)
                minutes = int(minutes)
                
                dtstart = datetime(2012, month, date, hours, minutes, 0, tzinfo=tz)
                if hours < 6: # if time is less than 6am, then it is the next day
                    dtstart += timedelta(hours=24)
                event.add('dtstart').value = dtstart
                event.add('dtend').value = dtstart+timedelta(hours=1) # Assuming that each show takes 1 hour
            else:
                # Event takes the whole day if no time specified
                dtstart = datetime(2012, month, date, 0, 0, 0, tzinfo=tz)
                event.add('dtstart').value = dtstart
                event.add('dtend').value = dtstart+timedelta(hours=24)

f = open('primavera_sound_2012.ics', 'wb')
f.write(cal.serialize())
f.close()


