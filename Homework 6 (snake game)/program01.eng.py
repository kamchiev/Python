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

import images


def generate_snake(start_img: str, position: list[int, int],
                   commands: str, out_img: str) -> int:
    colors = [(0, 0, 0), (255, 0, 0), (255, 128, 0), (0, 255, 0), (128, 128, 128)]
    background, obstacle, food, snake, trace = colors
    moves = {'E': (0, 1), 'W': (0, -1), 'N': (-1, 0), 'S': (1, 0),
             'NW': (-1, -1, 1, 1), 'NE': (-1, 1, -1, 1), 'SW': (1, -1, 1, -1), 'SE': (1, 1, -1, -1)}

    img = images.load(start_img)
    com = commands.split()

    c, r = position
    height, width = len(img), len(img[0])
    path = [(r, c)]

    for direction in com:
        x, y = moves[direction][:2]
        r += x
        c += y
        r, c = legit_move(r, c, height, width)

        try:
            if len(direction) == 2:
                i, j = moves[direction][2:]
                if img[r][c + i] == snake and img[r + j][c] == snake:
                    break
        except:
            pass

        if img[r][c] == background or img[r][c] == trace:
            x1, y1 = path.pop(0)
            img[x1][y1] = trace
            img[r][c] = snake
            path.append((r, c))

        elif img[r][c] == food:
            img[r][c] = snake
            path.append((r, c))
        else:
            break

    images.save(img, out_img)

    return len(path)


def legit_move(row, col, height, width):
    if row > height - 1:
        row = 0
    elif row < 0:
        row = height - 1
    if col > width - 1:
        col = 0
    elif col < 0:
        col = width - 1

    return (row, col)
