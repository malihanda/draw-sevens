import cv2
import math
import numpy as np
import random
import datetime

now = str(datetime.datetime.now()).split(".")[0].replace(" ", "-").replace(":", "-")
FILE_PATH = "im" + now + ".png"
ROWS = 24       # 24 or 13 works best
M = 20          # Space around the outside of the image
SPACER = 20     # Space in between two puzzles
SIZE = 20       # Size of one CELL
BORDER = 10     # Space outlining one puzzle
GRID_LINE = 3   # Width of the grid lines
PUZZLE_SIZE = (BORDER * 2) + (SIZE * 7) + ((7 - 1) * GRID_LINE)

WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
GREY = [200, 200, 200] # Color of the background
# BORDER_COLOR = [100, 100, 100]

# WHITE = [231, 232, 172]
# BLACK = [138, 44, 135]
# GREY = [85, 207, 200]
BORDER_COLOR = [77, 25, 75]


def read_puzzles():
    with open("sevens.txt", "r") as f:
        puzzles = []
        for line in f.readlines():
            puzzles.append(line.strip())
    return puzzles


def draw_block(color):
    block = np.zeros((SIZE, SIZE, 3), dtype=np.uint)
    block[:, :] = color
    return block


def draw_puzzle(p):
    colors = np.zeros((PUZZLE_SIZE, PUZZLE_SIZE, 3), dtype=np.uint8)
    colors[:, :] = BORDER_COLOR
    rows = p.split(" ")
    for i, row in enumerate(rows):
        for j in range(len(row)):
            c = WHITE if row[j] == "0" else BLACK
            block = draw_block(c)
            r_start = BORDER + (SIZE * j) + (j * GRID_LINE)
            r_stop = r_start + SIZE
            c_start = BORDER + (SIZE * i) + (i * GRID_LINE)
            c_stop = c_start + SIZE
            colors[r_start:r_stop, c_start:c_stop] = block
    return colors


def draw_puzzles(puzzles):
    cols = math.ceil(len(puzzles) / ROWS)

    # Make the array.
    width = (M * 2) + (PUZZLE_SIZE * cols) + ((cols - 1) * SPACER)
    height = (M * 2) + (PUZZLE_SIZE * ROWS) + ((ROWS - 1) * SPACER)
    pic = np.zeros((width, height, 3), dtype=np.uint8)
    pic[:, :] = GREY

    # Fill in the puzzles
    count = 0
    for i in range(ROWS):
        for j in range(cols):
            try:
                p = puzzles[count]
            except:
                continue
            puzzle_colors = draw_puzzle(p)
            r_start = M + (PUZZLE_SIZE * j) + (j * SPACER)
            r_stop = r_start + PUZZLE_SIZE
            c_start = M + (PUZZLE_SIZE * i) + (i * SPACER)
            c_stop = c_start + PUZZLE_SIZE
            pic[r_start:r_stop, c_start:c_stop] = puzzle_colors
            count += 1

    cv2.imwrite(FILE_PATH, pic)


puzzles = read_puzzles()
# random.shuffle(puzzles)
ps = sorted(puzzles, reverse=True)
draw_puzzles(ps)



