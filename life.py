from collections import OrderedDict
import pygame,random
from pygame.locals import *

pygame.init()

speed = 10
squares = 1 #size
map_size = 32 #width, height

if squares == 0:
	imgs = ["res/alive_8.png","res/dead_8.png",8]
if squares == 1:
	imgs = ["res/alive_16.png","res/dead_16.png",16]
if squares == 2:
	imgs = ["res/alive_32.png","res/dead_32.png",32]
if squares == 3:
	imgs = ["res/alive_64.png","res/dead_64.png",64]


width = map_size * imgs[2]
height = map_size * imgs[2]
screen_size = width, height
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
alive = pygame.image.load(imgs[0]).convert()
dead = pygame.image.load(imgs[1]).convert()
done = False

class cell:
	def __init__(self, location, alive = False):
		self.to_be = None
		self.alive = alive
		self.pressed = False
		self.location = location

class board:
	def __init__(self):
		self.map = []

	def fill(self, ran):
		for i in xrange(map_size):
			self.map.append([])
			for g in xrange(map_size):
				if ran == True:
					a = random.randint(0,4)
					if a == 0: self.map[i].insert(g, cell((i,g),True))
					else:
						self.map[i].insert(g,cell((i,g)))

				else:
					self.map[i].insert(g,cell((i,g)))

	def draw(self):
		for i in xrange(map_size):
			for g in xrange(map_size):
				cell = self.map[i][g]
				loc = cell.location
				if cell.alive == True:
					screen.blit(alive, (loc[0]*imgs[2],loc[1]*imgs[2]))
				else:
					screen.blit(dead, (loc[0]*imgs[2],loc[1]*imgs[2]))

	def get_neighbors(self,cell):
		mapa = self.map
		a = []
		b = []
		c = 0
		cell_loc = cell.location
		# ew
		try: a.append(mapa[abs(cell_loc[0]-1)][abs(cell_loc[1]-1)].location)
		except Exception: pass
		try: a.append(mapa[abs(cell_loc[0])][abs(cell_loc[1]-1)].location)
		except Exception: pass
		try: a.append(mapa[abs(cell_loc[0]+1)][abs(cell_loc[1]-1)].location)
		except Exception: pass
		try: a.append(mapa[abs(cell_loc[0]-1)][abs(cell_loc[1])].location)
		except Exception: pass
		try: a.append(mapa[abs(cell_loc[0]+1)][abs(cell_loc[1])].location)
		except Exception: pass
		try: a.append(mapa[abs(cell_loc[0]-1)][abs(cell_loc[1]+1)].location)
		except Exception: pass
		try: a.append(mapa[abs(cell_loc[0])][abs(cell_loc[1]+1)].location)
		except Exception: pass
		try: a.append(mapa[abs(cell_loc[0]+1)][abs(cell_loc[1]+1)].location)
		except Exception: pass
		
		#See Conway wiki for rules
		num = len(list(OrderedDict.fromkeys(a)))# removes duplicates
		for i in xrange(len(a)): b.append(mapa[a[i][0]][a[i][1]].alive)
		for i in b:# c houses how many cells are alive around it
			if i == True: c+=1
		if cell.alive == True:# rules
			if c < 2: cell.to_be = False
			if c > 3:cell.to_be = False
		else:
			if c == 3: cell.to_be = True

	def update_frame(self):
		for i in xrange(map_size):
			for g in xrange(map_size):
				cell = self.map[i][g]
				self.get_neighbors(cell)

	def update(self):
		for i in xrange(map_size):
			for g in xrange(map_size):
				cell = self.map[i][g]
				loc = cell.location
				if cell.to_be != None: cell.alive = cell.to_be
				if self.map[i][g].alive == True:
					screen.blit(alive,(loc[0]*imgs[2],loc[1]*imgs[2]))
				else:
					screen.blit(dead,(loc[0]*imgs[2],loc[1]*imgs[2]))
				cell.to_be = None

def cell_list():
	lst = []
	for i in xrange(map_size):
		lst.append([])
		for g in xrange(map_size):
			lst[i].append((board.map[i][g].location[0]*imgs[2],board.map[i][g].location[1]*imgs[2]))
	return lst

board = board()
board.fill(False)
board.draw()
tp = 0
run = False

while done == False:
	milliseconds = clock.tick(60)
	seconds = milliseconds / 1000.0
	tp += milliseconds

	for event in pygame.event.get():
		if event.type == QUIT:
			done = True
		if event.type == KEYDOWN:
			if event.key == K_SPACE:
				run = not run

		if event.type == KEYUP:
			if event.key == K_q:
				run = False
				board.update_frame()
				board.update()
			if event.key == K_r:
				board.map = []
				board.fill(False)
				board.draw()
			if event.key == K_a:
				board.map = []
				board.fill(True)
				board.draw()
		if event.type == MOUSEBUTTONUP:
			for i in xrange(map_size):
				for g in xrange(map_size):
					board.map[i][g].pressed = False

	mouse = pygame.mouse.get_pressed()
	pos = pygame.mouse.get_pos()

	if run == True and tp >= 1000/speed:
		print("run")
		tp = 0
		board.update_frame()
		board.update()

	if mouse[0]:
		rects = cell_list()
		for i in xrange(map_size):
			for g in xrange(map_size):
				if pos[0] >= rects[i][g][0] and pos[0] < rects[i][g][0]+imgs[2] and pos[1] >= rects[i][g][1] and pos[1] < rects[i][g][1]+imgs[2] and board.map[i][g].pressed == False:
					board.map[i][g].alive = True
					board.map[i][g].pressed = True
					board.update()
	if mouse[2]:
		rects = cell_list()
		for i in xrange(map_size):
			for g in xrange(map_size):
				if pos[0] >= rects[i][g][0] and pos[0] < rects[i][g][0]+imgs[2] and pos[1] >= rects[i][g][1] and pos[1] < rects[i][g][1]+imgs[2] and board.map[i][g].pressed == False:
					board.map[i][g].alive = False
					board.map[i][g].pressed = False
					board.update()
	pygame.display.flip()
pygame.quit()

