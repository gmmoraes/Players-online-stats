import sqlite3
import time
import datetime
import numpy as np
import urllib.request
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
from matplotlib.dates import AutoDateLocator, AutoDateFormatter, date2num
from tkinter import*
plt.style.use('ggplot')



class DataStore():
    def __init__(self):
        self.conn = sqlite3.connect('test2.db')
        self._create_table()
        self.get_all_players()

    def close(self):
        self.cursor.close()
        self.conn.close()



    def get_all_players(self):
        url = "https://secure.tibia.com/community/?subtopic=worlds"
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page.read(), 'html.parser')
        stats = soup.find_all("div", {"id":"RightArtwork"})
        number = soup.find_all("tr", {"class":"Odd"})
        dates = datetime.datetime.now().date()

        for totalOnline in stats:
            divTotal = totalOnline.find_all("div")
            for totalOnline in divTotal:
                total = list(totalOnline.text)
                total[0:5] = [''.join(total[0:5])]
                total[1:19] = [''.join(total[1:19])]
                number = int(total[0])
                name = str(total[1])
                self.data_entry(name,number, dates)


    def _create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS tibiaDB(name TEXT, number REAL, time BLOB, date INTEGER)')

    def data_entry(self,name,number, dates):
        with sqlite3.connect('test2.db') as db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO tibiaDB(name, number, time, date) VALUES(?, ?, ?, ?)",
                           (name, number, time.strftime("%H:%M:%S"), dates))
            self.conn.commit()







class GuiWindow():
    def __init__(self):
        root = Tk()
        frames = Frame(root)
        frames.pack()
        playersOnline = Button(frames, text="Players online list", fg="blue", command = self.graph_players)
        changes = Button(frames, text="Changes in max and min values", fg="blue", command = self.comparison)
        playersOnline.pack(side=LEFT)
        changes.pack(side=LEFT)
        root.mainloop()

    def comparison(self):
        with sqlite3.connect('test2.db') as db:
            cursor = db.cursor()
        highestNumber = cursor.execute('SELECT number, date, time FROM tibiaDB ORDER BY number DESC LIMIT 1')
        for rows in highestNumber:
            datesHigh = rows[1]
            yearHigh, monthHigh, dayHigh = datesHigh.split('-' )
            date_datetime = datetime.datetime.strptime(datesHigh, '%Y-%m-%d')
            int_datesHigh = date2num( date_datetime)
            print(type(int_datesHigh))
            high = float(rows[0])
            print("The highest numbers of players online was " + str(rows[0]))
            
        lowestNumber = cursor.execute('SELECT number,date, time FROM tibiaDB ORDER BY number ASC LIMIT 1')
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

        if int_datesLow == int_datesHigh: 
            percentChanges = "The Number of Players has raised " + str(percent) + "%"
        elif int_datesLow == int_datesHigh: 
            percentChanges = "The number of players has been reduced " + str(percent) + "%"
        elif int_datesLow > int_datesHigh:
            percentChanges = "The number of players has been reduced " + str(percent) + "%"
        elif int_datesLow < int_datesHigh:
            percentChanges = "The Number of Players has raised " + str(percent) + "%"


        fig, ax = plt.subplots() 
        plt.title(percentChanges)
        ax.bar(int_datesLow,low, label="Minimum number of players", color="red")
        ax.bar(int_datesHigh, high, label="Maximum number of players")

        
        locator = AutoDateLocator()
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter( AutoDateFormatter(locator) ) 

        
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


    def graph_players(self):
        with sqlite3.connect('test2.db') as db:
            cursor = db.cursor()
        numberPlayer = cursor.execute('SELECT number FROM tibiaDB')
        values = []
        for row in numberPlayer:
            floats = float(''.join(map(str,row)))
            values.append(floats)
            print(values[-1])

        

        datePlayer = cursor.execute('SELECT date FROM tibiaDB')
        values2 = []
        i = 0
        for row2 in datePlayer:
            floats2 = ''.join(map(str,row2))
            date_datetime = datetime.datetime.strptime(floats2, '%Y-%m-%d')
            allDates = date2num( date_datetime)
            values2.append(allDates)

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


GuiWindow()
