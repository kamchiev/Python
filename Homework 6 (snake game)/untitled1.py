# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 14:40:23 2022

@author: khayo
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
You have just been hired at a video game software house and you have
to render the snake game on an image  by saving the final image of the
snake's path and returning the length of the snake.
Implement the generate_snake function that takes as input a path to an
image file, which is the starting image "start_img". The image can
contain black background pixels, obstacle for the snake as red pixels
and finally food as orange pixels. The snake must be drawn in green.
In addition you must draw in gray the trail that the snake leaves onto
its path. The function also takes as input the initial snake position,
"position" as a list of two integers X and Y. The commands of the
player on how to move the snake in the video game are available in a
string "commands."  The function must save the final image of the
snake's path to the path "out_img," which is passed as the last input
argument to the function. In addition, the function must return the
length of the snake at the end of the game.

Each command in "commands" corresponds to a cardinal sign, followed by
a space. The possible cardinal signs are:

| NW | N | NE |
| W  |   |  E |
| SW | S | SE |

corresponding to one-pixel snake movements such as:

| up-left     | up     | up-right     |
| left        |        | right        |
| bottom-left | bottom | bottom-right |

The snake moves according to the commands; in the case the snake
eats food, it increases its size by one pixel.

The snake can move from side to side of the image, horizontally and
vertically, this means that if the snake crosses a side of the image,
it will appear again from the opposite side.
The game ends when the commands are over or the snake dies. The snake
dies when:
- it hits an obstacle
- it hits itself so it cannot pass over itself
- crosses itself diagonally. As an examples, a 1->2->3-4 path like the
  one below on the left is not allowed; while the one on the right is
  OK.

  NOT OK - diagonal cross        OK - not a diagonal cross
       | 4 | 2 |                    | 1 | 2 |
       | 1 | 3 |                    | 4 | 3 |

For example, considering the test case data/input_00.json
the snake starts from "position": [12, 13] and receives the commands
 "commands": "S W S W W S W N N W N N N N N W N" 
generates the image in visible in data/expected_end_00.png
and returns 5 since the snake is 5 pixels long at the
end of the game.

NOTE: Analyze the images to get the exact color values to use.

NOTE: do not import or use any other library except images.
'''


# load image 
# import commands
# define the colors
# check if the move is legal (if out of the border do sth )
    # - red 
    # - itself
    # - dioganal crossing
# keep track of the tail change it when it is necessary
# 


import images


def generate_snake(start_img: str, position: list[int, int],
                   commands: str, out_img: str) -> int:
    #use x,y = a,b trick
    background = (0,0,0) #black
    obstacle = (255,0,0) #red
    food = (255,128,0) #orange
    green = (0,255,0) #green guess
    gray = (128,128,128) #grey guess
    
    r,c = position #intial coordinate
    
    matrix = images.load(start_img) #image
    
    com = commands.split() #make commands list
    
    
    
    height = len(matrix)
    width = len(matrix[0])
    
    corners = ('NW','NE','SW','SE')
    alive = True
    
    
    while alive:
        
        
        if r > height:
            r = matrix
        
        #here we checked for diagonal crossing (itself)
        
        diag = False
        if com[0] in corners:
            d1,d2 = moves(com[0],r,c)[2:]
            
            if moves(d1,r,c) == green and moves(d2,r,c) == green:
                diag = True
            
        #let's see cases which kills snake 
        # red pixel, green pixel (itself), dioganal crossing (itself)
        
        if matrix[r][c] == obstacle or matrix[r][c] == green or diag or len(com) == 0:
            alive=False
        
        # check if coordinate is valid    
        x,y = moves(com[0],r,c)[:2]
        current_pix = matrix[x][y]
        
        #this part seeems wrong we should paint the tail not the
        matrix[r,c] == gray
        if current_pix == background:
            
            matrix[x,y] = gray
            
        elif current_pix == food:
            matrix[x,y]= green
        
        r,c = x,y
        
        #check for coming out other side of image
            
            
            

def snake_hole(r,c):
    x,y = moves(com[0],r,c)[:2]
    
    if 
    
    
            
#use dictionary later
def moves(direction,r,c):
    
    
    
    if direction == 'E':
        return (r,c+1) #right 'E':(0,1)
    
    elif direction == 'W':
        return (r,c-1) #left 'W':(0,-1)
    
    elif direction == 'N':
        return (r-1,c) #up
    
    elif direction == 'S':
        return (r+1,c) #bottom
    
    elif direction == 'NW':
        return (r-1,c-1,'S','E') #up_left 
    
    elif direction == 'NE':
        return (r-1,c+1,'S','W') #up_right
    
    elif direction == 'SW':
        return (r+1,c-1,'N','E') #bottom_left
    
    elif direction == 'SE':
        return (r+1,c+1,'N','W') #bottom_right
    
    
pos = r,c
if first row:
    upleft
    len(row) - c, c[-1]
    upright
    r,c = c,r
if last row:
    bottomleft
    r,c = c,r
    bottom right
    r-c, c[0]
if first column:
    upleft
    r[-1],len(row)-r
    bottomleft
    r,c = c,r
if last column:
    upright
    r,c = c,r
    bottom right
    r[0],len(row) - r
    




    
if __name__ == '__main__':
    
    file = open('data\input_00.json').read()

    
    data = eval(file)['input']
    
    start_img = data['start_img']
    position = data['position']
    commands = data['commands']
    out_img = data['out_img']
    
    g = generate_snake(start_img, position, commands, out_img)
    print(g)
   """

    

     }
 """
 right = r,c[0]
 left = r,c[-1]
 up = r[-1],c
 bottom = r[0],c
 up_left = r[-1],c[-1]
 bottom_left = 
 """
 moving_out = {
     
     }
 
 
 
"""
{''}
h = len(row)
pos = r,c
if first row:
    upleft
    h - c, c[-1]
    upright
    r,c = c,r
if last row:
    bottomleft
    r,c = c,r
    bottom right
    r-c, c[0]
if first column:
    upleft
    r[-1],h-r
    bottomleft
    r,c = c,r
if last column:
    upright
    r,c = c,r
    bottom right
    r[0],h - r
    
    
    [
    [0,0,0,0],ur
    [0,0,0,1],
    [0,0,0,0],
    [0,0,0,0],
    ]  
    
    
    
    
    
    
"""























