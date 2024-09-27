import pygame

WIN = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Example for Loop Error')

def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                run = False
                secondary()
                #Wenn enter gedrückt wird, wird von main zu secondary (sprich zb. von menü zu spiel) gewechselt
        pygame.display.update()
    pygame.quit()

def secondary():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                run = False
                main()
                #Und dann wird bei Enter drücken wieder zurückgewechselt. Funktioniert soweit fabelhaft.
        pygame.display.update()
main()

#Wenn main() zu ende ist, wird das programm geschlossen. Wenn man auf das X klickt auch.

#Aber: Wenn man einmal zu secondary und zurück zu main gewechselt ist, bekommt man beim schließen durch x folgenden Fehler:
#pygame.error: video system not initialized
#Process finished with exit code 1


class a():
    def __init__(self):
        self.x = 7