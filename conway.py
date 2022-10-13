import tkinter as tk
from random import randrange
import argparse
import math
import csv


class Grid():
    def __init__(self):
        self.width = 100
        self.height = 100
        self.cells = [[0 for x in range(self.width)]
                      for x in range(self.height)]
        self.center_x = math.floor(self.width / 2)
        self.center_y = math.floor(self.height / 2)


class Game(tk.Tk):
    def __init__(self, file_name=None):
        tk.Tk.__init__(self)
        self.grid = Grid()
        self.window_width = 1000
        self.window_height = 1000
        self.paused = False
        self.delay = 100
        self.file_name = file_name
        self.color_grid = "#2E3440"
        self.color_cell_fill = "#EEEEEE"
        self.color_cell_outline = "#222222"

        self.canvas = tk.Canvas(self, width=self.window_width, height=self.window_height,
                                bg=self.color_grid, bd=0, highlightthickness=0, relief='ridge')
        self.canvas.pack()
        self.title("Conway's Game of Life")

        if file_name == None:
            self.init_random()
        else:
            self.init_from_file(file_name=file_name)

        # Keypress bindings
        self.bind("<KeyPress-r>", self.restart)
        self.bind("<space>", self.pause)
        self.bind("<Escape>", self.exit_game)
        self.bind("<Up>", self.speed_up)
        self.bind("<Down>", self.slow_down)

        self.game_loop()

    def speed_up(self, event):
        if self.delay > 10:
            self.delay -= 10

    def slow_down(self, event):
        if self.delay < 1000:
            self.delay += 10

    def exit_game(self, event):
        exit(0)

    def restart(self, event):
        self.grid = Grid()
        if self.file_name:
            self.init_from_file(self.file_name)
        else:
            self.init_random()
        if self.paused:
            self.paused = False
            self.game_loop()

    def pause(self, event):
        if self.paused:
            self.paused = False
            self.game_loop()
        else:
            self.paused = True

    def init_from_file(self, file_name):
        try:
            file = open(file_name, "r")
            csv_reader = csv.reader(file, delimiter=",")
            for row in csv_reader:
                # Catch negative indices
                cell = (int(row[1]), int(row[0]))
                if cell[0] < 0 or cell[1] < 0:
                    print("Error: No negative indices are allowed.")
                    exit(1)
                self.grid.cells[cell[0]][cell[1]] = 1
        # Catch non-integer indices
        except ValueError:
            print(
                "Error: Please check that your file only contains integers separated by commas")
            exit(1)
        except IndexError:
            print("Error: One of your coordinates is out of bounds")
            exit(1)
        except FileNotFoundError:
            print("Error: File does not exist")
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
        if not self.paused:
            self.canvas.delete("all")
            self.draw()
            self.enforce_rules()
            self.after(self.delay, self.game_loop)

    def enforce_rules(self):
        next_generation = [[0 for x in range(self.grid.width)]
                           for x in range(self.grid.height)]

        for i in range(self.grid.height):
            for j in range(self.grid.width):
                number_neighbors = self.get_number_of_neighbors(j, i)

                # Rule 2: Any live cell with two or there live neighbours lives on to the next generation.
                if self.grid.cells[i][j] == 1 and (number_neighbors == 2 or number_neighbors == 3):
                    next_generation[i][j] = 1

                # Rule 4: Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
                elif self.grid.cells[i][j] == 0 and number_neighbors == 3:
                    next_generation[i][j] = 1

        self.grid.cells = next_generation

    def get_number_of_neighbors(self, x, y):
        n = 0

        # Calculate minimum and maximum (x,y) values in order
        # to avoid going out of bounds.
        y_min = max(y - 1, 0)
        y_max = min(y + 1, self.grid.height - 1)
        x_min = max(x - 1, 0)
        x_max = min(x + 1, self.grid.width - 1)

        for i in range(y_min, y_max + 1):
            for j in range(x_min, x_max + 1):
                if i == y and j == x:
                    continue
                if self.grid.cells[i][j] == 1:
                    n += 1

        return n

    def draw(self):
        for i in range(self.grid.height):
            for j in range(self.grid.width):
                if self.grid.cells[i][j] == 1:
                    self.canvas.create_rectangle(
                        j * 10, i * 10, j * 10 + 10, i * 10 + 10, fill=self.color_cell_fill, outline=self.color_cell_outline)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_name", type=str, required=False)
    args = parser.parse_args()
    game = None
    if args.file_name:
        game = Game(args.file_name)
    else:
        game = Game()
    game.mainloop()
