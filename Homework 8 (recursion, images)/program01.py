#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#landlord inherits a land
#land is rectangular
#patch of land is represented as list of lists
#if one wants to leese the land, the land must be devided into 4 other paches
#in case she does not leese, there will not be other paches 
#(devided paches) private properties should be colored 
#leesed land also can be leased again
#bg color is unknown but it will not be used to mark leesed land
#subdevison stops when all landlords stop subdevising
#smallest possible rectangular patch side is 2
# all the boundries should be traced so that program can build out image size of 1x(N+1)
## first pixel of the img is bg
##then it includes all hirarchy of colors used for subdiving the paches
##hirarchy is defined first visiting in depth to corners
##colors should be stored in reverse order wrt visiting mode
##


"""
A real estate owner in California, Lida,  inherits a piece of land. The
land is modeled as a rectangular patch of variable size. The patch of
land is represented with an image (list of lists).

To make some money out of it, she can decide to lease the land to
other people. To do that, she may decide to divide the land into four
other patches. In case she decides to not lease the land, no further
sub-patches are created. On the contrary, in case the land is divided
into four sub-patches, some colored marks (straight lines) on the land
are drawn with a thickness of one pixel to mark the private properties
that are created. There is no prior knowledge of how and where the
lines will be drawn, nor which colors will be used (there is no
regular pattern).  The only knowledge is that the lines are
axis-aligned.

The four lessees that receive the sub-patches of land may take the
same decision that Lida took before them. They may decide to sublease
once again their small patch to others or, else, to keep the land all
for themselves. The decision for each lessee is independent of each
other. For example, lessee #1 may decide to sublease again, while
lessee #2 may keep the land for himself, etc, whereas lessee #3 and #4
may subdivide. If they sublease and divide, they follow the same
policy of dividing in four parts and setting their boundaries with
line drawing but obviously with a different splitting position of
their land. For sure, they will be using a color that is different
from the colors used by Lida yet they will be using the same color
among them, at the same level of splitting.

NOTE: An important note is that the color of the background (bg) of
the land is not given (i.e. we do not know if the bg is black, or
white or blue etc) but we do know that the background land color is
NOT used by any of the lessees ever to mark their boundaries.

The subdivision process could continue until when all the lessees in
all patches stop subdividing their land. This process described here
leads us to the image that is taken as input to a program.

NOTE: You can assume that the smallest possible rectangular patch has
the shortest side of two pixels in length.

Think well about the problem and once you are sure of a solution,
design on the paper (this "design" needs be then described into the
pseudo code part) and then implement a program ex1(input_file,
output_file) which:
  - reads the file indicated by the parameter 'input_file'
    using the 'images' library 
  - preprocesses the image--if needed--and implements a
    *recursive* function to solve the requirements below.
  - counts all the patches of lands that are in the image and returns
    the number of patches. It should return the number of rectangles
    with the color of the background that is present in the
    image. Regarding the simplified case below:

        # +++++++++++++++++++
        # +-1-|-2-|---------+
        # ++++a+++|----5----+
        # +-3-|-4-|---------+
        # ++++++++b++++++++++
        # +-------|--7-|-8--+
        # +---6---|++++c+++++
        # +-------|-10-|-9--+
        # +++++++++++++++++++
  
    the approach should return 10 as the total number of patches. (The
    numbers in the simplified case above are just added for the sake
    of clarity. The image data does not contain those numbers,
    obviously).
  - finally, given that the real estate registry needs to book-keep
    all the boundaries created, the program shall build an output
    image of the size of 1x(N+1). The image encodes as the first pixel
    the color of the background. Then it should encode "the color
    hierarchy" of all the N colors used to subdivide the patches of
    land. The hierarchy is defined by "visiting" first in depth the
    upper left patch, then upper right patch, then lower left, and
    lower right. The colors should be stored in reverse order with
    respect to the "visit" made. With reference to the previous
    semplified case, assuming a boundary color is described with a
    letter, the output image should contain:
             out_colors = bg b c a


    Another case a bit more complex:

         +++++++++++++++++++++++++++++++++++++
         +-1-|-2-|---------|--------|--------+
         ++++a+++|----5----|---6----|----7---+
         +-3-|-4-|---------|--------|--------+
         ++++++++b+++++++++|++++++++c+++++++++
         +-------|--9-|-10-|--------|--------+
         +--8----|++++d++++|---13---|---14---+
         +-------|-11-|-12-|--------|--------+
         ++++++++++++++++++e++++++++++++++++++
         +-15|-16|---------|--------|-21|-22-+
         ++++f+++|---19----|---20---|+++g+++++
         +-17|-18|---------|--------|-23|--24+
         ++++++++h+++++++++|++++++++l+++++++++
         +-------|-26-|-27-|--------|-31-|-32+
         +--25---|++++m++++|---30---|+++n+++++
         +-------|-29-|-28-|--------|-33-|-34+
         +++++++++++++++++++++++++++++++++++++

         n_rect is: 34
         the color hierarchy is:
         bg e l n g h m f c b d a
 
NOTE: it is forbidden to import/use other libraries or open files
      except the one indicated

NOTE: The test system recognizes recursion ONLY if the recursive
      function/method is defined in the outermost level.  DO NOT
      define the recursive function within another function/method
      otherwise, you will fail all the tests.
"""

import images

def main_color(img, cor):
    x0, y0, x1, y1 = cor
    length = x1 - x0

    bg = img[0][0]
    lst = []
    cor = []
    for r in range(y0, y1):
        if img[x0][r] != bg and img[x0][r] not in lst:
            lst.append(img[x0][r])
            cor.append((x0, r))

    if not (cor):
        return []

    for el in cor:
        i, j = el
        count = 0
        while count < length and img[i][j] == img[i + count][j]:

            if length == count + 1:
                C = (i, j)
                break
            count += 1

    a, b = C
    n = 0
    for i in range(length):
        if img[a][b] == img[a + i][b - 1]:
            cross = (a + i, b)

    x2, y2 = cross

    all_new = [(x2 + 1, y2 + 1, x1, y1), (x2 + 1, y0, x1, y2 - 1), (x0, y2 + 1, x2 - 1, y1),
               (x0, y0, x2 - 1, y2 - 1)]
    return all_new


def rec(img, cor, count=0, lst=[]):
    if cor == []:
        return count + 1, lst

    for item in cor:
        new_cor = main_color(img, item)

        if new_cor != []:
            x, y = new_cor[0][:2]
            lst.append(img[x - 1][y - 1])

        count, lst = rec(img, new_cor, count, lst)

    return count, lst


def ex1(input_file, output_file):
    # write your code here
    img = images.load(input_file)

    B = main_color(img, (0, 0, len(img) - 1, len(img[0]) - 1))
    if B != []:

        x, y = B[0][:2]
        a = [img[x - 1][y - 1]]
    else:
        a = []
    patches, colors = rec(img, B)
    colors = [img[0][0]] + a + colors

    images.save([colors], output_file)

    return patches
    

