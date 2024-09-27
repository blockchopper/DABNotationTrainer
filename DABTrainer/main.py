
import pygame
import pygame_textinput
import random
import math
from dab.board import Board
from dab.constants import *
textinput = pygame_textinput.TextInputVisualizer()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dots and Boxes Notation Trainer')
pygame.key.set_repeat(200, 25)


class Trainer():
    def __init__(self, WIN):
        self.board = Board(WIN)
        self.running = True
        self.state = 'menu'
        self.options = DEFAULT_OPTIONS
        self.clock = pygame.time.Clock()
        self.highscores = []
        self.highscoresi = []
        self.places_txt = [' 1.', ' 2.', ' 3.', ' 4.', ' 5.', ' 6.', ' 7.', ' 8.', ' 9.', '10.', '11.', '12.', '13.', '14.', '15.', '16.', '17.', '18.', '19.', '20.']
        self.btn_hor = self.board.button('horizontal moves', 50, 630)
        self.btn_ver = self.board.button('vertical moves', 50, 671)
        self.btn_dot = self.board.button('dots', 320, 630)
        self.btn_box = self.board.button('boxes', 320, 671)
        self.btn_fail = self.board.button('reset on fail', 50, 753)
        self.btn_std = self.board.button('default settings', 320, 753)
        self.btn_time = self.board.button('timer', 50, 712)
        self.btn_inv = self.board.button('inverse training', 320, 712)
        self.buttons = [self.btn_hor, self.btn_ver, self.btn_dot, self.btn_box, self.btn_fail, self.btn_std, self.btn_time, self.btn_inv]
        self.countdown_time = 10000
        self.step_time = 2000
        self.ct = self.countdown_time
        self.current_time = 0
        self.new_objective_time = pygame.time.get_ticks()
        self.x, self.y = 0,0
        self.objective = self.board.element(self.x, self.y)
        self.score=0
        self.elements = []
        for x in range(1, 12, 1):
            for y in range(1, 12, 1):
                self.elements.append(self.board.element(x, y))

    @property
    def highscores_txt(self):
        highscores_txt = ''
        for index, element in enumerate(self.highscores):
            if index < 20:
                highscores_txt = highscores_txt + f"{element[0][0:20]}\n"
        return highscores_txt

    @property
    def highscoresi_txt(self):
        highscoresi_txt = ''
        for index, element in enumerate(self.highscoresi):
            if index < 20:
                highscoresi_txt = highscoresi_txt + f"{element[0][0:20]}\n"
        return highscoresi_txt

    def load_highscores(self):
        try:
            self.highscores = []
            with open('highscores.txt', 'r') as filehandle:
                filecontents = filehandle.readlines()
                for line in filecontents:
                    e1, e2 = line.split(' / ')
                    self.highscores.append((e1, int(e2)))
        except FileNotFoundError:
            print('No previous Highscores found')
        except ValueError:
            print('Something went wrong with the highscore values bro')
        try:
            self.highscoresi = []
            with open('highscoresi.txt', 'r') as filehandle:
                filecontents = filehandle.readlines()
                for line in filecontents:
                    e1, e2 = line.split(' / ')
                    self.highscoresi.append((e1, int(e2)))
        except FileNotFoundError:
            print('No previous Highscores found')
        except ValueError:
            print('Something went wrong with the highscore values bro')

    def draw_highscores(self):
        self.board.draw_text("~ Highscores ~", (825, 25), BLACK)
        self.board.draw_text([self.highscores_txt, self.highscoresi_txt][self.options['inverse']], (700, 70), BLACK)
        self.board.draw_text(nl.join(self.places_txt[0:min(len([self.highscores,self.highscoresi][self.options['inverse']]), 20)]), (650, 70), BLACK)
        self.board.draw_text(nl.join([str(x[1]) for x in [self.highscores[0:20],self.highscoresi[0:20]][self.options['inverse']]]), (1150, 70), BLACK)

    def update_highscores(self):
        self.highscores.sort(key=lambda y: y[1], reverse=True)
        self.highscoresi.sort(key=lambda y: y[1], reverse=True)
    def write_highscores(self):
        with open('highscores.txt', 'w') as filehandle:
            filehandle.writelines(f"{x[0]} / {x[1]}\n" for x in self.highscores)
        with open('highscoresi.txt', 'w') as filehandle:
            filehandle.writelines(f"{x[0]} / {x[1]}\n" for x in self.highscoresi)

    def rng(self):
        keys = ['horizontal', 'vertical', 'dots', 'boxes']
        opt = {key: self.options[key] for key in keys}
        pool = [key for key, value in opt.items() if value]
        roll = random.choice(pool)

        if roll == 'horizontal':
            self.x = random.randrange(2, 11, 2)
            self.y = random.randrange(1, 12, 2)
        elif roll == 'vertical':
            self.x = random.randrange(1, 12, 2)
            self.y = random.randrange(2, 11, 2)
        elif roll == 'dots':
            self.x = random.randrange(1, 12, 2)
            self.y = random.randrange(1, 12, 2)
        elif roll == 'boxes':
            self.x = random.randrange(2, 11, 2)
            self.y = random.randrange(2, 11, 2)


    def new_obj(self):
        textinput.value = ''
        oldx, oldy = self.x,self.y
        while oldx == self.x and oldy == self.y:
            self.rng()
        self.objective = self.board.element(self.x, self.y)
        self.new_objective_time = pygame.time.get_ticks()

    def reset_round(self):
        self.countdown_time = 10000
        self.step_time = 2000
        self.ct = self.countdown_time
        self.current_time = 0
        self.new_obj()
        self.score = 0

    def set_buttons(self):
        self.btn_hor.selected = self.options['horizontal']
        self.btn_ver.selected = self.options['vertical']
        self.btn_dot.selected = self.options['dots']
        self.btn_box.selected = self.options['boxes']
        self.btn_fail.selected = self.options['failure']
        self.btn_time.selected = self.options['timer']
        self.btn_inv.selected = self.options['inverse']
        self.btn_std.selected = False

    def menu(self):
        self.reset_round()
        self.clock.tick(FPS)
        self.board.draw_surface()
        self.board.draw_dots()
        self.draw_highscores()
        self.board.draw_text("Press Enter to start!\n\nHighscores only available with timer and reset activated.", (650, 650),BLACK)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.state = 'game'
        if self.btn_box.selected + self.btn_dot.selected + self.btn_hor.selected + self.btn_ver.selected == 1:
            if self.btn_box.selected == True:
                self.btn_box.active = False
            if self.btn_dot.selected == True:
                self.btn_dot.active = False
            if self.btn_hor.selected == True:
                self.btn_hor.active = False
            if self.btn_ver.selected == True:
                self.btn_ver.active = False
        elif self.btn_box.selected + self.btn_dot.selected + self.btn_hor.selected + self.btn_ver.selected > 1:
            self.btn_box.active = self.btn_dot.active = self.btn_hor.active = self.btn_ver.active = True
        else:
            self.btn_hor.selected = True

        for button in self.buttons:
            button.update(events)
            if self.btn_std.selected == True:
                self.btn_std.selected = False
                self.options = DEFAULT_OPTIONS
                self.set_buttons()
            button.draw()
        self.options = {'timer': self.btn_time.selected,
                   'inverse': self.btn_inv.selected,
                   'failure': self.btn_fail.selected,
                   'horizontal': self.btn_hor.selected,
                   'vertical': self.btn_ver.selected,
                   'dots': self.btn_dot.selected,
                   'boxes': self.btn_box.selected}

        pygame.display.update()

    def game(self):
        self.clock.tick(FPS)
        self.board.draw_surface()
        self.board.draw_dots()
        events = pygame.event.get()
        textinput.update(events)
        self.draw_highscores()
        if self.options['inverse']:
            self.board.draw_text(f"{self.objective.coords}", (50, 700), BLACK)
            self.board.draw_text("Click on the board element belonging to the coordinates below!\n\n Columns: a-k, Rows: 1-11\n Starting at bottom left",(650, 650), BLACK)
            for element in self.elements:
                element.update(events)
                if element.hovered == True:
                    self.coords = element.coords
                    element.draw()
                self.board.draw_dots()
        else:
            WIN.blit(textinput.surface, (100, 700))
            self.board.draw_text(
                "Enter the coordinates belonging to the board element shown!\n\n Columns: a-k, Rows: 1-11\n Starting at bottom left",(650, 650), BLACK)

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if not self.options['inverse'] and textinput.value == chr(96 + self.x) + str(self.y):
                    self.score += 1
                elif self.options['timer']:
                    if self.options['failure']:
                        if self.score != 0:
                            self.state = 'highscore'
                            textinput.value = ''
                else:
                    if self.options['failure']:
                        self.score = 0
                self.new_obj()
                textinput.value =''
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state = 'menu'
                textinput.value = ''
            if self.options['inverse'] and event.type == pygame.MOUSEBUTTONUP:
                if self.coords == self.objective.coords:
                    self.score += 1
                elif self.options['timer']:
                    if self.options['failure']:
                        if self.score != 0:
                            self.state = 'highscore'
                            textinput.value = ''
                        else:
                            self.state = 'menu'
                            textinput.value = ''
                else:
                    if self.options['failure']:
                        self.score = 0
                self.new_obj()
            if event.type == pygame.QUIT:
                self.running = False

        if self.objective != None and not self.options['inverse']:
            self.objective.draw()
            self.board.draw_dots()

        self.current_time = pygame.time.get_ticks()
        if self.score != 0:
            self.ct = int(max(self.countdown_time - self.step_time * math.floor(math.log(self.score)), 1500-1000*self.options['inverse']))
        else:
            self.ct = self.countdown_time
        if self.options['timer']:
            if self.current_time - self.new_objective_time > self.ct:
                if self.options['failure']:
                    if self.score != 0:
                        self.state = 'highscore'
                        textinput.value = ''
                    else:
                        self.state = 'menu'
                        textinput.value = ''
                else:
                    self.new_obj()

        scoretext = myfont.render("Score = " + str(self.score), 1, (0, 0, 0))
        WIN.blit(scoretext, (400, 700))
        if self.options['timer']:
            self.board.draw_time_bar(self.ct, self.current_time - self.new_objective_time)

        pygame.display.update()

    def highscore(self):
        self.clock.tick(FPS)
        self.board.draw_surface()
        self.board.draw_dots()
        self.board.draw_text(f'Game Over!\nScore: {self.score}\nPlease enter your name.\nPress "Escape" to delete your result.',(650,650), RED)
        self.draw_highscores()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if textinput.value != '':
                    name = textinput.value
                    textinput.value = ''
                    if self.options['inverse']:
                        self.highscoresi.append((name, self.score))
                    else:
                        self.highscores.append((name, self.score))
                    self.update_highscores()
                    self.write_highscores()
                    self.state = 'menu'
                    self.reset_round()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                textinput.value = ''
                self.reset_round()
                self.state = 'menu'
        textinput.update(events)
        WIN.blit(textinput.surface, (50, 700))
        pygame.display.update()

    def run(self):
        self.set_buttons()
        while self.running:
            if self.state == 'menu':
                self.menu()
            elif self.state == 'game':
                self.game()
            elif self.state == 'highscore':
                self.highscore()
        pygame.quit()
if __name__ == '__main__':
    trainer = Trainer(WIN)
    trainer.load_highscores()
    trainer.run()
