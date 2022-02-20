# WFC
My Implementation of the Wave Function Collapse algorithm for procedural map generation in 3 dimensions.  Visualized using Panda3d.

Last updated: 20 Feb, 2022
Wave Function Collapse (WFC) is an algorithm for procedural map generation in 2 or 3 dimensions.  The basic principle is that at every cell in the grid, every possible tile exists simultaneously.  At some point in the grid, either by a human or randomly, a single tile is chosen.  Then, all the tiles in the grid are updated according to a set of rules for which tiles are allowed to be next to each other, which is referred to as "collapsing".  When a cell only has one possible location left, it is drawn.  If the cells cannot be collapsed further, the uncollapsed cell with least entropy (defined as the least number of tiles it could still assume) is selected and collapsed randomly to one of its possible tiles.  
RUNNING THIS SCRIPT
    Only the file "runWFCv14_4 [presentation]" needs to be run, the other file containing function defitions only.  Panda3d (an open source game engine for python) will need to be installed for this to work.  Once the program as launced, the mouse can be used to rotate a camera, and standard "WASD" controlls will move a "player" object, around which a series of pipes will be placed according to the WFC algorithm.  
