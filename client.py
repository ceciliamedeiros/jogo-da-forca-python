import pygame
from network import Network
import pickle
pygame.font.init()

width = 700
height = 600
FONT = "monospace" 

btn_color = (0,102,102)
btn_color_over = (0,153,153)

COR_RETANGULO = (200,200,200)

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 300
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont(FONT, 30)
        text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def isOver(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

def redrawWindow(win, game, player):
    win.fill((173, 216, 230))
    if not(game.connected()):
        font = pygame.font.SysFont(FONT, 30)
        text = font.render("Aguardando outro jogador!", 1, (0,0,0))
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        if(game.has_word()):
            if(player == 0):
                font = pygame.font.SysFont(FONT, 30)
                text = font.render("O outro jogador irá fazer suas jogadas", 1,(0,0,0))
                text2 = font.render("Vidas restantes: " + str(game.life), 1, (0,0,0))
                text3 = font.render(game.get_word_q(), 1, ((0,0,0)))
                text4 = font.render(game.get_history(), 1, (0,0,0))
                text5 = font.render(("Histórico"), 1, (0,0,0))
                win.blit(text, (width/2 - text.get_width()/2, (height - 100 - text.get_height()/2) ))
                win.blit(text2, (width/2  - text2.get_width()/2, height/2 - 50 - text2.get_height()/2 - 10))
                win.blit(text3, (width/2  - text3.get_width()/2, height/2 - text3.get_height()/2- 10))
                win.blit(text4, (width/2 - text4.get_width()/2, height/2 - text4.get_height()/2 + 130))
                win.blit(text5, (width/2 - text5.get_width()/2, height/2 - text5.get_height()/2 + 90))
                     
            else:
                font = pygame.font.SysFont(FONT, 30)
                text2 = font.render("Vidas restantes: " + str(game.life), 1, (0,0,0))
                text3 = font.render(game.get_word_q(), 1, ((0,0,0)))
                text4 = font.render(game.get_history(), 1, (0,0,0))
                text5 = font.render(("Histórico"), 1, (0,0,0))
                win.blit(text2, (width/2  - text2.get_width()/2, height/2 - 50 - text2.get_height()/2 - 10))
                win.blit(text3, (width/2  - text3.get_width()/2, height/2 - text3.get_height()/2- 10))
                win.blit(text4, (width/2 - text4.get_width()/2, height/2 - text4.get_height()/2 + 130))
                win.blit(text5, (width/2 - text5.get_width()/2, height/2 - text5.get_height()/2 + 90))
                for btn in buttons:
                    if(btn.text == "Digitar letra"):
                        btn.draw(win)
        else:
            if(player == 0):
                for btn in buttons:
                    if(btn.text == "Digitar palavra"):
                        btn.draw(win)

            else:
                font = pygame.font.SysFont(FONT, 30)
                text = font.render("Aguardando o oponente digitar a palavra", 0, (0,0,0))
                win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))


    
    pygame.display.update()

def get_word():
    base_font = pygame.font.Font(None, 32)
    input_rect = pygame.Rect(270, height/2-32, 140, 32)

    color = pygame.Color('lightskyblue3')  
    word = ""
    active = False  
    aux = True
    while aux:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True 
            if active == True:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        active = False
                        aux = False
                    elif event.key == pygame.K_BACKSPACE:
                        word = word[:(len(word)-1)]
                    else:
                        word += pygame.key.name(event.key)       
                            
            pygame.draw.rect(win, color, input_rect)             
            text_surface = base_font.render(word, True, (255, 255, 255))
            win.blit(text_surface, (input_rect.x+5, input_rect.y+5))
            input_rect.w = max(100, text_surface.get_width()+10)

            pygame.display.flip()
            

    return word

def get_letter():
    base_font = pygame.font.Font(None, 32)
    input_rect = pygame.Rect(270, height/2-32, 140, 32)

    color = pygame.Color('lightskyblue3')  
    active = False  
    aux = True
    letter = ""
    while aux:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True 
            if active == True:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        active = False
                        aux = False
                    else:
                        letter += pygame.key.name(event.key)       
                            
            pygame.draw.rect(win, color, input_rect)             
            text_surface = base_font.render(letter, True, (255, 255, 255))
            win.blit(text_surface, (input_rect.x+5, input_rect.y+5))
            input_rect.w = max(100, text_surface.get_width()+10)

            pygame.display.flip()
            

    return letter
       
buttons = [Button("Digitar palavra", 200, height/2+100, btn_color), Button("Digitar letra", 200, 100, btn_color)]


def main():
    run = True
    clock = pygame.time.Clock()
    network = Network()
    player = int(network.getPlayer())
    print("You are player: ", player)
    while run:
        clock.tick(60)

        try:
            game = network.send("get")
        except:
            run = False
            print("Could not get the game.")
            break


        if game.ended():
            font = pygame.font.SysFont(FONT, 80)
            if (game.win() == 1 and player == 1) or  (game.win() == 0 and player == 0):
                text = font.render("Você GANHOU!", 1, (0, 102, 0))
            else:
                text = font.render("Você perdeu :(", 1, (204, 0, 0))

            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(5000)

            pygame.time.delay(200)
            try:
                game = network.send("reset")
            except: 
                run = False
                print("Could not get the game.")
                break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.MOUSEMOTION:
                color = pygame.Color('lightskyblue3')  
                pos = pygame.mouse.get_pos()
                for btn in buttons:
                    if btn.isOver(pos) and game.connected():
                        btn.color = btn_color_over
                    else:
                        btn.color = btn_color
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in buttons:
                    if btn.isOver(pos) and game.connected():
                        if(btn.text == "Digitar palavra"):
                            if(player == 0) and not(game.has_word()):
                                word = get_word()
                                game = network.send(word)
                        if(btn.text == "Digitar letra"):
                            if(player == 1):
                                letter = get_letter()
                                game = network.send(letter)
                            

        redrawWindow(win, game, player)    

def menu():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((173, 216, 230))
        font = pygame.font.SysFont(FONT, 30)
        text = font.render("Bem vindo ao jogo da forca!", 1, (0,0,0))
        text2 = font.render("Clique em qualquer lugar para jogar", 1, (0,0,0))
        win.blit(text, (100,200))
        win.blit(text2, (50,100))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menu()
