###WFC in Python: Version 13
'''
    This is the best version as of 3.25.2021.  with just 18 tiles, we can create a no-backtrack scenario of any 3d size.  Sizes above 10x10x10 produces exponentially slower load times.
    More Features to add:
        1.COMPLETED
        way to let a tile connect with multiple different connecters
            so an air block could connect with a floating block, like a balloon.
            Implementation:
                connecters are currently just integer values.  I could make them sets, lists, dictionaries.
                then, when checking connecters, I could just change the comparison to: if slot filled at direction, check connecter at [direction],
                compare with list of tiles [here], if a tile [here] does not *include* the connecter of the connecter in [direction], THEN remove it
                from the list.
            This should allow us to add new tiles without creating lots of backtracking by allowing the tiles to be more flexible with what they can connect
                to.
        2.COMPLETED
            Augmented Propogation
            Right now, when update slots' tile lists, we only update a slot if
            it touches a fully collapsed slot.
            Now, we need to make it so that all tiles are compared to each other 
        3.COMPLETED
            Panda3D Drawing
            need to make (or download) simple models to represent the tiles
            like we've done before, place 3d objects in space using the tuple coordinates in the dictionary
            will have to play around with getting the spacing/rotation looking decent
        4.COMPLETED
            Tile Weight
            Each tile should have a "weight" that determines its likelihood for being picked within the randTile() function
            -Add a weight variable to the Tile Object.  weight should be on a scale of 1 to 100
            -Change how randTile() draws tiles
                -instead of drawing random int between 1 and tile list length
                -we should use create a method (from random) that does the following weighted choice:
                sampleList = [100, 200, 300, 400, 500]
  
                randomList = random.choices(
                  sampleList, weights=(10, 20, 30, 40, 50), k=5)
  
                print(randomList)

        5.COMPLETED
            Infinite generation
            instead of fixed coordinates, generate in a radius around a variable called player position, stored in surface.
            player should maybe be its own object, with functions to get/set position,
                get position should round down to the nearest whole number
            player positon should start at 0,0,0
            I will have to drastically change how looping through the coordinate works
                currently workin in range 0 to maxX, 0 to maxY
                    will need to define a minX, and redfine maxX, to assume values equal to the player position -/+ the "radius"
                    then we can loop through minX and maxX to generate/update the coordinates
            everytime player moves to a new tile, we update the dictionary of the surface (self.slot)
                update minX,maxX for all 3 coordinates
                    --create new coordinate dictionary
                        loop through both dictionaries, and copy tiles over to new dictionary if a coordinate (x,y,z) is in both dictionaries
                            -if a coordinate in new dictionary doesn't have a "partner" in the old, then assign it the whole tileset list
                then run collapse on the new dictionary of the surface
                    --should collapse without a hitch
            at end of current collapse, we add a call to another function -- playerPositionUpdate
                thus freezing collapse function until player position changes again
            playerPositionUpdate
                -should return true or false
                -eventually, will ping player position from an object (a keyboard/mouse controller rigged to a camera), and return position every frame
                    - if player moved *enough*, will return TRUE, and will cause collapse sequence described above to run again
            Everytime the collapse finishes, it should pass the dictionary data to panda script, which will use it to update the rendered part
                if coord not in render coords, remove
                if coord new
                    assign it the correct model
            BIG question: should un-loaded slots be deleted or saved?
                -will result in MC issue of worlds becoming gigantic, although this shouldn't effect performance if its being saved to a file
                -if deleted, would ruin ability to do questing, ie, an npc says 'bring me ___ item' or is trapped and u must bring a key
                -possibility of making a sort of 'base', where player can choose a room to store loot, etc.
                    -waaay later in developement
                - could make a 'deleted' slot dictionary, then when player moves, check that new slots aren't in 'deleted' slot dictionary before regenerating

            UPDATE: 
                We have the infinite generation working based on player position, with some caveats:
                    1. RESOLVED!
                        load time is slow.  we are replacing all tiles each time the player movement threshold is reached.
                        -need to unload 'out of radius' tiles, and only load 'new' tiles
                        -could, inside surface class, generate list of 'remove' and 'new' tiles, in 2 new dictionaries
                            -then, in run, use 'remove' diction to remove
                        -see out they did infinite tunnel, should let us know how to do this, since its basically the same concept
                            -infinite tunnel sample uses models loaded to a list self.tunnel[x] = loader.loadModel('models/tunnel')
                            -maybe we can use a list, or even better a dictionary, as we load in our models
                        -issue with this now removed ALL of the previous loaded area's tiles instead of just the uncommon ones.  but it does seem faster
                    2. RESOLVED
                        sometime loading chunks in once direction really quick causes strange repeating patterns.  not sure why, but with big tiles this may not be an issue.
                        #might be an issue with how/when we decide to load new areas based on player position
        5.COMPLETED
            Tile "Biomes"
            increasing the number of tilesin the tileset may begin to effect load times, but not having enough tiles will result in boring, repeating maps.  Solution: biomes.
            based on player position (or perhaps time based?) a different tileset will be chosen to generate new tiles on when new entries are added to the map dictionary.  This
            could work in rings like we originally imagined, where player distance from origin (0,0,0) will effect difficulty, map generation, etc.  alteratively, could be based on
            time (like risk of rain 2) or better yet maybe, base it on player loot or player level.  New tilesets can be unlocked via player acheivements, like in binding of isaac
        6. Player controller
            -wasd movement, camera to look around
            -moves camera around
            -eventually add gravity/collision with walls, floor, etc.
            #UPDATE:
                we have basic WASD and mouse first person camera set up, but no phsyics between player and world.
                    This is good enough until we deal with the performance issues.  
        7. Increasing Performance
            #the infinite city example had an area of of 10x10x5, or 500 tiles, and it ran pretty smoooth
            #we are getting some "stuttering" (screen pauses for a moment, like half a second) when we generate a new surface
            #we need to seriously rethink how the collapse() function runs in accordance with the game's main loop
                #like, maybe run each step of the collapse loop each time the game's run loop iterates.
                    #if we moved enough
                        #do some of the collapse per main loop
                    #if we finished collapse of the new surface area
                        #do the normal procedude of addQ/removeQ 
            secondly, having really big maps (we did 14x14x14 at 12fps) causes frame rates to plummet.
                I suspect the issue is either
                    1) each tile model is composed of multiple meshes
                    2) something related to the tiles in the main loop is being done each time that is consuming resources
                I know ive already seen panda scenes with way more geometry then what we have (like the heightmaps), so I don't think that's an issue.
            #UPDATE## Doing WFC stepwise fixed the bumpiness, but created a program where the player could very quickly outrun the map generation.  Increasing steps done per run loop
                starts to reintroduce bumpiness.  
                #options:
                    #we could analyze how our wfc runs and try to find areas where we can speed it up
                    # we can settle for smaller maps, losing vertical view distance
                        #something like 8x8 by 3 might be small enough.  8x8x1 currently runs at 60 fps
                        #making the scale of what a tile is larger would reduce the weight on the wfc, allowing for maps with less tiles to still be "big" for the player
                        
                    #we could try improving wfc time by using pynum or scipy
                    #we could rewrite the wfc in c++

                    #as of writing this, I think trying 2 and 3 would be easy
                        #having really tall areas would *look* cool, but really isn't necessary
                    #Another options: do wfc in much larger radius than rendered tiles
                        #sure, larger radius would take more steps, but with our stepwise system, will not cause bumpiness in movement
                        #right now, most loops do not do any collapse, so we could view this as missed potential
                    
                            
                        
        7. Better Tile Models, more Tiles 
            The main thing is making a map we can walk through
            We will have to spend time thinking aboue game design at this point: what sort of map are we creating?
                Don't focus on art, just room types, sizes, etc.
            Empty rooms, staircases, etc.  Add rooms that connect together into bigger rooms
            Elevators would be cool.  generate the shafts for now, then add in events for it.
        8. Program restructuring
            A lot of the code we've written should be contained within functions and classes, and seperated into different files.  our runwfc file is especially messy
        9. Building the Game: Populating the map
            The next step is taking the map and adding another layer of random generation: that of putting chests, enemies, and other interactable items into the map
            One way to do this would be to spawn things as the map bring the tile into view
                take a random draw from a hat of possibilities that a chest or an enemy will be placed there
                certain tiles have certain possible spawns associated with them
                    ie, a laboratory might have a change of spawning a potions ( and then a random weighted draw of what kind)
            Issues: moving enemies: what happens to enemy that falls out of loaded area?
                I suppose it should despawn
            there should be a standard starting room.  similar rooms like it should spawn that have some sort of npc or machine that does leveling
            could be store rooms as well, or vending machines like in bioshock/borderlands
                

'''

import random as r
import pickle as pickle
from panda3d.core import loadPrcFileData
configVars = """
win-size 1280 720
window-title My Game
show-frame-rate-meter 1
show-scene-graph-analyzer-meter 1
"""
loadPrcFileData("", configVars)
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import PointLight, AmbientLight, NodePath
from math import sin, cos
from direct.filter.CommonFilters import CommonFilters

import sys

###

#working
#A class to store tiles and their information
class Tile():
    def __init__(self, cTuple = ({0},{0},{0},{0},{0},{0}), name = 'default', model = '', rotation = (0,0,0), weight = 100):
        #the way the tile is allowed to connect with others
        #the values are like jigsaw puzzle connections, n connects with n
        self.rotation = rotation #holds the rotation of the model
        self.connecters = {'north':set(cTuple[0]),'east':set(cTuple[1]),'south':set(cTuple[2]),'west':set(cTuple[3]),'above':set(cTuple[4]),'below':set(cTuple[5])}
        self.name = name
        self.model = model #holds a string with the name of the file

        self.weight = weight #weight effects how likely tile is to be chosen. 1 to 100
        
    def setConnecters(self, north, east, south, west, above, below):
        self.connecters['north'] = {north}
        self.connecters['east'] = {east}
        self.connecters['south'] = {south}
        self.connecters['west'] = {west}
        self.connecters['above'] = {above}
        self.connecters['below'] = {below}
    def setName(self, name):
        self.name = name
    def setModel(self, model):
        self.model = model

defTileList = [Tile(),Tile(),Tile(),Tile()]

#working
class Surface(): #the surface is what the tiles are placed on
    def __init__(self, radius = 3, tileList = defTileList, seed = r.randrange(sys.maxsize), playerPos = (0,0,0), oldSurf = 0, flatMode = 0): #s = Surface((10,10,20))
        
        self.seed = seed
        #print(self.seed)
        r.seed(seed)
        #self.x = dimensions[0] #dim is tuple, optional
        #self.y = dimensions[1] 
        #self.z = dimensions[2]
        self.tileList = tileList

        self.maxTiles = len(tileList) #the max tiles in a slot.
        
        #a dictionary with keys as tuples, values as all posible tiles
        #need to create all possible tuples
        #volume = self.x * self.y * self.z

        self.minX = playerPos[0] - radius
        self.maxX = playerPos[0] + radius
        self.minY = playerPos[1] - radius
        self.maxY = playerPos[1] + radius
        self.minZ = playerPos[2] - radius
        self.maxZ = playerPos[2] + radius
        if flatMode == 1:
            self.minZ = 0
            self.maxZ = 1
        
        volume = radius ** 3
        self.keyList = [] #stores the tuples
        count = 0
        for i in range(self.minX,self.maxX):
            for j in range(self.minY, self.maxY):
                for k in range(self.minZ, self.maxZ):
                    newTup = (i, j, k)
                    self.keyList.append(newTup)
                    count += 1
        #print(str(count))   #TP
        #valList = range(volume)
                    
        self.valList = []
        
        length = len(self.keyList)
        if oldSurf == 0: #if there is no surface being passed to this constructor, then this is the very first surface, and is populated as below     
            self.valList = [0]*length #make valList initialized with zeros with length equal to keyList's length
            for i in range(length):
                #self.valList.append(tileList.copy()) #not working at all
                self.valList[i] = tileList.copy()
        else: #if an oldSurf was passed, then we need to copy values
            #valIndex = 0
            for coord in self.keyList:
                if coord in oldSurf.slot: #if the coord in the new Surface is also in the old surface...
                    self.valList.append(oldSurf.slot[coord]) #copy tile of old to new at this coordinate
                else: #if this coord in the new surface is unique...
                    self.valList.append(tileList.copy()) #then its valList is all possible tiles for this tile Set
                #valIndex += 1
        self.slot = dict(zip(self.keyList,self.valList)) #puts valList and keyList together into a dictionary, which is the world map
        
        #history properties
        self.chrono = [] #stores a coordinate tuple each time that tuple is updated.  allows for repeats
        self.ttcounter = 0  #time travel counter: counts how many times we've erase history, used to increase potency of erase history after each call
        
        
    def randTile(self, coords): #takes coords from entropy, randomly picks a tile
        #print('coords in randTile(): ' + str(coords))
        #x = coords[0]
        #y = coords[1]
        #z = coords[2] #unpack a little to make more readable
        #print("seed in randTile() " + str(self.seed))
        #length = len(self.slot[coords])-1  #pre weight system
        #choice = r.randint(0,length)  #pre weight system

        #list of choices at this tile
        tileList = []
        weightList = []
        for entry in self.slot[coords]: #for each tile at this slot in the dictionary
            tileList.append(entry) #append tile to Tilelist
            weightList.append(entry.weight) #append that tiles weight to the weightList
        choice = r.choices(tileList, weightList) #weighted choice
        #self.slot[coords] = [self.slot[coords][choice]] #pick a random tile to be the choice
        self.slot[coords] = choice # put the chosen tile back in as the only remaining tile at this coordinate, packaged as a single item list
        #print("random choice: " + self.slot[coords][0].name + " at: " + str(coords))
        
    def writeHistory(self,coords): #add new coords
        self.chrono.append(coords)
    def eraseHistory(self,n): #erase history n steps when we backtrack
        self.ttcounter += 1
        #old backtracking function that only worked sometimes
        
        #n = self.ttcounter + 4
        n = n + self.ttcounter   #trying to make erase stronger each iteration
        for i in range(n):
            if(len(self.chrono) > 1):
                pos = self.chrono.pop()
                self.slot[pos] = self.tileList.copy() #the tilelist at the erased slot is now back to being the whole tile set
                print("reset " + str(pos) +" ", end = "")
        print("")
        ##hard reset mode: if any error, restart
        
        #print('reset all slots')
    """
        #self.slot = dict(zip(self.keyList,self.valList)) #does not reset all slots as intended
    def eraseHistoryRadius(self,coords,r): #erase all slots in radius around tile          
        volume = r ** 3
        nextDoors = []
        for i in range(volume-1): #generate coords
        """

    #if a slot doese not have a set tile, then we should display the weight instead
    def display(self): #display matrix as it runs to better understand when/why it fails
        #print(surf.slot[start][0].name + " at " + str(start))
        
        
        
        for k in range(minZ,maxZ):
            for j in range(minY,maxY):
                for i in range(minX,maxX):
                    if len(self.slot[i,j,k]) > 1:
                        weight = len(self.slot[i,j,k])
                        print(str(weight) + " ", end='')
                    else:
                        print(self.slot[i,j,k][0].name + " ",  end='')
                print("")#for newline
            print("")
    #def changeMap(newPosition): #this function should update the map, adding and deleting positions.  

    def initialize(self): #picks a random starting point. returns tuple  #shoult take seed from Surface.seed
        seed = self.seed
        r.seed(seed)
        initX = r.randint(self.minX, self.maxX-1)
        initY = r.randint(self.minY, self.maxY-1)
        initZ = r.randint(self.minZ, self.maxZ-1)
        start = initX, initY, initZ
        return start        
            
    def collapseStep(self): #Each call collapses the surface
        #instead of going until full collapse, go 1 step.  while doCollapse == True: collapse like normal then at end: doCollapse == False
        #only return matrix if we did full collapse, other wise return 0
         #the dictionary that is the map
        matrix = self.slot
        fullCollapse = False #turns true when all slots filled with tiles
        minX = self.minX
        maxX = self.maxX
        minY = self.minY
        maxY = self.maxY
        minZ = self.minZ
        maxZ = self.maxZ

        stepCounter = 0

        
        volume =  (abs(minX) + abs(maxX)) * (abs(minY) + abs(maxY)) * (abs(minZ) + abs(maxZ))
        #print("In collapse function!")

        didOneStep = False
        
        #while fullCollapse == False: #while we still need to collapse slots
        while didOneStep == False: #while we havn't yet done a step
            slotsFilled = 0
            madeUpdate = False #tracks whether any updates were made, bc if not, we need to pick another tile randomly at the lowest entropy slot
            for k in range(minZ, maxZ): #run through all coords
                for j in range(minY, maxY):
                    for i in range(minX, maxX):

                        updatedThisSlot = False #tracks if we changed tiles at this slot.  if true, we add it to the history at the end of this innermost loop
                        
                        #print("at: " + str(i) +", " + str(j) + ", " + str(k))
                        #if type(matrix[(i,j,k)]) == Tile: #if slot is filled ###ERROR, If 1 tile, this no longer works! Alternative : type? type(surf.slot[0,1,0]) == wfc.Tile
                        if len(matrix[i,j,k]) == 1: #should stop editing of already filled tiles
                            slotsFilled += 1
                            #print(str(slotsFilled) + "/" + str(volume))
                            if slotsFilled == volume:          #this may no longer be neccessary to stop the loop do to entropy function also detected full collapse
                                fullCollapse = True #stop the collapse
                                #print("reached Full Collapse")
                                break
                        else:
                            here = (i,j,k)
                            above = (i,j,k+1)
                            below = (i,j,k-1)
                            north = (i,j-1,k) #switched north and south
                            south = (i,j+1,k)
                            east = (i+1,j,k)
                            west = (i-1,j,k)
                            #check all 6 faces
                            #above
                            if above in matrix: #if the coords are even there
                                if len(matrix[above]) < self.maxTiles: #we should only compare slots with less than the max amount of tiles, no point comparing a 5 to a 9
                                    
                                    #c = matrix[above][0].connecters['below'] #read above connecter [replaced with below]
                                    allNextDoorTiles = set([]) #an empty set to store the intersection of all of above slot's 'below' connecters for all tiles
                                
                                    for tile in matrix[above]: #for all above slot's tiles
                                        allNextDoorTiles = allNextDoorTiles | tile.connecters['below'] #add the below connectors to this set
                                    #remove all tiles accept those that share a connecter with any in allNextDoorTiles
                                    copyMatrix = matrix[here].copy()
                                    for tile in matrix[here]:
                                        if not tile.connecters['above'] &  allNextDoorTiles: #for each tile in slot [here], if it shares no connecters with any tiles ['above'], remove it

                                        #if not tile.connecters['above'] &  c: #if the connecter of the possible tile does not match the connecter of the above determined tile
                                            #print('removed ' + tile.name + " at " + str(here) + " because above slot was a " + matrix[above][0].name )
                                            #remove this tile fom the list
                                            #matrix[here].remove(tile)
                                            copyMatrix.remove(tile)
                                            madeUpdate = True
                                            updatedThisSlot = True
                                    
                                    matrix[here] = copyMatrix #replace old matrix of tiles with new, updated matrix (note: matrix is a dictionary)
                                   
                                    if len(matrix[here]) == 0: #error check for complete emptying
                                        print("ERROR: EMPTIED SLOT " + str(here))
                                        self.writeHistory(here) #need to record this location so it gets reset
                                        self.eraseHistory(5) #try 5, may have to play around
                                        #i, j, k = 0,0,0 #may not be neccessary 
                            if below in matrix: 
                                if len(matrix[below]) < self.maxTiles:
                                    allNextDoorTiles = set([])
                                    
                                    for tile in matrix[below]: 
                                        allNextDoorTiles = allNextDoorTiles | tile.connecters['above'] 
                                    copyMatrix = matrix[here].copy()
                                    for tile in matrix[here]:
                                        if not tile.connecters['below'] & allNextDoorTiles:
                                            #print('removed ' + tile.name + " at " + str(here) + " because below slot was a " + matrix[below][0].name )
                                            #matrix[here].remove(tile)
                                            copyMatrix.remove(tile)
                                            madeUpdate = True
                                            updatedThisSlot = True
                                    matrix[here] = copyMatrix
                                    #if len(matrix[here]) == 1:  #if we reduced this slot to a certain tile at this step
                                        #self.writeHistory(here)#record it in the history list
                                    if len(matrix[here]) == 0:
                                        print("ERROR: EMPTIED SLOT"+ str(here))
                                        self.writeHistory(here)
                                        self.eraseHistory(5) #try 5, may have to play around
                                        #i, j, k = 0,0,0
                            if north in matrix: 
                                if len(matrix[north]) < self.maxTiles:
                                    #c = matrix[north][0].connecters['south']
                                    allNextDoorTiles = set([])
                                    for tile in matrix[north]: 
                                        allNextDoorTiles = allNextDoorTiles | tile.connecters['south']
                                    copyMatrix = matrix[here].copy()
                                    for tile in matrix[here]:
                                        if not tile.connecters['north'] & allNextDoorTiles:
                                            #print('removed ' + tile.name + " at " + str(here) + " because north slot was a " + matrix[north][0].name )
                                            #matrix[here].remove(tile)
                                            copyMatrix.remove(tile)
                                            madeUpdate = True
                                            updatedThisSlot = True
                                    matrix[here] = copyMatrix
                                    #if len(matrix[here]) == 1:  #if we reduced this slot to a certain tile at this step
                                        #self.writeHistory(here)#record it in the history list
                                    if len(matrix[here]) == 0:
                                        print("ERROR: EMPTIED SLOT"+ str(here))
                                        self.writeHistory(here)
                                        self.eraseHistory(5) #try 5, may have to play around
                                        #i, j, k = 0,0,0
                            if south in matrix: 
                                if len(matrix[south]) < self.maxTiles:
                                    #c = matrix[south][0].connecters['north']
                                    allNextDoorTiles = set([])
                                    for tile in matrix[south]: 
                                        allNextDoorTiles = allNextDoorTiles | tile.connecters['north']
                                    copyMatrix = matrix[here].copy()
                                    for tile in matrix[here]:
                                        if not tile.connecters['south'] & allNextDoorTiles:
                                            #print('removed ' + tile.name + " at " + str(here) + " because south slot was a " + matrix[south][0].name )
                                            #matrix[here].remove(tile)
                                            copyMatrix.remove(tile)
                                            madeUpdate = True
                                            updatedThisSlot = True
                                    matrix[here] = copyMatrix
                                    #if len(matrix[here]) == 1:  #if we reduced this slot to a certain tile at this step
                                        #self.writeHistory(here)#record it in the history list
                                    if len(matrix[here]) == 0:
                                        print("ERROR: EMPTIED SLOT"+ str(here))
                                        self.writeHistory(here)
                                        self.eraseHistory(5) #try 5, may have to play around
                                        #i, j, k = 0,0,0
                            if east in matrix: 
                                if len(matrix[east]) < self.maxTiles:
                                    #c = matrix[east][0].connecters['west']
                                    allNextDoorTiles = set([])
                                    for tile in matrix[east]: 
                                        allNextDoorTiles = allNextDoorTiles | tile.connecters['west']
                                    copyMatrix = matrix[here].copy()
                                    for tile in matrix[here]:
                                        if not tile.connecters['east'] & allNextDoorTiles:
                                            #print('removed ' + tile.name + " at " + str(here) + " because east slot was a " + matrix[east][0].name )
                                            #matrix[here].remove(tile)
                                            copyMatrix.remove(tile)
                                            madeUpdate = True
                                            updatedThisSlot = True
                                    matrix[here] = copyMatrix
                                    #if len(matrix[here]) == 1:  #if we reduced this slot to a certain tile at this step
                                        #self.writeHistory(here)#record it in the history list
                                    if len(matrix[here]) == 0:
                                        print("ERROR: EMPTIED SLOT" + str(here))
                                        self.writeHistory(here)
                                        self.eraseHistory(5) #try 5, may have to play around
                                        #i, j, k = 0,0,0
                            if west in matrix: 
                                if len(matrix[west]) < self.maxTiles:
                                    #c = matrix[west][0].connecters['east']
                                    allNextDoorTiles = set([])
                                    for tile in matrix[west]: 
                                        allNextDoorTiles = allNextDoorTiles | tile.connecters['east']
                                    copyMatrix = matrix[here].copy()
                                    for tile in matrix[here]:
                                        if not tile.connecters['west'] & allNextDoorTiles:
                                            #print('removed ' + tile.name + " at " + str(here) + " because west slot was a " + matrix[west][0].name )
                                            #matrix[here].remove(tile)
                                            copyMatrix.remove(tile)
                                            madeUpdate = True
                                            updatedThisSlot = True
                                    matrix[here] = copyMatrix
                                    #if len(matrix[here]) == 1:  #if we reduced this slot to a certain tile at this step
                                        #self.writeHistory(here)#record it in the history list
                                    if len(matrix[here]) == 0:
                                        print("ERROR: EMPTIED SLOT" + str(here))
                                        self.writeHistory(here)
                                        self.eraseHistory(5) #try 5, may have to play around
                                        #i, j, k = 0,0,0

                        if updatedThisSlot == True: #if we updated the tiles at this slot
                            self.writeHistory(here)
                            
            #self.display()    #Shows the step-by-step tiling of the surface's slots

          
            if madeUpdate == False: #if we ran through all slots and made no changes
                #then we should pick a slot and set its tile randomly
                newCoords = entropy(matrix) #get lowest entropy coords
                #print(str(newCoords), '  line 444')
                if newCoords == ('a','a','a'): #entropy() returns this tuple if all slots have entropy = 1, ie, the surface is filled fully
                    fullCollapse = True
                else:
                    self.randTile(newCoords) #set tile randomly at lowest entropy coords
                    self.writeHistory(newCoords) #add these coordinates to history
                #print("chose random tile at " + str(newCoords))
                stepCounter +=1
                if stepCounter == 40: #one step at a time is too slow, needed to try speeding it up
                    didOneStep = True #So, a step is thus every time we made it through without an update
        
                
        if fullCollapse == True: #if we fully collapsed the current dictionary       
            return matrix
        else:
            return 0
    def collapse(self):  #need to change collapse to take a partially filled matrix.  maybe a new function all together, keep this one for initial map area generation
    
         #the dictionary that is the map
        matrix = self.slot
        fullCollapse = False #turns true when all slots filled with tiles
        minX = self.minX
        maxX = self.maxX
        minY = self.minY
        maxY = self.maxY
        minZ = self.minZ
        maxZ = self.maxZ

        
        volume =  (abs(minX) + abs(maxX)) * (abs(minY) + abs(maxY)) * (abs(minZ) + abs(maxZ))
        #print("In collapse function!")
        while fullCollapse == False: #while we still need to collapse slots
            slotsFilled = 0
            madeUpdate = False #tracks whether any updates were made, bc if not, we need to pick another tile randomly at the lowest entropy slot
            for k in range(minZ, maxZ): #run through all coords
                for j in range(minY, maxY):
                    for i in range(minX, maxX):

                        updatedThisSlot = False #tracks if we changed tiles at this slot.  if true, we add it to the history at the end of this innermost loop
                        
                        #print("at: " + str(i) +", " + str(j) + ", " + str(k))
                        #if type(matrix[(i,j,k)]) == Tile: #if slot is filled ###ERROR, If 1 tile, this no longer works! Alternative : type? type(surf.slot[0,1,0]) == wfc.Tile
                        if len(matrix[i,j,k]) == 1: #should stop editing of already filled tiles
                            slotsFilled += 1
                            #print(str(slotsFilled) + "/" + str(volume))
                            if slotsFilled == volume:          #this may no longer be neccessary to stop the loop do to entropy function also detected full collapse
                                fullCollapse = True #stop the collapse
                                #print("reached Full Collapse")
                                break
                        else:
                            here = (i,j,k)
                            above = (i,j,k+1)
                            below = (i,j,k-1)
                            north = (i,j-1,k) #switched north and south
                            south = (i,j+1,k)
                            east = (i+1,j,k)
                            west = (i-1,j,k)
                            #check all 6 faces
                            #above
                            if above in matrix: #if the coords are even there
                                if len(matrix[above]) < self.maxTiles: #we should only compare slots with less than the max amount of tiles, no point comparing a 5 to a 9
                                    
                                    #c = matrix[above][0].connecters['below'] #read above connecter [replaced with below]
                                    allNextDoorTiles = set([]) #an empty set to store the intersection of all of above slot's 'below' connecters for all tiles
                                
                                    for tile in matrix[above]: #for all above slot's tiles
                                        allNextDoorTiles = allNextDoorTiles | tile.connecters['below'] #add the below connectors to this set
                                    #remove all tiles accept those that share a connecter with any in allNextDoorTiles
                                    copyMatrix = matrix[here].copy()
                                    for tile in matrix[here]:
                                        if not tile.connecters['above'] &  allNextDoorTiles: #for each tile in slot [here], if it shares no connecters with any tiles ['above'], remove it

                                        #if not tile.connecters['above'] &  c: #if the connecter of the possible tile does not match the connecter of the above determined tile
                                            #print('removed ' + tile.name + " at " + str(here) + " because above slot was a " + matrix[above][0].name )
                                            #remove this tile fom the list
                                            #matrix[here].remove(tile)
                                            copyMatrix.remove(tile)
                                            madeUpdate = True
                                            updatedThisSlot = True
                                    
                                    matrix[here] = copyMatrix #replace old matrix of tiles with new, updated matrix (note: matrix is a dictionary)
                                   
                                    if len(matrix[here]) == 0: #error check for complete emptying
                                        print("ERROR: EMPTIED SLOT " + str(here))
                                        self.writeHistory(here) #need to record this location so it gets reset
                                        self.eraseHistory(5) #try 5, may have to play around
                                        #i, j, k = 0,0,0 #may not be neccessary 
                            if below in matrix: 
                                if len(matrix[below]) < self.maxTiles:
                                    allNextDoorTiles = set([])
                                    
                                    for tile in matrix[below]: 
                                        allNextDoorTiles = allNextDoorTiles | tile.connecters['above'] 
                                    copyMatrix = matrix[here].copy()
                                    for tile in matrix[here]:
                                        if not tile.connecters['below'] & allNextDoorTiles:
                                            #print('removed ' + tile.name + " at " + str(here) + " because below slot was a " + matrix[below][0].name )
                                            #matrix[here].remove(tile)
                                            copyMatrix.remove(tile)
                                            madeUpdate = True
                                            updatedThisSlot = True
                                    matrix[here] = copyMatrix
                                    #if len(matrix[here]) == 1:  #if we reduced this slot to a certain tile at this step
                                        #self.writeHistory(here)#record it in the history list
                                    if len(matrix[here]) == 0:
                                        print("ERROR: EMPTIED SLOT"+ str(here))
                                        self.writeHistory(here)
                                        self.eraseHistory(5) #try 5, may have to play around
                                        #i, j, k = 0,0,0
                            if north in matrix: 
                                if len(matrix[north]) < self.maxTiles:
                                    #c = matrix[north][0].connecters['south']
                                    allNextDoorTiles = set([])
                                    for tile in matrix[north]: 
                                        allNextDoorTiles = allNextDoorTiles | tile.connecters['south']
                                    copyMatrix = matrix[here].copy()
                                    for tile in matrix[here]:
                                        if not tile.connecters['north'] & allNextDoorTiles:
                                            #print('removed ' + tile.name + " at " + str(here) + " because north slot was a " + matrix[north][0].name )
                                            #matrix[here].remove(tile)
                                            copyMatrix.remove(tile)
                                            madeUpdate = True
                                            updatedThisSlot = True
                                    matrix[here] = copyMatrix
                                    #if len(matrix[here]) == 1:  #if we reduced this slot to a certain tile at this step
                                        #self.writeHistory(here)#record it in the history list
                                    if len(matrix[here]) == 0:
                                        print("ERROR: EMPTIED SLOT"+ str(here))
                                        self.writeHistory(here)
                                        self.eraseHistory(5) #try 5, may have to play around
                                        #i, j, k = 0,0,0
                            if south in matrix: 
                                if len(matrix[south]) < self.maxTiles:
                                    #c = matrix[south][0].connecters['north']
                                    allNextDoorTiles = set([])
                                    for tile in matrix[south]: 
                                        allNextDoorTiles = allNextDoorTiles | tile.connecters['north']
                                    copyMatrix = matrix[here].copy()
                                    for tile in matrix[here]:
                                        if not tile.connecters['south'] & allNextDoorTiles:
                                            #print('removed ' + tile.name + " at " + str(here) + " because south slot was a " + matrix[south][0].name )
                                            #matrix[here].remove(tile)
                                            copyMatrix.remove(tile)
                                            madeUpdate = True
                                            updatedThisSlot = True
                                    matrix[here] = copyMatrix
                                    #if len(matrix[here]) == 1:  #if we reduced this slot to a certain tile at this step
                                        #self.writeHistory(here)#record it in the history list
                                    if len(matrix[here]) == 0:
                                        print("ERROR: EMPTIED SLOT"+ str(here))
                                        self.writeHistory(here)
                                        self.eraseHistory(5) #try 5, may have to play around
                                        #i, j, k = 0,0,0
                            if east in matrix: 
                                if len(matrix[east]) < self.maxTiles:
                                    #c = matrix[east][0].connecters['west']
                                    allNextDoorTiles = set([])
                                    for tile in matrix[east]: 
                                        allNextDoorTiles = allNextDoorTiles | tile.connecters['west']
                                    copyMatrix = matrix[here].copy()
                                    for tile in matrix[here]:
                                        if not tile.connecters['east'] & allNextDoorTiles:
                                            #print('removed ' + tile.name + " at " + str(here) + " because east slot was a " + matrix[east][0].name )
                                            #matrix[here].remove(tile)
                                            copyMatrix.remove(tile)
                                            madeUpdate = True
                                            updatedThisSlot = True
                                    matrix[here] = copyMatrix
                                    #if len(matrix[here]) == 1:  #if we reduced this slot to a certain tile at this step
                                        #self.writeHistory(here)#record it in the history list
                                    if len(matrix[here]) == 0:
                                        print("ERROR: EMPTIED SLOT" + str(here))
                                        self.writeHistory(here)
                                        self.eraseHistory(5) #try 5, may have to play around
                                        #i, j, k = 0,0,0
                            if west in matrix: 
                                if len(matrix[west]) < self.maxTiles:
                                    #c = matrix[west][0].connecters['east']
                                    allNextDoorTiles = set([])
                                    for tile in matrix[west]: 
                                        allNextDoorTiles = allNextDoorTiles | tile.connecters['east']
                                    copyMatrix = matrix[here].copy()
                                    for tile in matrix[here]:
                                        if not tile.connecters['west'] & allNextDoorTiles:
                                            #print('removed ' + tile.name + " at " + str(here) + " because west slot was a " + matrix[west][0].name )
                                            #matrix[here].remove(tile)
                                            copyMatrix.remove(tile)
                                            madeUpdate = True
                                            updatedThisSlot = True
                                    matrix[here] = copyMatrix
                                    #if len(matrix[here]) == 1:  #if we reduced this slot to a certain tile at this step
                                        #self.writeHistory(here)#record it in the history list
                                    if len(matrix[here]) == 0:
                                        print("ERROR: EMPTIED SLOT" + str(here))
                                        self.writeHistory(here)
                                        self.eraseHistory(5) #try 5, may have to play around
                                        #i, j, k = 0,0,0

                        if updatedThisSlot == True: #if we updated the tiles at this slot
                            self.writeHistory(here)
                            
            #self.display()    #Shows the step-by-step tiling of the surface's slots

          
            if madeUpdate == False: #if we ran through all slots and made no changes
                #then we should pick a slot and set its tile randomly
                newCoords = entropy(matrix) #get lowest entropy coords
                #print(str(newCoords), '  line 444')
                if newCoords == ('a','a','a'): #entropy() returns this tuple if all slots have entropy = 1, ie, the surface is filled fully
                    fullCollapse = True
                else:
                    self.randTile(newCoords) #set tile randomly at lowest entropy coords
                    self.writeHistory(newCoords) #add these coordinates to history
                #print("chose random tile at " + str(newCoords))
                
               
        return matrix
        
        


#ISSUE: counting slots with 1 tile as lowest entropy
def entropy(d): #only need to calculate entropy of effected tiles
    #d is the dictionary
    #loop through all possible x,y,z values: for i in d: d[i]
    minWeight = {'coords':('a','a','a'),'weight':1000}
    for i in d: #for all the slots on the surface
        weight = len(d[i]) #tiles stored in a list
        if weight < minWeight['weight'] and weight != 1:
            minWeight['weight'] = weight
            minWeight['coords'] = i
    #print("chose random tile at " + str(minWeight['coords']))
    return minWeight['coords'] #returns the coordinate tuple

    





    
    
        
        



       
   

        
    
        
        

