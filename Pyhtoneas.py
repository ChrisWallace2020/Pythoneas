#Chris Wallace
#Pythoneas

#T I M E   L O G
#04/09/17: 2.0 hr
#04/14/17: 0.5 hr
#04/15/17: 5.0 hr
#04/16/17: 2.0 hr
#04/17/17: 2.5 hr
#04/20/17: 5.0 hr
#04/21/17: 1.0 hr
#04/23/17: 1.0 hr
#04/24/17: 2.0 hr
#04/25/17: 3.0 hr
#04/26/17: 3.0 hr
#04/27/16: 4.0 hr
#04/28/17: 3.0 hr
#04/29/17: 5.0 hr
#04/30/17: 4.0 hr
#05/01/17: 4.0 hr
#05/02/17: 2.0 hr
#05/03/17: 3.0 hr

#TOTAL: 52.0 hr

################################################################################
#BACK END
################################################################################
import math
import random
#Used for Weather Underground API
import urllib.request
import json

#Use for user data and file reading
#File IO code taken from strings section of course wedbapge
#https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
with open("users.txt", "rt") as f:
    userDict = eval(f.read())

#Used for weather underground API
apikey = "4636dc7c5e68a48a"
state = None
city = None
apistuff = (0, 0, 0)
#Code taken from Weather Underground API Code Samples page (python section)
#https://www.wunderground.com/weather/api/d/docs?d=resources/code-samples&MR=1
#With help using Python documentation for urllib.request and json modules
#https://docs.python.org/3/library/urllib.request.html
#https://docs.python.org/2/library/json.html
def useAPIOnce():
    if((city != None) and (state != None)):
        url = 'http://api.wunderground.com/api/%s/' % apikey
        url += 'geolookup/conditions/q/%s/%s.json' % (state, city)
        f = urllib.request.urlopen(url)
        json_string = f.read().decode("utf-8")
        parsed_json = json.loads(json_string)
        location = parsed_json['location']['city']
        temp = float(parsed_json['current_observation']['feelslike_f'])
        wind = float(parsed_json['current_observation']['wind_mph'])
        precip = float(parsed_json['current_observation']['precip_today_metric'])
        rainsnow = None
        if(precip > 0):
            if(temp < 32):
                rainsnow = "snow"
            else:
                rainsnow = "rain"
            apistuff = (temp, wind, rainsnow)
        f.close()

def distance(x1, y1, x2, y2):
    #Find Cartesian Distance
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def testMap():
    #Test Graph for Dijksta's Algorithm
    a = Node(50, 100, "a")
    b = Node(250, 500, "b")
    c = Node(650, 400, "c")
    d = Node(300, 150, "d")
    e = Node(400, 50, "e")
    a.addAdj(b)
    a.addAdj(d)
    a.addAdj(e)
    c.addAdj(b)
    c.addAdj(d)
    c.addAdj(e)
    e.addAdj(d)
    d.addAdj(b)
    tmap = Map()
    tmap.nodes.add(a)
    tmap.nodes.add(a)
    tmap.nodes.add(b)
    tmap.nodes.add(c)
    tmap.nodes.add(d)
    tmap.nodes.add(e)
    print(tmap)
    return tmap

#MAP
class Map(object):
    def __init__(self):
        #Keep track of essential lists/sets for Dijkstra's algorithm
        self.visited = set()
        self.nodes = set()
        self.tree = list()
        self.path = list()
        self.possNodes = set()

    def __str__(self):
        #Effectively print all node and edge data
        stri = ""
        for node in self.nodes:
            for adj in node.adjs:
                stri = stri + "\n%s - %s %f" % (node.name, adj.name, 
                                                node.adjs[adj].weight)
            stri = stri + "\n"
        return stri

    def reset(self):
        #Refresh map (used for returning to home screen)
        self.visited = set()
        self.tree = list()
        self.path = list()
        self.nodes = set()
        print("TRIGGERED")

    def isPossible(self, start, end, node = None):
        #Finds if path is possible
        if(node == None):
            node = start
            self.possNodes.add(start)
        if(node == end):
            return True
        else:
            for node2 in node.adjs: 
                if(node2 not in self.possNodes):
                    self.possNodes.add(node2)
                    solve = self.isPossible(start, end, node2)
                    if(solve == True):
                        return solve
            return False

    def dijkstra(self, start, end, i = 0):
        #Dijkstra's Algorithm for mapping the shortest path
        #Initialize tentative distance of start node
        self.possNodes = set()
        if(not self.isPossible(start, end)): return "error"
        self.visited = set()
        self.tree = list()
        self.path = list()
        for node in self.nodes:
            node.reset()
        start.tentD = 0
        #Print check
        #print("START %s \nEND %s" % (start.name, end.name))
        #print("VISITED")
        self.visited.add(start)
        for node in self.visited:
            #print(node.name)
            pass
        #Run until end not has been visited
        while end not in self.visited:
            #Reset valid nodes
            valid = set()
            for node in self.visited:
                for adj in node.adjs:
                    #Make sure not already visited and adjascent to a visited
                    ch = (node.adjs[adj].weights[i] != math.inf)
                    if((adj not in self.visited) and (adj in node.adjs) and ch):
                        valid.add(adj)
                        if(node.tentD + node.adjs[adj].weights[i] < adj.tentD):
                            #Update tentative distance
                            #print(adj.closestTent)
                            adj.closestTent = node
                            adj.tentD = node.tentD + node.adjs[adj].weights[i]
            #Print Check
            #print("VALID")
            for node in valid:
                #print(node.name + " from " + node.closestTent.name)
                pass
            #Initialize minimum distance and minimum node
            minD = None
            minN = None
            #Find minimums
            for near in valid:
                if(minD == None):
                    minD = near.tentD
                    minN = near
                if(near.tentD < minD):
                    minD = near.tentD
                    minN = near
            #Print check
            #print("PICK %s" % minN.name)
            self.visited.add(minN) #Add closest node to visited
            #Print Check
            #print("VISITED")
            for node in self.visited:
                #print(node.name, end = " ")
                pass
            #print("")
            #Add tuple to represent edge
            self.tree.append((minN.closestTent, minN))
        #Print Check
        count = 0
        #print("TREE")
        for tup in self.tree:
            #print(count, end = " ")
            #print(tup[0].name, tup[1].name)
            count += 1
        #Extract specific path
        return self.findPath(start, end)

    def findPath(self, start, end):
        #Give list of nodes in path
        final = [end] #Initialize with end and move back
        prev = end #Keep track of last node
        #End when both start and end in path
        while start not in final:
            for tup in self.tree:
                #Found node that precedes last node
                if(tup[1] == prev):
                    final.insert(0, tup[0]) #Place in beginning of list
                    prev = tup[0]
        self.path = final
        #Print Check
        #print("PATH")
        for node in self.path:
            #print(node.name, end = " ")
            pass
        #print("")
        return self.path

    def findNode(self, x, y, r):
        #Determine which node was clicked based on cartesian coordinates
        for node in self.nodes:
            if((x <= node.x + r) and (x >= node.x - r) and (y <= node.y + r)
                and (y >= node.y - r)):
                return node

#NODE
class Node(object):
    def __init__(self, x, y, n):
        #Essential node characteristics
        self.x = x
        self.y = y #Cartesian coordinates
        self.name = n
        self.adjs = dict() #Dictionary of adjascent nodes mapping to edges
        self.tentD = math.inf 
        self.closestTent = None #To be implemented in Dijkstra's Algorithm

    def __str__(self):
        #Print Essential info of node
        return "%s (%d,%d)" % (self.name, self.x, self.y)

    def reset(self):
        #Reset values needed for Dijkstra's Algorithm
        self.tentD = math.inf
        self.closestTent = None

    def addAdj(self, other, od, st, prefW, prefS, c, s):
        #Add adjascent node
        d = distance(self.x, self.y, other.x, other.y)
        #Add wieghted edge to both dictioanries
        self.adjs[other] = Edge(self, other, d, od, st, prefW, prefS, c, s)
        other.adjs[self] = Edge(other, self, d, od, st, prefW, prefS, c, s)

    def removeAdj(self, other):
        #Remove an adjascent node from the node's dictionary
        if((other not in self.adjs) or (self not in other.adjs)):
            return 
        del self.adjs[other]
        del other.adjs[self]

#EDGE
class Edge(object):
    def __init__(self,node1,node2,distance,outdoors,stairs,prefW,prefS,c,s):
        #Specify important details about the edge
        self.node1 = node1
        self.node2 = node2
        self.outdoors = outdoors
        self.weatherweight = apistuff
        self.stairs = stairs
        self.weights = [distance]*3
        #Modify weights by data and user preference
        if(self.outdoors):
            (t, w, rs) = self.weatherweight
            weath = abs(50 - t) + w
            if(rs == "rain"):
                weath += 50
            elif(rs == "snow"):
                weath += 100
            self.weights[1] += ((prefW * weath)/self.weights[0])
        if(self.stairs):
            if(prefS == 2):
                #Add longest possible edge (Diagonal of window)
                self.weights[2] = math.inf
            else:
                self.weights[2] += prefS * 50

    def __str__(self):
        #Return a string representing an edge
        return "%s - %s, %f" % (self.node1.name, self.node2.name, 
                                self.weight)

    def getCoords(self):
        #Find coordinates of an edge for drawing purposes
        coords = []
        coords.append(self.node1.x)
        coords.append(self.node1.y)
        coords.append(self.node2.x)
        coords.append(self.node2.y)
        return coords

################################################################################
#FRONT END
################################################################################

#Run function and event based animations framework from course website
from tkinter import *
from tkinter import messagebox, simpledialog

def init(data):
    #Initialize data
    data.marginx = 50
    data.marginy = 50
    data.map = Map()
    #data.map = testMap()
    data.r = 5
    data.start = None
    data.end = None
    data.path = None
    data.circs = []
    data.screen = "home"
    data.mode = ""
    data.nextchar=chr(ord("a")+(len(data.map.nodes))%26)
    data.firstNode = None
    data.secondNode = None
    data.undoN = []
    data.undoE = []
    data.gridSpacing = 40
    data.pathindex = 0
    data.sp = None
    data.wp = None
    data.user = None
    data.password = None
    data.userkey = None
    data.mapStr = ""
    data.fileName = None
    data.fsstr = ""
    data.ssstr = ""
    data.clicked = None
    data.fileSpots1 = list()
    data.fileSpots2 = list()
    data.userList = list()
    data.otherList = list()
    #Image Code taken from Misc Tkinter Demos on course webpage
    #https://www.cs.cmu.edu/~112/notes/imagesDemo1.py
    #Image from https://icons.wxug.com/logos/PNG/wundergroundLogo_4c.png
    data.image = None
    data.wuimage = PhotoImage(file = "wu.gif")
    data.wuimage = data.wuimage.subsample(4, 4)
    data.hlcolors = ["green", "orange", "dodger blue"]
    #Button Code taken from Misc Tkinter Demos on Course Webpage
    #https://www.cs.cmu.edu/~112/notes/button-demo1.py
    #https://www.cs.cmu.edu/~112/notes/button-demo2.py
    buttonFrame = Frame(data.root)
    editB = Button(buttonFrame, text = "EDIT", font = "Times 32",
                   command=lambda:onButton(data,"edit"))
    editB.grid(row=0,column=1)
    browseB = Button(buttonFrame, text = "BROWSE", font = "Times 32",
                     command=lambda:onButton(data,"browse"))
    browseB.grid(row=0,column=0)
    homeB = Button(data.root, text = "HOME", font = "Times 32",
                   command=lambda:onButton(data,"home"))
    homeB.pack()
    buttonFrame.pack(side=BOTTOM)

def choose(message, title, options):
    #Taken from Misc Tkinter Demos on course webpage
    #https://www.cs.cmu.edu/~112/notes/dialogs-demo1.py
    msg = message + "\n" + "Choose one:"
    for i in range(len(options)):
        msg += "\n" + str(i+1) + ": " + options[i]
    response = simpledialog.askstring(title, msg)
    return int(response)

def onButton(data, buttonId):
    #Button clicked, as taken from course website
    #https://www.cs.cmu.edu/~112/notes/button-demo1.py
    #https://www.cs.cmu.edu/~112/notes/button-demo2.py
    if(buttonId == "edit"): 
        data.screen = "edit"
        #Taken from Misc Tkinter Demos on Course webpage
        #https://www.cs.cmu.edu/~112/notes/dialogs-demo1.py
        msgC = "Enter City:"
        msgSt = "Enter State (abbreviated):"
        titleC = "CITY"
        titleSt = "STATE"
        city = simpledialog.askstring(titleC, msgC)
        city = city.replace(" ", "_")
        state = simpledialog.askstring(titleSt, msgSt)
        data.mapStr += "city = !%s!\nstate = !%s!" % (city, state)
        useAPIOnce()
        msgW = "How much do you want to walk outdoors?"
        msgS = "Are stairs an issue?"
        titleW = "WEATHER"
        titleS = "ACCESSIBILITY"
        optionsW = ["I'd like to walk outside", "It doesn't matter"]
        optionsW.append("I'd like to walk inside")
        optionsS = ["I don't mind stairs","I'd rather not traverse stairs"]
        optionsS.append("Avoid stairs")
        responseW = choose(msgW, titleW, optionsW)
        responseS = choose(msgS, titleS, optionsS)
        data.wp = responseW - 2
        data.sp = responseS - 1
        msgPic = "Enter the name of your picture (include .gif)"
        msgPic += "\n(type \'grid\' if you simply want a grid and no picture)"
        titlePic = "TITLE"
        #Do not ask if editing saved map with pic
        if(data.image == None):
            data.image = simpledialog.askstring(titlePic, msgPic)
            if(data.image != "grid"):
                #Image Code taken from Misc Tkinter Demos on course webpage
                #https://www.cs.cmu.edu/~112/notes/imagesDemo1.py
                data.mapStr += "\ndata.image=PhotoImage(file = !%s!)"%data.image
                data.image = PhotoImage(file = data.image)
    elif(buttonId == "browse"): 
        data.screen = "browse"
    elif(buttonId == "home"):
        data.screen = "home"
        data.image = None
        data.map = Map()
        data.path = None
        data.circs = []

def save(data):
    #Save map to txt file
    #Dialog code taken from Misc Tkinter Demos on Course webpage
    #https://www.cs.cmu.edu/~112/notes/dialogs-demo1.py
    titleFile = "SAVE"
    msgFile = "What would you like to save this map as (include .txt)"
    data.fileName = simpledialog.askstring(titleFile, msgFile)
    data.fileName = data.user + "_" + data.fileName
    #File IO Code taken from string notes in course Webpage
    #https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
    with open(data.fileName, "wt") as f:
        f.write(data.mapStr)
    userDict[data.userkey].add(data.fileName)
    with open("users.txt", "wt") as f:
        f.write(repr(userDict))

def mousePressed(event, data):
    #Manipulate the map depending on the mode
    if(data.screen == "edit"):
        #Save button clicked
        if((data.width - 80 < event.x) and (event.x < data.width) and 
           (data.height - 40 < event.y) and (event.y < data.height)):
            save(data)
        if((0<event.x) and (event.x<160) and (40<event.y) and (event.y<160)):
            data.pathindex = (event.y//data.gridSpacing) - 1
            if((data.start != None) and (data.end != None)):
                data.path = data.map.dijkstra(data.start, data.end, 
                                              data.pathindex)
        if(data.mode == "node"):
            #Add a node
            data.map.nodes.add(Node(event.x, event.y, data.nextchar))
            data.mapStr+="\ndata.map.nodes.add(Node(%d, %d" % (event.x, event.y)
            data.mapStr += ", !%s!))" % data.nextchar
            data.nextchar = chr(ord("a")+(len(data.map.nodes)%26))
        elif(data.mode == "edge"):
            #Connect 2 selected nodes with an edge
            if(data.firstNode == None): #Only recognize if node is clicked
                if(data.map.findNode(event.x, event.y, data.r) != None):
                    data.firstNode = data.map.findNode(event.x, event.y, data.r)
                    data.fsstr = "data.map.findNode(%d,%d" % (event.x,event.y)
                    data.fsstr += ", %d)" % data.r
            elif(data.secondNode == None):
                if((data.map.findNode(event.x, event.y, data.r) != None) and
                    data.map.findNode(event.x,event.y,data.r)!=data.firstNode):
                    data.secondNode = data.map.findNode(event.x, event.y,data.r)
                    data.ssstr = "data.map.findNode(%d, %d" % (event.x,event.y)
                    data.ssstr += ", %d)" % data.r
                    #Message box code taken from Misc Tkinter Demos, course site
                    #https://www.cs.cmu.edu/~112/notes/dialogs-demo1.py
                    titleOD = "OUTDOORS"
                    msgOD = "Is this path outdoors?"
                    od = messagebox.askquestion(titleOD, msgOD)
                    if(od == "yes"):
                        od = True
                    elif(od == "no"):
                        od = False
                    titleST = "STAIRS"
                    msgST = "Does this path have stairs?"
                    st = messagebox.askquestion(titleST, msgST)
                    if(st == "yes"):
                        st = True
                    elif(st == "no"):
                        st = False
                        #Add adjs and crete edge
                    data.firstNode.addAdj(data.secondNode, od, st, data.wp,
                                          data.sp, city, state)
                    data.mapStr += "\n%s.addAdj(%s, " % (data.fsstr, data.ssstr)
                    data.mapStr += "%s, %s, " % (str(od), str(st))
                    data.mapStr += "data.wp, data.sp, city, state)"
                    #Reset
                    data.firstNode = None
                    data.secondNode = None   
        else:
            for node in data.map.nodes:
                #Find Clicked node
                if((event.x <= node.x+data.r)and(event.x >= node.x-data.r)and 
                   (event.y <= node.y+data.r)and(event.y >= node.y-data.r)):
                    if(node == data.start):
                        data.start = None
                        data.circs = []
                        data.path = None
                        return
                    if(data.start == None):
                        #Set start node for dijkstra
                        data.start = node
                        data.circs.append((node.x, node.y))
                    elif(data.end == None):
                        #Set end node for dijkstra
                        data.end = node
                        data.path = data.map.dijkstra(data.start, data.end, 
                                                      data.pathindex)
                        data.circs.append((node.x, node.y))
                        if(data.path == "error"):
                            #Path not possible, notiy user and reset data.end
                            data.end = None 
                            data.circs.pop()
                            data.path = None
                            #Warning box from Misc Tkinter Demos, course webpage
                            #https://www.cs.cmu.edu/~112/notes/dialogs-demo1.py
                            msg = "The node you are trying to reach is not"
                            msg += " connected to the node previously selected"
                            messagebox.showwarning("ERROR: INVALID PATH", msg)
                            return
                    else:
                        #Reset with new start
                        data.start = node
                        data.end = None
                        data.path = []
                        data.circs = [(node.x, node.y)]
    elif(data.screen == "browse"):
        findClick(data, event.x, event.y)

def findClick(data, x, y):
    #Determines which file was clicked
    #File IO code taken from course webpage for strings notes
    #https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
    for i in range(len(data.fileSpots1)):
        (x1, y1, x2, y2) = data.fileSpots1[i]
        if((x1 < x) and (x < x2) and (y1 < y) and (y < y2)):
            found = data.userList[i]
            if(found == data.clicked):
                #Second Click
                with open(data.clicked, "rt") as f:
                    #Update data.mapStr
                    data.mapStr = f.read()
                    data.map = Map()
                    data.path = None
                    data.image = None
                    #Get user preferences again
                    #Taken from Misc Tkinter Demos on Course webpage
                    #https://www.cs.cmu.edu/~112/notes/dialogs-demo1.py
                    msgW = "How much do you want to walk outdoors?"
                    msgS = "Are stairs an issue?"
                    titleW = "WEATHER"
                    titleS = "ACCESSIBILITY"
                    optionsW = ["I'd like to walk outside", "It doesn't matter"]
                    optionsW.append("I'd like to walk inside")
                    optionsS = ["I don't mind stairs"]
                    optionsS.append("I'd rather not traverse stairs")
                    optionsS.append("Avoid stairs")
                    responseW = choose(msgW, titleW, optionsW)
                    responseS = choose(msgS, titleS, optionsS)
                    data.wp = responseW - 2
                    data.sp = responseS - 1
                    exec(data.mapStr.replace("!", "\'"))
                    data.nextchar=chr(ord("a")+(len(data.map.nodes)%26))
                    data.screen = "edit"
                    useAPIOnce()
            else:
                #First Click
                data.clicked = found
                return
    for i in range(len(data.fileSpots2)):
        (x1, y1, x2, y2) = data.fileSpots2[i]
        if((x1 < x) and (x < x2) and (y1 < y) and (y < y2)):
            found = data.otherList[i]
            if(found == data.clicked):
                #Second Click
                with open(data.clicked, "rt") as f:
                    #Update data.mapStr
                    data.mapStr = f.read()
                    data.map = Map()
                    data.path = None
                    data.image = None
                    #Taken from Misc Tkinter Demos on Course webpage
                    #https://www.cs.cmu.edu/~112/notes/dialogs-demo1.py
                    #Get user preferences again
                    msgW = "How much do you want to walk outdoors?"
                    msgS = "Are stairs an issue?"
                    titleW = "WEATHER"
                    titleS = "ACCESSIBILITY"
                    optionsW = ["I'd like to walk outside", "It doesn't matter"]
                    optionsW.append("I'd like to walk inside")
                    optionsS = ["I don't mind stairs"]
                    optionsS.append("I'd rather not traverse stairs")
                    optionsS.append("Avoid stairs")
                    responseW = choose(msgW, titleW, optionsW)
                    responseS = choose(msgS, titleS, optionsS)
                    data.wp = responseW - 2
                    data.sp = responseS - 1
                    exec(data.mapStr.replace("!", "\'"))
                    data.nextchar=chr(ord("a")+(len(data.map.nodes)%26))
                    data.screen = "edit"
                    useAPIOnce()
                    
            else:
                #First Click
                data.clicked = found
                return
    #Nothing was clicked
    data.clicked = None

def keyPressed(event, data):
    #Change mode depending on key press
    if(data.screen == "edit"):
        if((data.mode == "node") and (event.char == "n")):
            #Unselect mode
            data.mode = ""
            return
        if((data.mode == "edge") and (event.char == "e")):
            #Unelect mode
            data.mode = ""
            return
        #Change mode
        if(event.char == "n"):
            data.mode = "node"
        elif(event.char == "e"):
            data.mode = "edge"
        if(data.mode == "node"):
            #Undo/redo for nodes
            if(event.char == "u"):
                data.undoN.append(data.map.nodes.pop())
            if((event.char == "r") and (data.undoN != [])):
                data.map.nodes.add(data.undoN.pop())
        #Change weighting preference and calculate new path
        if(event.keysym == "Left"):
            data.pathindex = (data.pathindex - 1) % 3
            if((data.path != None) and (data.start != None) and 
                (data.end != None)):
                data.path = data.map.dijkstra(data.start, data.end, 
                                              data.pathindex)
        if(event.keysym == "Right"):
            data.pathindex = (data.pathindex + 1) % 3
            if((data.path != None) and (data.start != None) and 
                (data.end != None)):
                data.path = data.map.dijkstra(data.start, data.end, 
                                              data.pathindex)

def timerFired(data, canvas):
    #Redraw new random home background
    if(data.screen == "home" or data.screen == "browse"):
        drawBackground(data, canvas)

def drawBackground(data, canvas):
    #Draws opaque gray background on home screen
    for i in range(50):
        x1 = random.randint(-5 * data.width, 0)
        x2 = random.randint(0, 5 * data.width)
        y1 = random.randint(-5 * data.height, 0)
        y2 = random.randint(0, 5 * data.height)
        canvas.create_line(x1, y1, x2, y2, fill = "lavender", width = 5)

def redrawAll(canvas, data):
    #Draw front end
    if(data.screen == "home"):
        #Print title and directions
        drawBackground(data, canvas)
        canvas.create_text(data.width//2, data.height//2-100, text="PYTHONEAS",
                           font = "Times 96")
        directions1 = "Create custom maps or edit existing ones"
        directions2 = "with shortest mapping capabilities via Dijkstra's"
        directions2 += " Algorithm."
        directions3 = "Go deeper than distance with custom weighting options"
        directions4 = "such as weather and accessibility to find multiple "
        directions4 += "viable paths."
        directsb="Click \'Browse\' to open maps created by you and other users."
        directse = "Click \'Edit\' to start a new map from scratch."
        canvas.create_text(data.width//2, data.height//2 + 30, text=directions1,
                           font = "Times 20")
        canvas.create_text(data.width//2, data.height//2 + 50, text=directions2,
                           font = "Times 20")
        canvas.create_text(data.width//2, data.height//2 + 70, text=directions3,
                           font = "Times 20")
        canvas.create_text(data.width//2, data.height//2 + 90, text=directions4,
                           font = "Times 20")
        canvas.create_text(data.width//2, data.height//2 + 110, text=directsb,
                           font = "Times 20")
        canvas.create_text(data.width//2, data.height//2 + 130, text=directse,
                           font = "Times 20")
        #Sign in
        if(data.user == None):
            titleUse = "USER"
            msgUse = "Enter your username:"
            data.user = simpledialog.askstring(titleUse, msgUse)
            titlePass = "PASSWORD"
            msgPass = "Enter your password:"
            data.password = simpledialog.askstring(titlePass, msgPass)
            data.userkey = data.user + data.password
            if(data.userkey not in userDict):
                userDict[data.userkey] = set()
                #File IO code taken from strings section of course wedbapge
            #https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
                with open("users.txt", "wt") as f:
                    f.write(repr(userDict))

    elif(data.screen == "edit"):
        #Draw grid/pic
        drawGrid(canvas, data)
        if(data.image != "grid"):
            canvas.create_image(data.width//2, data.height//2, image=data.image)
        #Draw elements
        drawCircs(canvas, data)
        drawEdges(canvas, data, data.pathindex)
        drawNodes(canvas, data)
        if(data.path != None):
            drawPath(canvas, data)
        #Print directions
        directions5 = "N - Node Mode"
        directions5 += "\nE - Edge Mode"
        canvas.create_text(5, 5, text = directions5, anchor = NW, 
                           font = "Times 16")
        if(data.mode == "node"):
            nodedir = "Click where you wish to add a node"
            nodedir2 = "\nPress N to exit Node Mode"
            canvas.create_text(data.width-40, 20, text="NODE", font="Times 18")
            canvas.create_text(data.width, 60, text = nodedir,
                               anchor = SE, font = "Times 16")
            canvas.create_text(data.width, 80, text = nodedir2,
                               anchor = SE, font = "Times 16")
        elif(data.mode == "edge"):
            edgedir = "Click 2 nodes you wish to connect with an edge"
            edgedir2 = "\nPress E to exit Edge Mode"
            canvas.create_text(data.width-40, 20, text="EDGE", font="Times 18")
            canvas.create_text(data.width, 60, text = edgedir,
                               anchor = SE, font = "Times 16")
            canvas.create_text(data.width, 80, text = edgedir2,
                               anchor = SE, font = "Times 16")
        else:
            dijkdir = "Click a start node and an end node"
            dijkdir2 = "\nClick the node again to undo your selection"
            canvas.create_text(data.width, 60, text = dijkdir,
                               anchor = SE, font = "Times 16")
            canvas.create_text(data.width, 80, text = dijkdir2,
                               anchor = SE, font = "Times 16")
            options = ["DISTANCE", "WEATHER", "ACCESSIBILITY"]
            canvas.create_text(data.width - 60, 20,
                               text = options[data.pathindex], font ="Times 16")
            canvas.create_line(data.width - 198, 20, data.width - 122, 20, 
                               fill = data.hlcolors[data.pathindex], width = 5)
        #Print Buttons
        canvas.create_rectangle(data.width-80, data.height-40, data.width, 
                                data.height, fill = "Black")
        canvas.create_text(data.width - 40, data.height - 20, text = "SAVE",
                           font = "Times 16", fill = "White")
        rectBounds = [(2, 42, 158, 78), (1, 82, 158, 118), (2, 122, 158, 158)]
        canvas.create_rectangle(rectBounds[data.pathindex], 
                                fill = data.hlcolors[data.pathindex])
        canvas.create_rectangle(5, 45, 155, 75, fill = "black")
        canvas.create_rectangle(5, 85, 155, 115, fill = "black")
        canvas.create_rectangle(5, 125, 155, 155, fill = "black")
        butcs = ["white"]*3
        #Highlight clicked preference
        butcs[data.pathindex] = data.hlcolors[data.pathindex]
        canvas.create_text(80,60,text="DISTANCE",font="Times 14",fill=butcs[0])
        canvas.create_text(80,100,text="WEATHER",font="Times 14",fill=butcs[1])
        canvas.create_text(80,140,text="ACCESSIBILITY",font="Times 14",
                           fill=butcs[2])
    elif(data.screen == "browse"):
        drawBackground(data, canvas)
        #Print files
        colSpot = data.width//4
        canvas.create_text(colSpot,20,text="YOUR MAPS",font="Times 30")
        canvas.create_text(3*colSpot,20,text="OTHER MAPS",font="Times 30")
        spacing1 = 75
        #Find margins for clicking purposes
        xm = 125
        ym = 20
        data.userList = list(userDict[data.userkey])
        for file in userDict[data.userkey]:
            #Highlight after one click
            if(file == data.clicked):
                colr = "blue"
            else:
                colr = "black"
            canvas.create_text(colSpot,spacing1,text=file,font="Times 20",
                               fill = colr)
            tup = (colSpot-xm,spacing1-ym,colSpot+xm,spacing1+ym)
            if(tup not in data.fileSpots1):
                data.fileSpots1.append(tup)
            spacing1 += 25
        spacing2 = 75
        t = 3*colSpot
        for user in userDict:
            if(user != data.userkey):
                for file in userDict[user]:
                    #Highlight after one click
                    if(file not in data.otherList):
                        data.otherList.append(file)
                    if(file == data.clicked):
                        colr = "blue"
                    else:
                        colr = "black"
                    canvas.create_text(t,spacing2,text=file,font="Times 20",
                                       fill = colr)
                    tup = (t-xm,spacing2-ym,t+xm,spacing2+ym)
                    if(tup not in data.fileSpots2):
                        data.fileSpots2.append(tup)
                    spacing2 += 25
        browseDirections = "Double Click to open a file"
        canvas.create_text(data.width, data.height, text = browseDirections,
                           font = "Times 16", anchor = SE)
    #Display Weather Underground Logo as per their requirements
    #Code taken from Misc Tkinter Demos from course webpage
    #https://www.cs.cmu.edu/~112/notes/imagesDemo1.py
    canvas.create_image(0, data.height, anchor = SW, image = data.wuimage)

def drawGrid(canvas, data):
    #Draw Background grid for edit screen
    for i in range(data.gridSpacing, data.width, data.gridSpacing):
        canvas.create_line(i, 0, i, data.height, fill = "light sky blue")
    for j in range(data.gridSpacing, data.height, data.gridSpacing):
        canvas.create_line(0, j, data.width, j, fill = "light sky blue")

def drawCircs(canvas, data):
    #Show start and end node
    rad = data.r + 5
    for circ in data.circs:
        canvas.create_oval(circ[0] - rad, circ [1] - rad, circ[0] + rad,
                           circ[1] + rad, fill = "seashell4")
    
def drawNodes(canvas, data, col = "black", txt = "white"):
    #Draw all nodes with labels
    for node in data.map.nodes:
        canvas.create_oval(node.x - data.r, node.y - data.r, node.x + data.r, 
                           node.y + data.r, fill = col)
        #canvas.create_text(node.x, node.y, text = str(node.name), 
                           #font = "Times 16", fill = txt)

def drawEdges(canvas, data, i = 0, txt = "grey"):
    #Draw all edges with labels
    for node in data.map.nodes:
        for adj in node.adjs:
            [x1, y1, x2, y2] = node.adjs[adj].getCoords()
            if((data.pathindex == 2) and (node.adjs[adj].weights[2]==math.inf)):
                #Make red if stairs and wished to be avoided
                canvas.create_line(x1, y1, x2, y2, fill = "red")
            else:
                canvas.create_line(x1, y1, x2, y2, fill = "black")
            (x, y) = ((x1+x2)/2, (y1+y2)/2)
            if(node.adjs[adj].weights[data.pathindex] == math.inf):
                t = "inf"
            else:
                t = str(int(node.adjs[adj].weights[data.pathindex]))
            canvas.create_text(x, y, text = t, fill = txt, font = "Times 10")

def drawPath(canvas, data):
    #Draw the path
    drawPathEdges(canvas, data, data.pathindex)
    drawPathNodes(canvas, data)

def drawPathEdges(canvas, data, ind = 0):
    #Highlight edges in path
    for i in range(0, len(data.path) - 1):
        node1 = data.path[i]
        node2 = data.path[i+1]
        [x1, y1, x2, y2] = [node1.x, node1.y, node2.x, node2.y]
        #Use different colors for highlight
        canvas.create_line(x1, y1, x2, y2, fill = data.hlcolors[data.pathindex],
                           width = 10)
        (x, y) = ((x1+x2)/2, (y1+y2)/2)
        if(node1.adjs[node2].weights[data.pathindex] == math.inf):
            t = "inf"
        else:
            t = str(int(node1.adjs[node2].weights[data.pathindex]))
        canvas.create_rectangle(x - 10, y - 5, x + 10, y + 5, fill = "black")
        canvas.create_text(x, y,text = t, fill = data.hlcolors[data.pathindex],
                           font = "Times 10")

def drawPathNodes(canvas, data):
    #Highlight nodes in path
    for node in data.path:
        #Use different colors for highlight
        canvas.create_oval(node.x - data.r, node.y - data.r, node.x + data.r, 
                           node.y + data.r, fill=data.hlcolors[data.pathindex])
        #canvas.create_text(node.x, node.y, text = str(node.name), 
                           #font = "Times 16", fill = "black")

def run(width=300, height=300):
    #Taken from course webpage
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data, canvas)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 3000 # milliseconds

    # create the root and the canvas (Note Change: do this BEFORE calling init!)
    root = Tk()

    #For buttons to access root
    data.root = root

    init(data)
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed

    print("bye!")
run(1000, 600)