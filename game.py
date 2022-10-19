import re # Regex
import pygame
import sys

class Game:
    
    def __init__(self, id):
        self.life = 8
        self.word_q = self.word_a = ""
        self.history = ""
        self.letter = ""
        self.end = False
        self.repeated = False
        self.ready = False
        self.winner = 2

    def restart(self): 
        self.life = 8
        self.word_q = self.word_a = ""
        self.history = ""
        self.letter = ""
        self.end = False
        self.ready = False
        self.winner = 2


    def connected(self):
        return self.ready

    def status(self):  
        if(self.life <= 0):
            self.loss = True

        if(not (self.word_q.find(self.word_a) == -1)):
            self.victory = True

    def ended(self):
        return self.end

    def win(self): 
        if (self.life <= 0):
            self.winner = 0
            self.end = True
        else:
            if (self.word_a == self.word_q):
                self.winner = 1
                self.end = True
        return self.winner

    def initialize_question(self):
        self.word_q = ""
        for i in range(0, len(self.word_a)):
            self.word_q += "-"

    def replace(self):
        for i in range(0, len(self.word_a)):
            if self.letter == self.word_a[i]:
                self.word_q = self.word_q[:i] + self.letter + self.word_q[i+1:]
        self.letter = ""
        self.win()
    
    def lose_points(self):
        self.history += " " + self.letter
        self.life -= 1
        self.letter = ""
        self.win()

    def has_word(self):
        if self.word_a != "":
            return True
        else:
            return False

    def set_letter(self, letter):
        self.letter = letter
        self.update()
    
    def set_word(self, word):
        self.word_a = word
        self.initialize_question()

    def get_word_a(self):
        return self.word_a

    def get_word_q(self):
        return self.word_q

    def get_history(self):
        return self.history

    def update(self):
        if(not (self.history.find(self.letter) == -1) or not (self.word_q.find(self.letter) == -1)):
            self.repeated = True
        elif(not (self.word_a.find(self.letter) == -1)):
            self.replace() 
        else:
            self.lose_points()

    
    
