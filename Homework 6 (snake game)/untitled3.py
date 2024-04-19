# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 10:36:36 2022

@author: khayo
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# info
# save snake's final path
# snake increase its size to 1 pixel if it eats a food
# if snake crosses one side of the image, it appers from the other side of it
# snake can move side to side horizontally, vertically and even diagonally


# background, food, obstacle are given as black, orange and red respectively
# initially we are given image, position of snake, commands
#
# what we need to do
# return the length of snake
# return the path of snake as saved in out_img

# game is over if :
# we are out of commands
# snake hits the obstacle
# snake hits itself and even it crosses itself diagonally

# Note
# get colors from image
# do not import any library except images

# solution
# get


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

NE NE NE NE S NW SW NE NE S SE 

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

# define the colors
# load image
# import commands

# check if the move is legal (if out of the border do sth )
# - red
# - itself
# - dioganal crossing
# keep track of the tail change it when it is necessary
#


import images


def generate_snake(start_img: str, position: list[int, int],
                   commands: str, out_img: str) -> int:
    colors = [(0, 0, 0), (255, 0, 0), (255, 128, 0), (0, 255, 0), (128, 128, 128)]
    background, obstacle, food, snake, trace = colors

    moves = {
        'E': (0, 1), 'W': (0, -1), 'N': (-1, 0), 'S': (1, 0),
        'NW': (-1, -1, 'S', 'E'), 'NE': (-1, 1, 'S', 'W'), 'SW': (1, -1, 'N', 'E'), 'SE': (1, 1, 'N', 'W')}

    matrix = images.load(start_img)  # image
    com = commands.split()  # make commands list
    
    corners = ('NW', 'NE', 'SW', 'SE')

    r = position[1]
    c = position[0]
    

    path = [(r, c)]

    for direction in com:
        
        
        
        x = moves[direction][0]
        y = moves[direction][1]
        r += x
        c += y

        #r,c = is_legit(r, c, len(matrix), len(matrix[0]))        
        
        if direction in corners:
            d1, d2 = moves[direction][2:]
            a1,b1 = moves[d1]
            a2,b2 = moves[d2]
            
            
            
            if matrix[a1][b1] == snake and matrix[a2][b2] == snake:
                print(1)
                break

        
       
        preciding_point = matrix[r][c]

                
       
        if preciding_point == snake:
            break


        elif preciding_point == food:
            matrix[r][c] = snake
            


        elif preciding_point != food:

            m, n = path.pop(0)
            matrix[m][n] = trace
            matrix[r][c] = snake
        if preciding_point == obstacle:
           break

        path.append((r,c))
    print(path)
    print(r,c)
    return matrix




def is_legit(r,c,height,width):
    if not (0 <= r <= height - 1) or not (0 <= c <= width - 1):
        if r > height:
            r = 0
        elif r < 0:
            r = -1
        elif c > width:
            c = 0
        elif c < 0:
            c = -1
    return (r,c)
    


if __name__ == '__main__':
    file = open('data\input_10.json').read()

    data = eval(file)['input']

    start_img = data['start_img']
    position = data['position']
    commands = data['commands']
    out_img = data['out_img']
    

    g = generate_snake(start_img, position, commands, out_img)
    images.save(g, 'img1.png')

