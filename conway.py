import tkinter as tk
from random import randrange
import sys
import argparse
import math
import csv

class Grid():
    def __init__(self):
        self.width = 100
        self.height = 100
        self.cells = [[0 for x in range(self.width)] for x in range(self.height)]
        self.center_x = math.floor(self.width / 2)
        self.center_y = math.floor(self.height / 2)

class Game(tk.Tk):
    def __init__(self, file_name = None):
        tk.Tk.__init__(self)
        self.grid = Grid()
        self.window_width = 1000
        self.window_height = 1000
        
        self.canvas = tk.Canvas(self, width=self.window_width, height=self.window_height, bg="#000000", bd=0, highlightthickness=0, relief='ridge')
        self.canvas.pack()
        self.title("Conway's Game of Life")

        if file_name == None:
            self.init_random()
        else:
            self.init_from_file(file_name=file_name)

        self.game_loop()

    def init_from_file(self, file_name):
        try:
            file = open(file_name, "r")
            csv_reader = csv.reader(file, delimiter=",")
            for row in csv_reader:
                self.grid.cells[int(row[1])][int(row[0])] = 1
        except FileNotFoundError:
            print("File does not exist")
            exit(1)

    def init_random(self):
        rand = randrange(30, 50)
        i = 0
        while i < rand:
            rand_x = randrange(self.grid.center_x - 5, self.grid.center_x + 5)
            rand_y = randrange(self.grid.center_y - 5, self.grid.center_y + 5)
            if self.grid.cells[rand_y][rand_x] == 0:
                self.grid.cells[rand_y][rand_x] = 1
                i += 1

    def game_loop(self):
        self.canvas.delete("all")
        self.draw()
        self.enforce_rules()
        self.after(50, self.game_loop)
        
    def enforce_rules(self):
        temp_cells = [[0 for x in range(self.grid.width)] for x in range(self.grid.height)]

        for i in range(self.grid.height):
            for j in range(self.grid.width): 
                number_neighbors = self.get_number_of_neighbors(j, i)
                
                # Rule 2: Any live cell with two or there live neighbours lives on to the next generation.
                if self.grid.cells[i][j] == 1 and (number_neighbors == 2 or number_neighbors == 3):
                    temp_cells[i][j] = 1
                
                # Rule 4: Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
                elif self.grid.cells[i][j] == 0 and number_neighbors == 3:
                    temp_cells[i][j] = 1
        
        self.grid.cells = temp_cells
    
    def get_number_of_neighbors(self, x, y):
        n = 0
        # Right
        if x + 1 < self.grid.width and self.grid.cells[y][x + 1] == 1:
            n += 1
        # Left
        if x - 1 >= 0 and self.grid.cells[y][x - 1] == 1:
            n += 1
        # Above
        if y + 1 < self.grid.height and self.grid.cells[y + 1][x] == 1:
            n += 1
        # Below
        if y - 1 >= 0 and  self.grid.cells[y - 1][x] == 1:
            n += 1
        # Diagonally above and left
        if y + 1 < self.grid.height and x - 1 >= 0 and self.grid.cells[y + 1][x - 1] == 1:
            n += 1
        # Diagonally above and right
        if y + 1 < self.grid.height and x + 1 < self.grid.width and self.grid.cells[y + 1][x + 1] == 1:
            n += 1
        # Diagonally below and left
        if y - 1 >= 0 and x - 1 >= 0 and self.grid.cells[y - 1][x - 1] == 1:
            n += 1
        # Diagonally below and right
        if x + 1 < self.grid.width and y - 1 >= 0 and self.grid.cells[y - 1][x + 1] == 1:
            n += 1

        return n

    def draw(self):
        for i in range(self.grid.height):
            for j in range(self.grid.width):
                if self.grid.cells[i][j] == 1:
                    self.canvas.create_rectangle(j * 10, i * 10, j * 10 + 10 , i * 10 + 10, fill="#EEEEEE", outline="#222222")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_name', type = str, required = False)
    args = parser.parse_args()
    if args.file_name:
        game = Game(args.file_name)
        game.mainloop()
    else:
        game = Game()
        game.mainloop()
