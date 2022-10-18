import pygame
from network import Network
import pickle
pygame.font.init()

LARGURA_TELA = 700 # Não é recomendado alterar esse campo
ALTURA_TELA = 600 # Não é recomendado alterar esse campo
FONT = "georgia" # Não é recomendado alterar esse campo

COR_BOTAO = (220,220,220)
COR_BOTAO_SELECIONADO = (150,150,150)
COR_BOTAO_BORDA = (100,100,100)

COR_RETANGULO = (200,200,200)
width = 700
height = 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 200
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont(FONT, 30)
        text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

buttons = [Button("Iniciar jogo", 100, 500, (0,0,0)), Button("Digitar palavra", 100, 500, (0,0,0)), Button("Digitar letra", 100, 500, (0,0,0))]

def redrawWindow(win, game, player):
    win.fill((173, 216, 230))
    if not(game.connected()):
        font = pygame.font.SysFont(FONT, 30)
        text = font.render("Aguardando outro jogador!", 1, (255,255,255), True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        if(game.has_word()):
            if(player == 0):
                font = pygame.font.SysFont(FONT, 30)
                text = font.render("O outro jogador irá fazer suas jogadas", 0, 	(32,178,170), True)
                text2 = font.render("Vidas restantes: " + str(game.life), 0, 	(32,178,170), True)
                text3 = font.render(game.get_word_q(), 0, 	(32,178,170), True)
                text4 = font.render(game.get_history(), 0, (255,255,25), True)
                win.blit(text, (width/2 - text.get_width()/2, (height - 100 - text.get_height()/2) ))
                win.blit(text2, (width/2  - text2.get_width()/2, height/2 - 50 - text2.get_height()/2 - 10))
                win.blit(text3, (width/2  - text3.get_width()/2 - 20, height/2 - text3.get_height()/2- 10))
                win.blit(text4, (width/2 - text4.get_width()/2 + 10, height/2 - text4.get_height()/2 - 30))
                     
            else:
                font = pygame.font.SysFont(FONT, 50)
                text = font.render("O outro jogador irá fazer suas jogadas", 0, (255,255,25), True)
                text2 = font.render("Vidas" + str(game.life), 0, (255,255,25), True)
                text3 = font.render("p" + game.word_q, 0, (255,255,25), True)
                text4 = font.render("h" + game.history, 0, (255,255,25), True)
                win.blit(text2, (width/2  - text.get_width()/2, height/2 - text.get_height()/2 - 20))
                win.blit(text3, (width/2  - text.get_width()/2, height/2 - text.get_height()/2 - 40))
                win.blit(text4, (width/2 - text.get_width()/2, height/2 - text.get_height()/2 - 60))
                for btn in buttons:
                    if(btn.text == "Digitar letra"):
                        btn.draw(win)
        else:
            if(player == 0):
                for btn in buttons:
                    if(btn.text == "Digitar palavra"):
                        btn.draw(win)

            else:
                font = pygame.font.SysFont(FONT, 20)
                text = font.render("Aguardando o oponente digitar a palavra", 0, (255,255,25), True)
                win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))


    
    pygame.display.update()

def get_word():
    base_font = pygame.font.Font(None, 32)
    input_rect = pygame.Rect(200, 200, 140, 32)

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
                    if event.key == pygame.K_RETURN:
                        active = False
                        aux = False
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
    input_rect = pygame.Rect(200, 200, 140, 32)

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
                    if event.key == pygame.K_RETURN:
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
       
buttons = [Button("Iniciar jogo", 100, 500, (0,0,0)), Button("Digitar palavra", 100, 500, (0,0,0)), Button("Digitar letra", 100, 500, (0,0,0))]


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
            redrawWindow(win, game, player)
            pygame.time.delay(200)
            try:
                game = network.send("reset")
            except: 
                run = False
                print("Could not get the game.")
                break

            font = pygame.font.SysFont(FONT, 90)
            if (game.winner() == 1 and player == 1) or  (game.winner() == 0 and player == 0):
                text = font.render("You WON!", 1, (255, 0, 0))
            else:
                text = font.render("You lost.", 1, (255, 0, 0))

            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in buttons:
                    if btn.click(pos) and game.connected():
                        if(btn.text == "Digitar palavra"):
                            if(player == 0) and not(game.has_word()):
                                word = get_word()
                                game = network.send(word)
                        if(btn.text == "Digitar letra"):
                            if(player == 1):
                                letter = get_letter()
                                print(letter)
                                game = network.send(letter)
                            

        redrawWindow(win, game, player)    

def menu():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((48, 72, 136))
        font = pygame.font.SysFont(FONT, 40)
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
