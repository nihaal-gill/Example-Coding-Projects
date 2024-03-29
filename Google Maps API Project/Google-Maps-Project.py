import tkinter
from tkinter import Tk, Canvas, Frame, Button, Label, Entry, END, LEFT, BOTTOM, TOP, RIGHT, SUNKEN
import math
import ssl
from urllib.request import urlopen, urlretrieve
from urllib.parse import urlencode, quote_plus
import json

GOOGLEAPIKEY = "AIzaSyCSKoYf7PqR5gfAe8I_hLGTmVciV616Ij0"

class Globals:
    rootWindow = None
    mapLabel = None
    locationEntry = None
    defaultLocation = "Mauna Kea, Hawaii"
    mapLocation = defaultLocation
    mapFileName = 'googlemap.gif'
    mapSize = 400
    zoomLevel = 9
    mapType = 'roadmap'


# Given a string representing a location, return 2-element tuple
# (latitude, longitude) for that location
#
# See https://developers.google.com/maps/documentation/geocoding/
# for details
#
def geocodeAddress(addressString):
    urlbase = "https://maps.googleapis.com/maps/api/geocode/json?address="
    geoURL = urlbase + quote_plus(addressString)
    geoURL = geoURL + "&key=" + GOOGLEAPIKEY

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    stringResultFromGoogle = urlopen(geoURL, context=ctx).read().decode('utf8')
    jsonResult = json.loads(stringResultFromGoogle)
    if (jsonResult['status'] != "OK"):
        print("Status returned from Google geocoder *not* OK: {}".format(jsonResult['status']))
        return (0.0, 0.0)  # this prevents crash in retrieveMapFromGoogle - yields maps with lat/lon center at 0.0, 0.0
    loc = jsonResult['results'][0]['geometry']['location']
    return (float(loc['lat']), float(loc['lng']))


# Contruct a Google Static Maps API URL that specifies a map that is:
# - is centered at provided latitude lat and longitude long
#
# - Globals.mapSize-by-Globals.mapsize in size (in pixels),
# - is "zoomed" to the Google Maps zoom level in Globals.zoomLevel
#
# See https://developers.google.com/maps/documentation/static-maps/
#
def getMapUrl(lat, lng):
    urlbase = "http://maps.google.com/maps/api/staticmap?"
    args = "center={},{}&zoom={}&size={}x{}&maptype={}&markers=color:red|label:S|{},{}&sensor=false&format=gif".format(lat, lng, Globals.zoomLevel, Globals.mapSize,
                                                               Globals.mapSize,Globals.mapType,lat,lng)
    args = args + "&key=" + GOOGLEAPIKEY
    mapURL = urlbase + args
    return mapURL


# Retrieve a map image via Google Static Maps API:
# - centered at the location specified by global propery mapLocation
# - zoomed according to global property zoomLevel (Google's zoom levels range from 0 to 21)
# - width and height equal to global property mapSize
# Store the returned image in file name specified by global variable mapFileName
#
def retrieveMapFromGoogle():
    lat, lng = geocodeAddress(Globals.mapLocation)
    url = getMapUrl(lat, lng)
    urlretrieve(url, Globals.mapFileName)


##########
#  basic GUI code

def displayMap():
    retrieveMapFromGoogle()
    mapImage = tkinter.PhotoImage(file=Globals.mapFileName)
    Globals.mapLabel.configure(image=mapImage)
    # next line necessary to "prevent (image) from being garbage collected" - http://effbot.org/tkinterbook/label.htm
    Globals.mapLabel.mapImage = mapImage


def readEntryAndDisplayMap():
    #### you should change this function to read from the location from an Entry widget
    #### instead of using the default location
    locationString = Globals.locationEntry.get()
    Globals.mapLocation = locationString
    displayMap()

#function for being able to zoom in
def ZoomIn():
   Globals.zoomLevel += 1
   displayMap()

#function for being able to zoom out
def ZoomOut():
    Globals.zoomLevel -= 1
    displayMap()

def radioButtonChosen():
    global selectedButtonText
    global choiceVar
    global label

    if choiceVar.get() == 1:
        selectedButtonText = "roadmap"
        Globals.mapType = "roadmap"
    elif choiceVar.get() == 2:
        selectedButtonText = "satellite"
        Globals.mapType = "satellite"
    elif choiceVar.get() == 3:
        selectedButtonText = "terrain"
        Globals.mapType = "terrain"
    else:
        selectedButtonText = "hybrid"
        Globals.mapType = "hybrid"
    displayMap()
    label.configure(text="Radio button choice is: {}".format(selectedButtonText))

def initializeGUIetc():
    global selectedButtonText
    global choiceVar
    global label

    Globals.rootWindow = tkinter.Tk()
    Globals.rootWindow.title("HW9")

    locationLabelFrame = tkinter.Frame(Globals.rootWindow)
    locationLabel = Label(locationLabelFrame, text="Enter the location:")
    locationLabelFrame.pack()
    locationLabel.pack()

    Globals.locationEntry = tkinter.Entry()
    Globals.locationEntry.pack()

    '''
    seachTermFrame = tkinter.Frame(Globals.rootWindow)
    seachTermFrame.pack()
    seachTermLabel = Label(seachTermFrame, text="Enter your search term:")
    seachTermLabel.pack()
    '''
    mainFrame = tkinter.Frame(Globals.rootWindow)
    mainFrame.pack()

    # you need to add an Entry widget that allows you to type in an address
    # The click function should extract the location string from the Entry widget
    # and create the appropriate map.
    readEntryAndDisplayMapButton = tkinter.Button(mainFrame, text="Show me the map!", command=readEntryAndDisplayMap)
    readEntryAndDisplayMapButton.pack()

    ZoomInButton = tkinter.Button(mainFrame,text="+", command=ZoomIn)
    ZoomInButton.pack()

    ZoomOutButton = tkinter.Button(mainFrame,text="-",command=ZoomOut)
    ZoomOutButton.pack()

    selectedButtonText = ""
    choiceVar = tkinter.IntVar()
    choiceVar.set(1)
    choice1 = tkinter.Radiobutton(mainFrame, text="Road Map View", variable=choiceVar, value=1,command=radioButtonChosen)
    choice1.pack()
    choice2 = tkinter.Radiobutton(mainFrame, text="Satellite Map View", variable=choiceVar, value=2, command=radioButtonChosen)
    choice2.pack()
    choice3 = tkinter.Radiobutton(mainFrame,text="Terrain Map View", variable=choiceVar,value=3,command=radioButtonChosen)
    choice3.pack()
    choice4 = tkinter.Radiobutton(mainFrame,text="Hybrid Map View", variable=choiceVar,value=4,command=radioButtonChosen)
    choice4.pack()

    label = tkinter.Label(mainFrame, text="radio button choice is: {}".format(selectedButtonText))
    label.pack()
    # we use a tkinter Label to display the map image
    Globals.mapLabel = tkinter.Label(mainFrame, width=Globals.mapSize, bd=2, relief=tkinter.FLAT)
    Globals.mapLabel.pack()


def HW9():
    initializeGUIetc()
    displayMap()
    Globals.rootWindow.mainloop()


HW9()
