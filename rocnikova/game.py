import pygame
import os
pygame.init()

screen = pygame.display.set_mode((998, 598))
pygame.display.set_caption("Game")
character_width,character_height=120,120

menuBG=pygame.image.load(os.path.join("d:\Moje dokumenty\škola\Inf\pythonProjec\Rocnikova\Background.png"))
BG1=pygame.image.load(os.path.join("d:\Moje dokumenty\škola\Inf\pythonProjec\Rocnikova\Background2.png"))

girl_image=pygame.image.load(os.path.join("d:\Moje dokumenty\škola\Inf\pythonProjec\Rocnikova\Girl.png"))
girl_image=pygame.transform.scale(girl_image,(character_width,character_height))

boy_image=pygame.image.load(os.path.join("d:\Moje dokumenty\škola\Inf\Rocnikova\Boy.png"))
boy_image=pygame.transform.scale(boy_image,(character_width,character_height))

portal=pygame.image.load(os.path.join("d:\Moje dokumenty\škola\Inf\Rocnikova\Portal.png"))


Speed=70
lBlue=(204,255,255)
black=(0,0,0)
white=(255,255,255)

width,height= 30,450
vel=5

font = pygame.font.SysFont('Georgia',30, bold=True)
font2 = pygame.font.SysFont('Georgia',20, bold=True)


class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False
        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }
#def counter():
    #run = True
    #while run:
        #for event in pygame.event.get():
            #if event.type == win:
                #if keys_pressed[pygame.K_d] and portal:


#def girl_movement(keys_pressed, girl):
    #clock = pygame.time.Clock()
    #girl=pygame.Rect(30,450,120,120)
    #if keys_pressed[pygame.K_RIGHT]:  # and girl.x+vel+girl.width<990:
        #girl.x += vel
    #if keys_pressed[pygame.K_LEFT]:  # and girl.x-vel>10:
        #girl.x -= vel
    #if keys_pressed[pygame.K_SPACE]:
        #girl.y -= vel
    #run = True
    #while run:
        #clock.tick(Speed)
        #for event in pygame.event.get():
            #if event.type == pygame.QUIT:
                #run = False

            #screen.blit(girl_image,(girl.x,girl.y))

        #pygame.display.flip()
        #pygame.display.update()


def options():
    pygame.display.set_caption("Options")
    screen.fill((255, 255, 255))
    line1 = font2.render('Na pohybovanie používaš tlačítka <-  ->', True, black)
    line2 = font2.render('Skáčeš pomocou medzerníku.', True, black)
    line3 = font2.render('Tvojou úlohou je vyhnúť sa prekážkam a dostať sa do portalu,ktory otvoris pomocou klavesy D.',
                         True, black)

    screen.blit(line1, (12, 120))
    screen.blit(line2, (12, 150))
    screen.blit(line3, (12, 180))
    buttonBACK = font.render('BACK', True, black, lBlue)
    Backbutton = pygame.Rect(10, 10, 120, 50)

    screen.blit(buttonBACK, Backbutton)


    line4 = font2.render('Vyber si charakter.', True, black)

    screen.blit(line4,(12, 210))


    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Backbutton.collidepoint(event.pos):
                    back()

        pygame.display.flip()
        pygame.display.update()


def start():
    clock = pygame.time.Clock()
    pygame.display.set_caption("Game")
    screen.blit(BG1, (0, 0))

    buttonBACK = font.render('BACK', True, black, lBlue)
    Backbutton = pygame.Rect(10, 10, 120, 50)

    screen.blit(buttonBACK, Backbutton)

    girl = pygame.Rect(30, 350, character_width, character_height)
    screen.blit(girl_image, (girl.x, girl.y))
    #boy
    #level_counter = font.render('Level ', True, black)
    #level = pygame.Rect(580, 10, 120, 50)

    #screen.blit(level_counter, level)
    run = True
    while run:
        clock.tick(Speed)


        #girl_movement(keys_pressed, girl)

        for event in pygame.event.get():

            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_RIGHT]:  # and girl.x+vel+girl.width<990:
                girl.x += vel
            if keys_pressed[pygame.K_LEFT]:  # and girl.x-vel>10:
                girl.x -= vel
            if keys_pressed[pygame.K_SPACE]:
                girl.y -= vel
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Backbutton.collidepoint(event.pos):
                    back()

        pygame.display.flip()
        pygame.display.update()

def back():
    screen.blit(menuBG,(0,0))
    pygame.display.set_caption("Main menu")

    surf = font.render('Play', True, lBlue)
    button = pygame.Rect(62, 340, 120, 50)

    surf2 = font.render('Options', True, lBlue)
    button2 = pygame.Rect(395, 349, 120, 50)

    surf3 = font.render('Quit', True, lBlue)
    button3 = pygame.Rect(840, 265, 120, 50)

    screen.blit(surf, button)
    screen.blit(surf2, button2)
    screen.blit(surf3, button3)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(event.pos):
                    start()
                if button2.collidepoint(event.pos):
                    options()
                if button3.collidepoint(event.pos):
                    pygame.QUIT()
        main(keys_pressed, girl)
        pygame.display.flip()
        pygame.display.update()

def main_menu():
    pygame.display.set_caption("Main menu")
    screen.blit(menuBG,(0,0))

    surf = font.render('Play', True, lBlue)
    button = pygame.Rect(62, 340,120,50)

    surf2 = font.render('Options', True, lBlue)
    button2 = pygame.Rect(395, 349,120,50)

    surf3 = font.render('Quit', True, lBlue)
    button3 = pygame.Rect(840, 265,120,50)

    screen.blit(surf, button)
    screen.blit(surf2, button2)
    screen.blit(surf3, button3)
    girl = pygame.Rect(30, 450, character_width, character_height)
    Backbutton = pygame.Rect(10, 10, 120, 50)

    run= True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                if button.collidepoint(event.pos):
                    start()
                if button2.collidepoint(event.pos):
                    options()
                if button3.collidepoint(event.pos):
                    pygame.QUIT()
                if Backbutton.collidepoint(event.pos):
                    back()
            pygame.display.flip()
            pygame.display.update()


def main(keys_pressed, girl):
    main_menu()
    girl = pygame.Rect(30, 450, character_width , character_height)
    #boy

    clock=pygame.time.Clock()
    run=True
    while run:
        clock.tick(Speed)
        for event in pygame.event.get():
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_RIGHT]:  # and girl.x+vel+girl.width<990:
                girl.x += vel
            if keys_pressed[pygame.K_LEFT]:  # and girl.x-vel>10:
                girl.x -= vel
            if keys_pressed[pygame.K_SPACE]:
                girl.y -= vel
            #girl_movement(keys_pressed, girl)
            start()
        pygame.display.flip()
        pygame.display.update()
        #start(girl)
        #
        if event.type ==pygame.QUIT:
            run=False
        pygame.QUIT()
if __name__=='__main__':
    keys_pressed = pygame.key.get_pressed()
    girl = pygame.Rect(30, 450, character_width, character_height)
    main(keys_pressed, girl)