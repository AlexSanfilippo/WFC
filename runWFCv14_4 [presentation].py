###Goal: to run MyWFCRun13 with panda3D
#adding support and testing tile weight system

import MyWFCRun14_1 as wfc

from panda3d.core import loadPrcFileData

configVars = """
win-size 1280 720
window-title My WFC App
show-frame-rate-meter 1
show-scene-graph-analyzer-meter 1
"""

loadPrcFileData("", configVars)

from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import PointLight, AmbientLight, NodePath
from math import sin, cos, floor, radians
from direct.filter.CommonFilters import CommonFilters


import random as r

import wfcmath as wfcm

import sys

from panda3d.core import WindowProperties #needed to hide mouse


###Master Control Variables
seed = r.randint(0,1000000)
masterRadius = 4
masterFlatMode = 0

#seed = 6
#seed = 163677
#seed = 535755 #produced placement error and backtrack loop. now 9 backtracks
#seed = 51

#Tileset for testing  multiple connections
ns_s = wfc.Tile(({1},{0},{1},{0},{0},{0}), '|', 'models/MyModels/wfc/straightColor',(0,0,0), 100)
ew_s = wfc.Tile(({0},{1},{0},{1},{0},{0}), '-', 'models/MyModels/wfc/straightColor',(90,0,0), 100)
nsew_i4 = wfc.Tile(({1},{1},{1},{1},{0},{0}), '+', 'models/MyModels/wfc/crossColor', (0,0,0), 100)
blank = wfc.Tile(({0,23},{0,24},{0,21},{0,22},{0},{0}), 'blank', 'models/MyModels/wfc/blank2', (0,0,0), 100)
blank_rare = wfc.Tile(({0,23},{0,24},{0,21},{0,22},{0},{0}), 'blank', 'models/MyModels/wfc/blank2', (0,0,0), 2000)
loneHouse = wfc.Tile(({21},{22},{23},{24},{0},{0}), 'house', 'H')




ab_s = wfc.Tile(({0},{0},{0},{0},{1},{1}),'.', 'models/MyModels/wfc/straightColor',(0,90,0), 100)

nw_i2 = wfc.Tile(({1},{0},{0},{1},{0},{0}), 'b1', 'models/MyModels/wfc/i2Color', (0,0,-90), 100)
ne_i2 = wfc.Tile(({1},{1},{0},{0},{0},{0}), 'b2', 'models/MyModels/wfc/i2Color', (0,0,90), 100)
es_i2 = wfc.Tile(({0},{1},{1},{0},{0},{0}), 'b3', 'models/MyModels/wfc/i2Color',(0,180,90), 100)
sw_i2 = wfc.Tile(({0},{0},{1},{1},{0},{0}), 'b4', 'models/MyModels/wfc/i2Color', (0,180,-90), 100)

nab_i3 = wfc.Tile(({1},{0},{0},{0},{1},{1}),'c1', 'models/MyModels/wfc/i3Color_T',(0,0,0), 100)
eab_i3 = wfc.Tile(({0},{1},{0},{0},{1},{1}),'c2', 'models/MyModels/wfc/i3Color_T', (90,0,0), 100)
sab_i3 = wfc.Tile(({0},{0},{1},{0},{1},{1}),'c3', 'models/MyModels/wfc/i3Color_T',(180,0,0), 100)
wab_i3 = wfc.Tile(({0},{0},{0},{1},{1},{1}),'c4', 'models/MyModels/wfc/i3Color_T',(-90,0,0), 100)

neab_i4 = wfc.Tile(({1},{1},{0},{0},{1},{1}),'d1', 'models/MyModels/wfc/i4Color', (0,0,180), 100)
esab_i4 = wfc.Tile(({0},{1},{1},{0},{1},{1}),'d2', 'models/MyModels/wfc/i4Color',(180,0,0), 100)
swab_i4 = wfc.Tile(({0},{0},{1},{1},{1},{1}),'d3', 'models/MyModels/wfc/i4Color',(0,180,0), 100)
nwab_i4 = wfc.Tile(({1},{0},{0},{1},{1},{1}),'d4', 'models/MyModels/wfc/i4Color',(0,0,0), 100)

nab_i3r = wfc.Tile(({1},{0},{0},{0},{1},{1}),'c1', 'models/MyModels/wfc/i3Color_T',(0,0,0), 5)
eab_i3r = wfc.Tile(({0},{1},{0},{0},{1},{1}),'c2', 'models/MyModels/wfc/i3Color_T', (90,0,0), 5)
sab_i3r = wfc.Tile(({0},{0},{1},{0},{1},{1}),'c3', 'models/MyModels/wfc/i3Color_T',(180,0,0), 5)
wab_i3r = wfc.Tile(({0},{0},{0},{1},{1},{1}),'c4', 'models/MyModels/wfc/i3Color_T',(-90,0,0), 5)

neab_i4r = wfc.Tile(({1},{1},{0},{0},{1},{1}),'d1', 'models/MyModels/wfc/i4Color', (0,0,180), 5)
esab_i4r = wfc.Tile(({0},{1},{1},{0},{1},{1}),'d2', 'models/MyModels/wfc/i4Color',(180,0,0), 5)
swab_i4r = wfc.Tile(({0},{0},{1},{1},{1},{1}),'d3', 'models/MyModels/wfc/i4Color',(0,180,0), 5)
nwab_i4r = wfc.Tile(({1},{0},{0},{1},{1},{1}),'d4', 'models/MyModels/wfc/i4Color',(0,0,0), 5)

neswab_i6r = wfc.Tile(({1},{1},{1},{1},{1},{1}),'*','models/MyModels/wfc/sixWayColor',(0,0,0), 1)
#5 way intersections could go here
neswab_i6 = wfc.Tile(({1},{1},{1},{1},{1},{1}),'*','models/MyModels/wfc/sixWayColor',(0,0,0), 100)

#Vertical "caps" or "roofs"

nsb_i3 = wfc.Tile(({1},{0},{1},{0},{0},{1}),'c1', 'models/MyModels/wfc/i3Color_T',(0,90,0), 100)
ewb_i3 = wfc.Tile(({0},{1},{0},{1},{0},{1}),'c2', 'models/MyModels/wfc/i3Color_T', (90,90,0), 100)
sab_i3 = wfc.Tile(({0},{0},{1},{0},{1},{1}),'c3', 'models/MyModels/wfc/i3Color_T',(180,0,0), 100)
wab_i3 = wfc.Tile(({0},{0},{0},{1},{1},{1}),'c4', 'models/MyModels/wfc/i3Color_T',(-90,0,0), 100)


#weighted tile
#ns_s_red = ns_s = wfc.Tile(({1},{0},{1},{0},{0},{0}), '|', 'models/MyModels/wfc/straightPipe2Red',(0,0,0), 100) 


#Working Tilesets
improved3D = [ns_s, ew_s, nsew_i4, blank, nw_i2, ne_i2, es_i2, sw_i2, neswab_i6, ab_s, nab_i3, eab_i3, sab_i3, wab_i3, neab_i4, esab_i4, swab_i4, nwab_i4] #This tileset produces no errors on nxnxn, a perfect set
myTileList10 = [ns_s, ew_s, nsew_i4, blank, loneHouse]
simpleList = [ns_s, ew_s, nsew_i4, blank] #not compatable with 3d infinite generation.  results in misplaced tiles eventually
improved3D_scarce = [ns_s, ew_s, nsew_i4, blank_rare, nw_i2, ne_i2, es_i2, sw_i2, neswab_i6, ab_s, nab_i3, eab_i3, sab_i3, wab_i3, neab_i4, esab_i4, swab_i4, nwab_i4]
improved3D_lessVertical = [ns_s, ew_s, nsew_i4, blank, nw_i2, ne_i2, es_i2, sw_i2, neswab_i6r, ab_s, nab_i3r, eab_i3r, sab_i3r, wab_i3r, neab_i4r, esab_i4r, swab_i4r, nwab_i4r]
caps = [ns_s, ew_s, nsew_i4, blank, nw_i2, ne_i2, es_i2, sw_i2, neswab_i6, ab_s, nab_i3, eab_i3, sab_i3, wab_i3, neab_i4, esab_i4, swab_i4, nwab_i4, nsb_i3, ewb_i3]


#biomeList = [improved3D, improved3D_scarce]
biomeList = [caps]
#biomeList = [improved3D_lessVertical, simpleList] #for 2d maps ONLY

surf = wfc.Surface(radius = masterRadius, tileList = biomeList[0], seed = seed, playerPos = (0,0,0), oldSurf = 0, flatMode = masterFlatMode)  #1000 tiles in 4.43 seconds

start = surf.initialize()

surf.randTile(start)

surf.collapse()   

#newSurf = wfc.Surface(radius = 3, tileList = improved3D,seed = seed, playerPos = (1,0,0), oldSurf = surf) #basics of new map based on movement
#newSurf.collapse()
#surf = newSurf

#Below is user input stuff

#global dictionary to store keys and thier values
keyMap = {
        'up': False,
        'down': False,
        'left': False,
        'right': False,
        'turn_left':False,
        'turn_right':False,
        'vertical_up':False,
        'vertical_down':False
        
            }
  #callback fxn to update the keyMap
def updateKeyMap(key, state):
    keyMap[key] = state




###Below handles the panda3d scene, placing models in the correction positions for the corresponding tiles



class WFC(ShowBase):
    def __init__(self,surf):
        super().__init__()



        self.tiles = NodePath("tiles")
        self.tiles.reparentTo(self.render)

        
        
        self.jack = self.loader.loadModel("models/jack")
        self.jack.setHpr(0,180,180)
        self.jack.setPos(0,0,0)
        self.jack.reparentTo(self.render)
        
        self.accept("arrow_left", updateKeyMap, ["left", True]) #updates keymap dictionary
        self.accept("arrow_left-up", updateKeyMap, ["left",False])

        self.accept("arrow_right", updateKeyMap, ["right", True]) #updates keymap dictionary
        self.accept("arrow_right-up", updateKeyMap, ["right",False])

        self.accept("arrow_up", updateKeyMap, ["up", True]) #updates keymap dictionary
        self.accept("arrow_up-up", updateKeyMap, ["up",False])

        self.accept("arrow_down", updateKeyMap, ["down", True]) #updates keymap dictionary
        self.accept("arrow_down-up", updateKeyMap, ["down",False])

        #allows wasd instead of arrow keys
        self.accept("a", updateKeyMap, ["left", True]) #updates keymap dictionary
        self.accept("a-up", updateKeyMap, ["left",False])

        self.accept("d", updateKeyMap, ["right", True]) #updates keymap dictionary
        self.accept("d-up", updateKeyMap, ["right",False])

        self.accept("w", updateKeyMap, ["up", True]) #updates keymap dictionary
        self.accept("w-up", updateKeyMap, ["up",False])

        self.accept("s", updateKeyMap, ["down", True]) #updates keymap dictionary
        self.accept("s-up", updateKeyMap, ["down",False])
        

        #self.accept("arrow_down", updateKeyMap, ["turn_left", True]) #updates keymap dictionary     #TP
        #self.accept("arrow_down-up", updateKeyMap, ["turn_left",False])

        self.accept("q", updateKeyMap, ["turn_left", True]) #updates keymap dictionary
        self.accept("q-up", updateKeyMap, ["turn_left",False])

        self.accept("e", updateKeyMap, ["turn_right", True]) #updates keymap dictionary
        self.accept("e-up", updateKeyMap, ["turn_right",False])

        self.accept("space", updateKeyMap, ["vertical_up", True]) #updates keymap dictionary
        self.accept("space-up", updateKeyMap, ["vertical_up",False])

        self.accept("v", updateKeyMap, ["vertical_down", True]) #updates keymap dictionary
        self.accept("v-up", updateKeyMap, ["vertical_down",False])

        
        self.speed = 1
        
        self.scale = .5


        

        
        #old camera, gave nice top-down view. replaced with movable first-person view
        #self.cam.setPos(2,2,65)
        #self.cam.setHpr(0,-90,0) #roll turns head to side
        
        self.cam.setPos(0,0, 30)
        self.cam.setScale(.01) #needed?
        ###loop through surf.slot, make objects at correct locations
        


        #creates the point light
        plight = PointLight("plight")
        plight.setShadowCaster(True,1024,1024) #creates shadows
        self.render.setShaderAuto()
        plight.setColor((1,1,1,1)) # a tuple, white light
        #self.plnp = self.light_model.attachNewNode(plight)
        
        #self.plnp.setPos(2,0,9)
        #plight.setAttenuation((0,1,0)) #light drop off

        #creates ambient light (how dark the shaded parts should be
        alight = AmbientLight('alight')
        alight.setColor((0.04, 0.04, 0.04, 1))
        self.alnp = self.render.attachNewNode(alight)
        

        ####Attach light to camera
        self.plnp = self.cam.attachNewNode(plight)
        self.cam.setLight(self.plnp)#adds point light to the trees



        '''This for loop replaces the below for loop, better implementation'''
        #mi = 0 #index of model
        self.modelDict = {} #model is now a dictionary.
        #how to add items one by one?
        #model[key] = val
        for coord in surf.slot: #for each coordinate in the slot matrix
            #get slot's tile: surf.slot[coord][0]
            #get tile's model
            
            #these two lines make reading easier
            model = surf.slot[coord][0].model #assign model the coordinates and tile model #wait, why not just use surf then? save a step?
            rotation = surf.slot[coord][0].rotation #add this to Tile Class
            
            #load the model
            self.modelDict[coord] = self.loader.loadModel(model)
            self.modelDict[coord].setPos(coord) #place model at coordinates
            self.modelDict[coord].setHpr(rotation) #rotate model
            self.modelDict[coord].setScale(self.scale) #set model scale

            

            self.tiles.setLight(self.plnp)#adds point light to the trees
            
            self.modelDict[coord].reparentTo(self.tiles) #without this, model won't be rendered.
            #place model at slot's coords


        ###printing by text for troubleshooting
        '''
        for k in range(surf.z):
            for j in range(surf.y):
                #for i in x:
                for i in range(surf.x):
                    
                    print(str(surf.slot[i,j,k][0].name) + " ", end = '')#print row
                print("")#for newline
            print("")
        '''
   
            
          
        
        self.anchorPos = (0,0,0)

        self.prevSurf = surf
        
              
        self.taskMgr.add(self.play, "play")
        self.turnSpeed =128
        
        self.origin = (0,0,0) #for determining biome change


        #player controller stuff
        self.heading = 0
        self.pitch = 0

        

        self.sensitivity = 30

        #hide the mouse cursor
        props = WindowProperties()
        props.setCursorHidden(True)
        self.win.requestProperties(props)


        ##QUEUES
        self.removeQ = []
        self.addQ = []
        self.newSurf = []
        self.collapseStatus = 1
        

    def angularMovement(self): #update the meaning of move "forward" to be based on camera heading.
        rotation = self.cam.getHpr()
        n = rotation[0] % 360
        heading = abs(n)
        headingRadians = radians(heading)#convert heading into radians

        deltaX = cos(headingRadians)
        deltaY = sin(headingRadians)

        return (deltaX, deltaY) #returns a tuple     



        

        
    def cameraLook(self, dt):  #this feels ineligant, there is probably a better way to do this
        if self.mouseWatcherNode.hasMouse(): #if mouse is on screen
            x = self.mouseWatcherNode.getMouseX()
            y = self.mouseWatcherNode.getMouseY()
            #if x != 0 and y != 0:
            #if self.win.movePointer(): #Testing this
            self.heading -= x * self.sensitivity
            self.pitch += y * self.sensitivity
            #print('heading: ' + str(self.heading) +  'pitch: ' + str(self.pitch))
            camRotation = self.cam.getHpr()
            self.cam.setHpr(camRotation[0] + self.heading, camRotation[1] + self.pitch, 0)
            self.heading = 0
            self.pitch = 0

            self.win.movePointer(0, floor(base.win.getXSize() / 2), floor(base.win.getYSize() / 2))

    def queuesBuilder(self, oldSlot, newSlot): #builds 2 queues: one for tiles to add, another for tiles to remove
        #slot is the dictionary of tiles
        #addQ = self.addQ
        #removeQ = self.removeQ
        for newCoord in newSlot: #for each coordinate in the slot dictionary
            if newCoord not in oldSlot: #if a coordinate is in new but NOT in old, then it is new and the model must be set up
                #add newCoord to the addQ
                self.addQ.append(newCoord)


                
                

                


                    
                self.tiles.setLight(self.plnp)#makes it so tile surface will respond to the light attached to the camera  #does this need to be called every time?
            #oldNodeCounter = 0
        for oldCoord in oldSlot:  #removes JUST the nodes that are out of radius due to player movement
            if oldCoord not in newSlot: 
                #then add this coordinate to queue of nodes to be removed
                self.removeQ.append(oldCoord)
                
                
        #return removeQ, addQ

    def updateQueues(self, removeQ, addQ): #called each cycle of run(): addes/removes tiles from first items in add/remove queues
        #pop next time in addQ and removeQ
        if addQ: #if addQ has an time to pop
            newCoord = addQ.pop(0)
            ##then add the new nodes
            if newCoord in self.newSurf.slot:  #cheesy
                model = self.newSurf.slot[newCoord][0].model  #fix this in Tile creation
                rotation = self.newSurf.slot[newCoord][0].rotation #add this to Tile Class
                #load the model
                self.modelDict[newCoord] = self.loader.loadModel(model)
                self.modelDict[newCoord].setPos(newCoord) #place model at coordinates
                self.modelDict[newCoord].setHpr(rotation) #rotate model
                self.modelDict[newCoord].setScale(self.scale) #set model scale
                self.modelDict[newCoord].reparentTo(self.tiles) #without this, model won't be rendered.
                #print('added node at ' + str(newCoord))#tp


        if removeQ:
            oldCoord = removeQ.pop(0)
            if oldCoord in self.modelDict:  #cheesy
                
                ##remove old nodes
                self.modelDict[oldCoord].removeNode()
                #print('removed node at ' + str(oldCoord))#tp
        
    def play(self, task):
        dt = globalClock.getDt()
        #print(dt)
        self.cameraLook(dt)
    
        #keyboard events!   #MAKE THIS A FUNCTION
        pos = self.jack.getPos()
        posCam = self.cam.getPos()
        rotation = self.cam.getHpr()
        dy, dx = self.angularMovement()
        #print(rotation)
        if keyMap["left"]:
            #pos.x -= self.speed * dt #old
            pos.y -= self.speed * dt * dx
            pos.x -= self.speed * dt * dy
         
        if keyMap["right"]:
            #pos.x += self.speed * dt
            #print(pos.x)
            pos.y += self.speed * dt * dx
            pos.x += self.speed * dt * dy
        if keyMap["up"]:
            pos.y += self.speed * dt * dy
            pos.x -= self.speed * dt * dx
            #print(pos.y)
        if keyMap["down"]: 
            #pos.y -= self.speed * dt
            pos.y -= self.speed * dt * dy
            pos.x += self.speed * dt * dx
        if keyMap["turn_left"]: 
            rotation[0] += self.turnSpeed * dt
            #print('turn left')
            
        if keyMap["turn_right"]:
            rotation[0] -= self.turnSpeed * dt
            
            #print('turn right')
        if keyMap["vertical_up"]: 
            pos.z += self.speed * dt
        if keyMap["vertical_down"]: 
            pos.z -= self.speed * dt
        #if keyMap["cam_switch"]:
            
            #print(pos.y)
        #if keyMap["turn_left"]
         #   rotation.h +=self.turnSpeed * dt
        #self.jack.setPos(pos)
        self.jack.setPos(pos)
        self.cam.setHpr(rotation)

        #really basic proof-of-concept biome changer.  should be a function, taking player position, checks if biome change needed based on dist from (0,0,0) and returns new biomeList
        #This should be its own function
        pcDist = wfcm.distance(pos, self.origin)
        if pcDist >= 10: #switch out biomes.  could be a function, really
            oldBiome = biomeList.pop(0) #remove first biome from the list
            biomeList.append(oldBiome) #old biome goes to end of the list
            print('new biome')
            self.origin = pos
            
           
        if self.newSurf: #if newSurf isn't an empty list
            self.collapseStatus = self.newSurf.collapseStep()
            if self.collapseStatus != 0 and self.prevSurf != self.newSurf: #if the step-wise collapse has finished collapsing the current new surface
            #then do the stuff to add the tile models to the scene
                #print('finished collapsing')
            
            #Places tile models into the mother node 'tiles'  
                self.queuesBuilder(self.prevSurf.slot, self.newSurf.slot) #creates queues of tiles to be added and removed
            
            #print('addQ' + str(self.addQ) +' removeQ: ' + str(self.removeQ))  #TP
            #need to save newSurf for next time
                self.prevSurf = self.newSurf
        
        #wip-should be a function
        #currently, second condition doesn't seem to be stopping it
        distance = wfcm.distance(self.anchorPos, pos) #distance between old and new coordinates of player
        if distance > 1 and self.collapseStatus != 0: #when distance threshold reached and the previous newSurface has been built
            #print('creating new Surface...')
            #update anchor to current pos of jack
            #self.anchorPos = self.cam.getPos()
            self.anchorPos = pos #pos of jack
            #move floor anchor to current player position
            floorAnchor = (floor(self.anchorPos[0]), floor(self.anchorPos[1]), floor(self.anchorPos[2])) 
            #create new surface
            self.newSurf = wfc.Surface(radius = masterRadius, tileList = biomeList[0], seed = r.randrange(sys.maxsize), playerPos = floorAnchor, oldSurf = self.prevSurf, flatMode = masterFlatMode) #basics of new map based on movement

            #fill in new parts of new surface with collapse()
        

            

        #need condition: if at least one of the queues had items to be popped off:
        #if 'newSurf' in vars() or 'newSurf' in globals():
        
        if self.removeQ or self.addQ: #if either Queue has any items to be handled 
            self.updateQueues(self.removeQ, self.addQ) #handles adding/removing of tile MODELS from the panda scene
        #else:
            #print('emptied Queues')
        #print('tic...')  #used to find how many loops its taking to collapse     
        return task.cont       
        
        

    
app = WFC(surf)
app.run()
