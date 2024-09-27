import pygame

WIDTH, HEIGHT = 1200, 800

ROWS, COLS = 5,5

BORDER_WIDTH = 10
BOARD_SIZE = 600

FPS = 60

DEFAULT_OPTIONS = {'timer' : True, 'inverse' : False, 'failure' : True, 'horizontal' : True, 'vertical' : True, 'dots' : False, 'boxes' : False}

myfont = pygame.font.Font(pygame.font.get_default_font(),25)
nl = '\n'

#rgb
CLR_BORDER = (194, 148, 79)
CLR_BACK = (243,194,128)
CLR_PASSIVE = (102, 85, 68)
CLR_DOTS = (51,34,17)
RED = (255, 0, 0)
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
LIGHT_BLUE = (179, 217, 255)
CLR_SELECTED = (255, 128, 0)