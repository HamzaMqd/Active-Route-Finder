import customtkinter as ctk
import tkintermapview as tmv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from matplotlib.figure import Figure
import datetime as dt
from geopy import distance
import random
import string



#presetting window theme and mode

ctk.set_default_color_theme('blue')
ctk.set_appearance_mode('dark')


class arf(ctk.CTk):
     def __init__(self, title, size):
         super().__init__()

        #creating presets for window size and title

         self.title(title)
         self.minsize(size[0], size[1])
         #self.maxsize(size[0], size[1])
         self.geometry(f'{size[0]}x{size[1]}')

         #creating grid for widgets

         self.grid_rowconfigure((0,1,2), weight=1)
         self.grid_columnconfigure((0,1), weight=1)


         #create frame for menu buttons

         self.barFrame = ctk.CTkFrame(self, corner_radius=10)
         self.barFrame.grid(row=0, column=0, columnspan=1, rowspan=3, padx=10, pady=10, sticky='nsew')
         self.barFrame.grid_columnconfigure(4, weight=1)
         self.barFrame.grid_rowconfigure(2, weight=1)
         self.barFrame.grid_propagate(False)

         #add widgets to barFrame

         self.textLabel = ctk.CTkLabel(self.barFrame, text='welcome to the active route finder')
         self.textLabel.grid(row=0, column=0, padx=10) 

         self.startRoute = ctk.CTkButton(self.barFrame, text='start route', width=270)
         self.startRoute.grid(row=1, column=0, padx=10, pady=10)

         self.entryButton = ctk.CTkButton(self.barFrame, text='connect marker', command=self.pathConnect)
         #self.entryButton.configure(command = self.clearInput)
         self.entryButton.grid(row=1, column=1, padx=10, pady=10, sticky='e')

         self.clearButton = ctk.CTkButton(self.barFrame, text='clear route', command = self.clearInput)
         self.clearButton.grid(row=1, column=2, padx=10, pady=10, sticky='e')

         #create a frame for the tabview and configure it

         self.multiBox = ctk.CTkTabview(self.barFrame)
         self.multiBox.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')
         self.multiBox.add('data')
         self.multiBox.add('settings')
         self.multiBox.add('route log')
         self.multiBox.add('user manual')
         self.multiBox.set('data')

         self.multiBox.tab('user manual').grid_columnconfigure(1, weight=1)
         self.multiBox.tab('user manual').grid_rowconfigure(1, weight=1)

         self.multiBox.tab('settings').grid_columnconfigure((0,1), weight=1)
         self.multiBox.tab('settings').grid_rowconfigure((0,1,2,3), weight=1)

         self.multiBox.tab('data').grid_columnconfigure((0,1,2), weight=1)
         self.multiBox.tab('data').grid_rowconfigure((0,1,2), weight=1)

         self.multiBox.tab('route log').grid_columnconfigure(1, weight=1)
         self.multiBox.tab('route log').grid_rowconfigure(1, weight=1)

        #create widgets for the settings tab

         self.appeareanceModeText = ctk.CTkLabel(self.multiBox.tab('settings'), text='appearance mode', anchor='w')
         self.appeareanceModeText.grid(row=0, column=0, padx=5, pady=5)

         self.appeareanceModeOption = ctk.CTkOptionMenu(self.multiBox.tab('settings'), values=['light', 'dark'], command=self.changemode)
         self.appeareanceModeOption.grid(row=1, column=0, padx=5, pady=5)

         self.scalingLabel = ctk.CTkLabel(self.multiBox.tab('settings'), text='user interface scaling', anchor='w')
         self.scalingLabel.grid(row=2, column=0, padx=5, pady=5)

         self.scalingMenu = ctk.CTkOptionMenu(self.multiBox.tab('settings'), values=['100%', '80%,', '110%'])
         self.scalingMenu.grid(row=3, column=0, padx=5, pady=5)

         self.valueLabel = ctk.CTkLabel(self.multiBox.tab('settings'), text='configure input data type')
         self.valueLabel.grid(row=0, column=1, padx=5, pady=5)

         self.unitLabel = ctk.CTkLabel(self.multiBox.tab('settings'), text='configure unit measurements')
         self.unitLabel.grid(row=2, column=1, padx=10, pady=10)

         self.unitOpt = ctk.CTkOptionMenu(self.multiBox.tab('settings'), values=['miles', 'kilometres'])
         self.unitOpt.grid(row=3, column=1, padx=10, pady=10)


        #create frame and add widgets for the statistics tab

         self.fuelEntry = ctk.CTkEntry(self.multiBox.tab('data'), placeholder_text='enter fuel price per litre')
         self.fuelEntry.grid(row=1, column=0, padx=10, pady=10, sticky='new')

         self.consumptionEntry = ctk.CTkEntry(self.multiBox.tab('data'), placeholder_text='enter fuel mpg')
         self.consumptionEntry.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

         self.fuelEntryButton = ctk.CTkButton(self.multiBox.tab('data'), command = self.validations, text='input fuel data')
         self.fuelEntryButton.grid(row=1, column=0, padx=10, pady=10, sticky='sew')

         self.dataBox = ctk.CTkScrollableFrame(self.multiBox.tab('data'), corner_radius=10, height=700, width=300)
         self.dataBox.grid(row=1, column=1, rowspan=2, padx=10, pady=10, sticky='nse')

         self.dataLabel = ctk.CTkLabel(self.dataBox, corner_radius=10, text='')
         self.dataLabel.grid(padx=10, pady=10)

         self.placeholder = ctk.CTkButton(self.multiBox.tab('data'), text='calculate distance')
         self.placeholder.grid(row=2, column=0, padx=10, pady=10, sticky='ew') 




        #create and add widgets to the usermanual tab

         self.scrollable = ctk.CTkScrollableFrame(self.multiBox.tab('user manual'))
         self.scrollable.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')
         self.scrollable.grid_columnconfigure(1, weight=1)
         self.scrollable.grid_rowconfigure(1, weight=1)

         self.manualText = ctk.CTkLabel(self.scrollable, corner_radius=10, height=1000)
         self.manualText.grid(column=1, row=1, columnspan=1, padx=10, pady=10, sticky='nsew')


        #lines 104 to 108 open an external text file in order to read the user manual and place it into the user manual tab

         f = open('arfusermanual.txt', 'r')
         textFile = f.read()
         f.close()

         self.manualText.configure(text=textFile)

        #creating new infrastructure for a textbox instead of label and scrollable frame so data can be inputted into route log easier

         self.logText = ctk.CTkTextbox(self.multiBox.tab('route log'))
         self.logText.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')


        #create a frame for the map overlay

         self.displayFrame = ctk.CTkFrame(self, corner_radius=10)
         self.displayFrame.grid(row=0, column=1, columnspan=1, rowspan=3, padx=10, pady=10, sticky='nsew')
         self.displayFrame.grid_columnconfigure(1, weight=1)
         self.displayFrame.grid_rowconfigure(1, weight=1)
         self.displayFrame.grid_propagate(False)


        #add overlay to overlay frame

         self.overlay = tmv.TkinterMapView(self.displayFrame, corner_radius=10)
         self.overlay.place()
         self.overlay.grid(column=1, row=1, columnspan=1, rowspan=1, padx=10, pady=10, sticky='nsew')

         self.overlay.add_left_click_map_command(self.leftClick)

         #creating lists with the global scope in order to be used in the route procedures

         global pathList ; pathList = []
         global nodeList ; nodeList = []
         global idList ; idList = []
         global positionList ; positionList = []
         global totalList ; totalList = []
         global distList ; distList = []
         



    #creating functionality for the change theme button

     def changemode(self, newmode: str):
         ctk.set_appearance_mode(newmode)

    #creating functionality for the user interface scale customiser

     def differscale(self, newScale: str):
         newScale_float = int(newScale.replace('%', '')) / 100
         ctk.set_widget_scaling(newScale_float)

    #creating functionality for the user input bar

     def entryInput(self):
         inputValue = self.entryBox.get()
         print(inputValue)

     def leftClick(self, coordinates_tuple):

         global currentNode ; currentNode = (round(coordinates_tuple[0], 4), round(coordinates_tuple[1], 4))
         nodeList.append(currentNode)

         for i in range(1):
             global identifier ; identifier = ''.join(random.choices(string.ascii_uppercase, k=4))
             idList.append(identifier)

         totalList.append(tuple[nodeList[-1], idList[-1]])

         #create marker from the selected coordinates from the left click event on map overlay
         self.overlay.set_marker(coordinates_tuple[0], coordinates_tuple[1], text=identifier)

         #simulateanously open text file and write coordinate data and unique identifiers to that text file
         fileCommand = open('arfrouteinfo.txt', 'a')
         fileCommand.write(str(currentNode))
         fileCommand.write(identifier)
         fileCommand.write('\n')
         fileCommand.close()

         fileRead = open('arfrouteinfo.txt', 'r')

         #read the coordinate and identifier data from arfrouteinfo.txt in order to display to the route log
         self.logText.insert('0.0', fileRead )

         fileRead.close()

         #integrate a running total for distance in left click event

         if len(nodeList) > 1:
             for x in range(1):
                 if self.unitOpt == 'kilometers':
                     dist = distance.distance(nodeList[-1], nodeList[-2]).kilometers
                     distList.append(dist)
                     if len(distList) > 0:
                         totalDistance = sum(distList)
                         print(nodeList)
                         print(idList)
                         print(totalList)
                         print(distList)
                         print(totalDistance)
                 
                 
                 else:
                     dist = distance.distance(nodeList[-1], nodeList[-2]).miles
                     distList.append(dist)
                     if len(distList) > 0:
                         totalDistance = sum(distList)
                         print(nodeList)
                         print(idList)
                         print(totalList)
                         print(distList)
                         print(totalDistance)
                        
         if len(nodeList) > 1:
             self.overlay.set_path(nodeList)


     # this procedure ensures that when the 'clear' button is pressed that the routeinfo file and markers are also cleared.
     def clearInput(self):
         self.overlay.delete_all_marker
         self.overlay.delete_all_path
         with open('arfrouteinfo.txt', 'r+') as dataFile:
             dataFile.truncate(0)

     #create a validation proceduere that validates fuel consumption and fuel price inputs in order to keep accuracy of calculations

     def validations(self):

         try:
             inputData = float(self.fuelEntry.get())
             print(len(str(inputData)))

             if len(str(inputData)) < 6:
                 print('input too short')
             if len(str(inputData)) > 6:
                 print('input too long')

         except:
             print('invalid fuel price input')

         try:
             consumptionInput = float(self.consumptionEntry.get())
             print(len(str(consumptionInput)))

             if len(str(consumptionInput)) > 4:
                 print('mpg figure too large')
             if len(str(consumptionInput)) < 4:
                 print('mpg figure too small')
         except:
             print('invalid fuel consumption input')

     def pathConnect(self):
         pathList.append(currentNode)
         print(pathList) 

         # create code for path connects between placed nodes and visible markers

#this command will make sure that the window updates as the user goes about accessing it as well as ensuring the size and title of window

if __name__ == '__main__':
    app = arf('active route finder', (1300,900))
    app.mainloop()

print('user has exited the active route finder')

#wiping the data from the text file after the program is terminated

with open('arfrouteinfo.txt', 'r+') as dataFile:
     dataFile.truncate(0)  