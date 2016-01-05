#!/usr/bin/env python
# Grid is on an x,y axis with 0,0 being in the top left corner
# this pattern imitates John Conways game of life.
# each cell (iving or dead) lives of a set of 3 basic rules
# 1. Any live cell with fewer than two live neighbors dies
# 2. Any live vell with two or three live neighbors lives on to the next generation
# 3. Any live cell with more than three live nieghbors dies
# 4. Any dead cell with exactly three live neighbors become a live cell

import opc, time, random, sys

h = 256
client=opc.Client('localhost:7890')

xs = {x: list() for x in range(16)}
ys = {y: list() for y in range(16)}
pixels = {}

def grid(start,x0,y0):
    for i in xrange(start,start+64):
        p = i-start
        x = x0 + p%8
        y = y0 + int(p/8)
        xs[x].append(i)
        ys[y].append(i)
        pixels[i] = (x,y)

grid(256+0*64,0,0)
grid(256+1*64,8,0)
grid(256+2*64,0,8)
grid(256+3*64,8,8)

print pixels

gameboard = [[0 for j in range(16)] for i in range(16)]
temp_g_board = [[0 for j in range(16)] for i in range(16)]

def output(render):
    render = [(c*.4 for c in cs) for cs in render]
    client.put_pixels(render)

render = [(0,0,0) for _ in range(512)]

random_placement = [random.randrange(256,512) for i in range(75)]

# set the default pixels

print random_placement
"""
for k, (x,y) in pixels.items():
	if k in random_placement:
		render[k] = (0,150,0)
		gameboard[x][y] = 1
"""
def vertical_bar_pattern():
	for k, (x,y) in pixels.items():
		if y == 7 or y == 8:
			render[k] = (0,150,0)
			gameboard[x][y] = 1
	print gameboard

def glider_pattern():
	for k, (x,y) in pixels.items():
		if x==1 and y==1 or x==0 and y==2 or x==2 and y==1 or x==2 and y==2 or x==1 and y==0:
			render[k] = (0,150,0)
			gameboard[x][y] = 1
glider_pattern()
#vertical_bar_pattern()
client.put_pixels(render)
time.sleep(1)

def top_border_check(x,y):
    flag = 0;
    for xx,yy in [(x-1,15),(x+1,15),(x,15),(x,y+1),(x+1,y+1),(x-1,y+1),(x-1,y),(x+1,y)]:
        if gameboard[xx][yy] == 1:
            flag = flag + 1
    return flag

def right_border_check(x,y):
    flag = 0;
    for xx,yy in [(0,y),(0,y-1),(0,y+1),(x-1,y),(x-1,y+1),(x-1,y-1),(x,y+1),(x,y-1)]:
        if gameboard[xx][yy] == 1:
            flag = flag + 1
    return flag

def bottom_border_check(x,y):
    flag = 0;
    for xx,yy in [(x,0),(x+1,0),(x-1,0),(x,y-1),(x-1,y-1),(x+1,y-1),(x-1,y),(x+1,y)]:
        if gameboard[xx][yy] == 1:
            flag = flag + 1
    return flag

def left_border_check(x,y):
    flag = 0;
    for xx,yy in [(15,y),(15,y+1),(15,y-1),(x+1,y),(x+1,y-1),(x,y+1),(x+1,y+1),(x,y-1)]:
        if gameboard[xx][yy] == 1:
            flag = flag + 1
    return flag

def top_left_corner_check(x,y):
    flag = 0;
    for xx,yy in [(x,y+1),(x+1,y+1),(x+1,y),(15,y+1),(15,y),(15,15),(x,15),(x+1,15)]:
        if gameboard[xx][yy] == 1:
            flag = flag + 1
    return flag

def bottom_left_corner_check(x,y):
    flag = 0;
    for xx,yy in [(x,y-1),(x+1,y-1),(x+1,y),(15,y-1),(15,y),(15,0),(0,0),(x+1,0)]:
        if gameboard[xx][yy] == 1:
            flag = flag + 1
    return flag

def top_right_corner_check(x,y):
    flag = 0;
    for xx,yy in [(x-1,y),(x-1,y+1),(x,y+1),(x,15),(0,15),(x,0),(0,y+1),(x-1,15)]:
        if gameboard[xx][yy] == 1:
            flag = flag + 1
    return flag

def bottom_right_corner_check(x,y):
    flag = 0;
    for xx,yy in [(x,y-1),(x-1,y),(x-1,y-1),(0,y-1),(0,y),(0,0),(x,0),(x-1,0)]:
        if gameboard[xx][yy] == 1:
            flag = flag + 1
    return flag

def check_neighbors(x,y):
    	flag = 0
    	for xx, yy in [(x,y-1), (x+1,y-1), (x+1,y+1), (x+1,y), (x,y+1), (x-1,y+1), (x-1,y), (x-1,y-1)]:
		if gameboard[xx][yy] == 1:
			flag = flag + 1
	return flag

total = 0
lik = 0
for c in range(300):
	cellCountCheck = 0
	# check each creature on the grid
	for z, (x,y) in pixels.items():
		if gameboard[x][y] == 1:
			flag = 0
			# check if top border
			if y == 0 and (x >=1 and x <= 14):
				flag = top_border_check(x,y)
			# check if right border
			elif x == 15 and (y >=1 and y <= 14):
				flag = right_border_check(x,y)
			# check if bottom border
			elif y == 15 and (x >= 1 and x <= 14):
				flag = bottom_border_check(x,y)
			# check if left border
			elif x == 0 and (y >= 1 and y <= 14):
				flag = left_border_check(x,y)
			# check corners
			elif x == 0 and y == 0:
				flag = top_left_corner_check(x,y)
			elif x == 15 and y == 15:
				flag = bottom_right_corner_check(x,y)
			elif x == 0 and y == 15:
				flag = bottom_left_corner_check(x,y)
			elif x == 15 and y == 0:
				flag = top_right_corner_check(x,y)
			else:
				flag = check_neighbors(x,y)

			if flag >=2 and flag <= 3:
				temp_g_board[x][y] = 1
			else:
				temp_g_board[x][y] = 0
		# birth check
		else:
			flag = 0
			#check if top border
			if y == 0 and (x >=1 and x <= 14):
				flag = top_border_check(x,y)
			#check if right border
			elif x == 15 and (y >=1 and y <= 14):
				flag = right_border_check(x,y)
			#check if bottom border
			elif y == 15 and (x >= 1 and x <= 14):
				flag = bottom_border_check(x,y)
			#check if left border
			elif x == 0 and (y >= 1 and y <= 14):
				flag = left_border_check(x,y)
			#check corners
			elif x == 0 and y == 0:
				flag = top_left_corner_check(x,y)
			elif x == 15 and y == 15:
				flag = bottom_right_corner_check(x,y)
			elif x == 0 and y == 15:
				flag = bottom_left_corner_check(x,y)
			elif x == 15 and y == 0:
				flag = top_right_corner_check(x,y)
			else:
				flag = check_neighbors(x,y)

			if flag >=3 and flag <= 3:
				temp_g_board[x][y] = 1
			else:
				temp_g_board[x][y] = 0
	# assign the temp game board to the actual game board
	# modify the corresponding lights on the board
	color = random.randrange(0,150)
	for p, (xxx,yyy) in pixels.items():
		gameboard[xxx][yyy] = temp_g_board[xxx][yyy]
		if gameboard[xxx][yyy] == 1:
			render[p] = (0,150,0)
			cellCountCheck = cellCountCheck + 1
		else:
			render[p] = (0,0,0)
	"""
	# check of the grid has a continuos pattern
	if total == cellCountCheck:
		lik = lik + 1
	else:
		total = cellCountCheck
	if lik > 15:
		import sys
		sys.exit()
	"""
	client.put_pixels(render)
	time.sleep(0.1)
	for i in range(16):
		for k in range(16):
			temp_g_board[i][k] = 0
sys.exit()

