import pygame
from .constants import *

class Board:
    def __init__(self, win):
        self.board = []
        self.win = win

    def draw_surface(self):
        self.win.fill(LIGHT_BLUE)

        pygame.draw.line(self.win, BLACK, (BOARD_SIZE+2*BORDER_WIDTH-4,0), (BOARD_SIZE+2*BORDER_WIDTH-4, HEIGHT), BORDER_WIDTH+2)
        pygame.draw.line(self.win, BLACK, (0, BOARD_SIZE+2*BORDER_WIDTH-4), (WIDTH, BOARD_SIZE+2*BORDER_WIDTH-4), BORDER_WIDTH+2)
        pygame.draw.line(self.win, BLACK, (BORDER_WIDTH/2,BORDER_WIDTH/2), (BORDER_WIDTH/2,HEIGHT), BORDER_WIDTH+1)
        pygame.draw.line(self.win, BLACK, (BORDER_WIDTH/2, BORDER_WIDTH/2), (WIDTH, BORDER_WIDTH/2), BORDER_WIDTH+1)

        pygame.draw.rect(self.win, BLACK, (0, 0, BOARD_SIZE+2*BORDER_WIDTH+3,BOARD_SIZE+2*BORDER_WIDTH+3))
        pygame.draw.rect(self.win, CLR_BORDER, (0,0, BOARD_SIZE+2*BORDER_WIDTH+2,BOARD_SIZE+2*BORDER_WIDTH+2))
        pygame.draw.rect(self.win, BLACK, (BORDER_WIDTH, BORDER_WIDTH, BOARD_SIZE+2, BOARD_SIZE+2))
        pygame.draw.rect(self.win, CLR_BACK, (BORDER_WIDTH+1, BORDER_WIDTH+1, BOARD_SIZE, BOARD_SIZE))

        pygame.draw.line(self.win, CLR_BORDER, (BORDER_WIDTH/2-1,BORDER_WIDTH/2-1), (BORDER_WIDTH/2-1,HEIGHT), BORDER_WIDTH)
        pygame.draw.line(self.win, CLR_BORDER, (BORDER_WIDTH/2-1, BORDER_WIDTH/2-1), (WIDTH, BORDER_WIDTH/2-1), BORDER_WIDTH)
        pygame.draw.line(self.win, CLR_BORDER, (BOARD_SIZE+2*BORDER_WIDTH-4, 0), (BOARD_SIZE+2*BORDER_WIDTH-4, HEIGHT), BORDER_WIDTH)
        pygame.draw.line(self.win, CLR_BORDER, (0, BOARD_SIZE+2*BORDER_WIDTH-4), (WIDTH, BOARD_SIZE+2*BORDER_WIDTH-4), BORDER_WIDTH)

    def draw_dots(self):
        for row in range(ROWS+1):
            for col in range(COLS+1):
                pygame.draw.circle(self.win, CLR_DOTS, (BOARD_SIZE/(ROWS+1)/2 + BORDER_WIDTH+1+row*BOARD_SIZE/(ROWS+1), BOARD_SIZE/(COLS+1)/2 + BORDER_WIDTH+1+col*BOARD_SIZE/(COLS+1)), BOARD_SIZE/((COLS+1)*10))

    def draw_time_bar(self, reset_time, elapsed_time):
        pygame.draw.rect(self.win, BLACK,(49, 640,503,22))
        pygame.draw.line(self.win, GREEN, (550,650),(50,650), 20)
        pygame.draw.line(self.win, RED, (550,650), (550-elapsed_time/reset_time*500,650),20)

    def clear(self):
        pygame.draw.rect(self.win, CLR_BACK, (BORDER_WIDTH+1, BORDER_WIDTH+1, BOARD_SIZE, BOARD_SIZE))
        self.draw_dots()

    def draw_text(self,  text, pos, clr):
        '''
        text_surface = font.render(text, True, BLACK)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.win.blit(text_surface, text_rect)
        '''
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = myfont.size(' ')[0]  # The width of a space.
        max_width, max_height = self.win.get_size()
        x,y = pos
        for line in words:
            for word in line:
                word_surface = myfont.render(word, True, clr)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                self.win.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.

    def element(self, x, y):
        return Element(x,y, self.win)

    def button(self, text, x, y):
        return (Button(text, x, y, self.win))



class Element():
    def __init__(self, x, y, win):
        self.x = x
        self.y = 12 - y
        self.coords = chr(96+x)+str(y)
        self.win = win
        self.hovered = False
        self.highlighted = False
        self.hitbox = pygame.Rect(
            BORDER_WIDTH + 1 + BOARD_SIZE / (COLS + 1) / 2 + (self.x - 2) / 2 * BOARD_SIZE / (COLS + 1) + 25,
            BORDER_WIDTH + 1 + BOARD_SIZE / (ROWS + 1) / 2 + (self.y - 2) / 2 * BOARD_SIZE / (ROWS + 1) + 25,
            BOARD_SIZE / (COLS + 1) - 50,
            BOARD_SIZE / (ROWS + 1) - 50)
        if x%2:
            if y%2:
                self.type = "dot"
            else:
                self.type = "line"
        elif y%2:
            self.type = "line"
        else:
            self.type = "box"


    def draw(self):
        if self.type == "box":
            pygame.draw.rect(self.win, [CLR_PASSIVE,RED][self.highlighted], (BORDER_WIDTH+1 + BOARD_SIZE/(COLS+1)/2 + (self.x-2)/2 * BOARD_SIZE/(COLS+1),
                                                                        BORDER_WIDTH+1 + BOARD_SIZE/(ROWS+1)/2 + (self.y-2)/2 * BOARD_SIZE/(ROWS+1),
                                                                        BOARD_SIZE/(COLS+1),
                                                                        BOARD_SIZE/(ROWS+1)))

        elif self.type == "line":
            pygame.draw.line(self.win, [CLR_PASSIVE,RED][self.highlighted],
                             (BORDER_WIDTH+1 + BOARD_SIZE/(COLS+1)/2 + (self.x-1-(1-self.x%2))/2 * BOARD_SIZE/(COLS+1), BORDER_WIDTH+1 + BOARD_SIZE/(ROWS+1)/2 + (self.y-1-(1-self.y%2))/2 * BOARD_SIZE/(ROWS+1)),
                             (BORDER_WIDTH+1 + BOARD_SIZE/(COLS+1)/2 + (self.x-1+(1-self.x%2))/2 * BOARD_SIZE/(COLS+1), BORDER_WIDTH+1 + BOARD_SIZE/(ROWS+1)/2 + (self.y-1+(1-self.y%2))/2 * BOARD_SIZE/(ROWS+1))
                             , 10)
        elif self.type == "dot":
            pygame.draw.circle(self.win, [CLR_PASSIVE,RED][self.highlighted], (BOARD_SIZE/(ROWS+1)/2 + BORDER_WIDTH+1+(self.x-1)/2*BOARD_SIZE/(ROWS+1), BOARD_SIZE/(COLS+1)/2 + BORDER_WIDTH+1+(self.y-1)/2*BOARD_SIZE/(COLS+1)), BOARD_SIZE/((COLS+1)*5))

    def update(self, event_list):
        pos = pygame.mouse.get_pos()
        for event in event_list:
            if self.hitbox.collidepoint(pos):
                self.hovered = True
                if pygame.mouse.get_pressed()[0]:
                    self.highlighted = True
                else: self.highlighted = False
            else:
                self.highlighted = False
                self.hovered = False

class Button():
    def __init__(self, text, x, y, win):
        self.selected = False
        self.hovered = False
        self.font = myfont
        self.text = text
        self.surface = win
        self.minwidth = 250

        self.active = True

        self.text_surface = self.font.render(self.text, True, BLACK)
        self.text_rect = self.text_surface.get_rect()
        self.text_width = self.text_rect.width
        self.text_rect = pygame.Rect(x+7, y+7, max(self.text_rect.width, self.minwidth), self.text_rect.height)

        self.text_rect.x = max(x+7, x+7+(self.text_rect.width-self.text_width)/2)

        self.button_rect = pygame.Rect(x+5, y+5, self.text_rect.width+4, self.text_rect.height+4)

        self.border_rect = pygame.Rect(x, y, self.button_rect.width+10, self.button_rect.height+10)


    def update(self, event_list):
        pos = pygame.mouse.get_pos()
        for event in event_list:
            if self.border_rect.collidepoint(pos):
                self.hovered = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.press()
            else:
                self.hovered = False

    def press(self):
        if self.active == True:
            if self.selected == False:
                self.selected = True
            elif self.selected == True:
                self.selected = False

    def draw(self):
        if self.selected == True:
            clr_button = CLR_SELECTED
        elif self.selected == False:
            clr_button = CLR_BACK
        if self.hovered == True:
            clr_border = BLACK
        elif self.hovered == False:
            clr_border = CLR_PASSIVE

        pygame.draw.rect(self.surface, clr_border, self.border_rect)
        pygame.draw.rect(self.surface, clr_button, self.button_rect)
        self.surface.blit(self.text_surface, self.text_rect)





