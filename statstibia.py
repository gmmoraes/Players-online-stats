from bs4 import BeautifulSoup
import urllib.request
import sqlite3
from matplotlib import pyplot as plt
from cairocffi import *
from tkinter import*
import time
import datetime
import numpy as np
from matplotlib.dates import AutoDateLocator, AutoDateFormatter, date2num
plt.style.use('ggplot')



class Stats():
    def __init__(self):
        self.conn = sqlite3.connect('test2.db')
        self.c = self.conn.cursor()
        self.create_table()
        self.a = []
        self.dates = datetime.datetime.now().date()
        url = "https://secure.tibia.com/community/?subtopic=worlds"
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page.read(), 'html.parser')
        stats = soup.find_all("div", {"id":"RightArtwork"})
        number = soup.find_all("tr", {"class":"Odd"})

        for totalOnline in stats:
            divTotal = totalOnline.find_all("div")
            for totalOnline in divTotal:
                total = list(totalOnline.text)
                total[0:5] = [''.join(total[0:5])]
                total[1:19] = [''.join(total[1:19])]
                self.number = int(total[0])
                self.name = str(total[1])
                self.data_entry()


            
  



    def create_table(self):
        self.c.execute('CREATE TABLE IF NOT EXISTS tibiaDB(name TEXT, number REAL, time BLOB, date INTEGER)')

    def data_entry(self):
        self.c.execute("INSERT INTO tibiaDB(name, number, time, date) VALUES(?, ?, ?, ?)",
                       (self.name, self.number, time.strftime("%H:%M:%S"), self.dates))
        self.conn.commit()

    def comparison(self):
        highestNumber = self.c.execute('SELECT number, date, time FROM tibiaDB ORDER BY number DESC LIMIT 1')
        for rows in highestNumber:
            datesHigh = rows[1]
            yearHigh, monthHigh, dayHigh = datesHigh.split('-' )
            date_datetime = datetime.datetime.strptime(datesHigh, '%Y-%m-%d')
            int_datesHigh = date2num( date_datetime)
            high = float(rows[0])
            print("The highest numbers of players online was " + str(rows[0]))
            
        lowestNumber = self.c.execute('SELECT number,date, time FROM tibiaDB ORDER BY number ASC LIMIT 1')
        for rows in lowestNumber:
            datesLow = rows[1]
            yearLow, monthLow, dayLow = datesLow.split('-' )
            date_datetime = datetime.datetime.strptime(datesLow, '%Y-%m-%d')
            int_datesLow = date2num( date_datetime)

            print(int_datesHigh)
            print(int_datesLow)

            low = float(rows[0])
            print("The lowest number of players online was "+ str(rows[0]))

        percent = round((((low/high) * 100) - 100) *-1, 2)


        if int_datesLow == int_datesHigh: 
            percentChanges = "The Number of Players has raised " + str(percent) + "%"
        elif int_datesLow == int_datesHigh: 
            percentChanges = "The number of players has been reduced " + str(percent) + "%"
        elif int_datesLow > int_datesHigh:
            percentChanges = "The number of players has been reduced " + str(percent) + "%"
        elif int_datesLow < int_datesHigh:
            percentChanges = "The Number of Players has raised " + str(percent) + "%"


        #Creates suplot and Graphs
        fig, ax = plt.subplots() #ver porque precisa de fig
        plt.title(percentChanges)
        ax.bar(int_datesLow,low, label="Minimum number of players", color="red")
        ax.bar(int_datesHigh, high, label="Maximum number of players")

        
        #format date strings on xaxis:
        locator = AutoDateLocator()#esses codigos localizam e formatam o codigo de unix para data
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter( AutoDateFormatter(locator) ) 

        #adjust x limits and apply autoformatter fordisplay of dates
        #obs como estou com duas barras nao precisa desses
        if int(yearHigh) > int(yearLow) or int(yearHigh) == int(yearLow) and int(monthHigh) > int(monthLow) or int(yearHigh) == int(yearLow) and int(monthHigh) == int(monthLow) and int(dayHigh) > int(dayLow):
            if int(dayHigh) < 30 and int(dayLow) > 1 and int(monthHigh) != 2:
                dayLow = str(int(dayLow) - 1)
                dayHigh = str(int(dayHigh) + 1)
            else:
                monthHigh = str(int(monthHigh) + 1)
                monthLow = str(int(monthLow) - 1)
            joinHigh = yearHigh + '-' + monthHigh+ '-'+ dayHigh
            joinLow = yearLow +'-' + monthLow+ '-' + dayLow
            min_date = date2num( datetime.datetime.strptime(joinLow, '%Y-%m-%d'))
            max_date = date2num( datetime.datetime.strptime(joinHigh, '%Y-%m-%d'))
        else:
            if int(dayLow) < 30 and int(dayHigh) > 1 and int(monthLow) != 2:
                dayLow = str(int(dayLow) + 1)
                dayHigh = str(int(dayHigh) - 1)
            else:
                monthHigh = str(int(monthHigh) - 1)
                monthLow = str(int(monthLow) + 1)
            joinHigh = yearHigh + '-' + monthHigh+ '-'+ dayHigh
            joinLow = yearLow +'-' + monthLow+ '-' + dayLow
            min_date = date2num( datetime.datetime.strptime(joinHigh, '%Y-%m-%d'))
            max_date = date2num( datetime.datetime.strptime(joinLow, '%Y-%m-%d'))

        ax.set_xlim([min_date, max_date])
        fig.autofmt_xdate()
        plt.legend()
        plt.show()
        
            


    def graphPlayers(self):
        numberPlayer = self.c.execute('SELECT number FROM tibiaDB')
        values = []
        for row in numberPlayer:
            floats = float(''.join(map(str,row)))
            values.append(floats)
            print(values[-1])

        

        datePlayer = self.c.execute('SELECT date FROM tibiaDB')
        values2 = []
        i = 0
        for row2 in datePlayer:
            floats2 = ''.join(map(str,row2))
            date_datetime = datetime.datetime.strptime(floats2, '%Y-%m-%d')
            allDates = date2num( date_datetime)
            values2.append(allDates)


        print(len(values2))
         


        fig, ax = plt.subplots() 
        ax.plot(values2,values, label="Minimum number of players", color="red")
        plt.title('Tibia Players Online')
        plt.ylabel('Number of players')
        plt.xlabel('Dates')
        locator = AutoDateLocator()
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter( AutoDateFormatter(locator) )
        fig.autofmt_xdate()
        plt.show()

        self.c.close()
        self.conn.close()

class tkinter():
    def __init__(self):
        root = Tk()
        frames = Frame(root)
        frames.pack()
        playersOnline = Button(frames, text="Players online list", fg="blue", command = self.executePlayers)
        changes = Button(frames, text="Changes in max and min values", fg="blue", command = self.executeComparison)
        playersOnline.pack(side=LEFT)
        changes.pack(side=LEFT)
        root.mainloop()


    def executeComparison(self):
        Stats().comparison()

    def executePlayers(self):
        Stats().graphPlayers()



        
        

        
    



tkinter()
Stats()


