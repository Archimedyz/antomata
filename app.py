import tkinter as tk

UP=0
RIGHT=1
DOWN=2
LEFT=3

LIGHT="white"
DARK="gray16"

SQUARE_SIZE = 16
HALF_SQUARE_SIZE = SQUARE_SIZE / 2
QUARTER_SQUARE_SIZE = SQUARE_SIZE / 4

STEPS_PER_UPDATE = 10
UPDATES_PER_SECOND = 10
UPDATE_DELAY = 1000 // UPDATES_PER_SECOND

CANVAS_WIDTH = 640
CANVAS_HEIGHT = 640


root = tk.Tk()
canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)

root.minsize(CANVAS_WIDTH, CANVAS_HEIGHT)
root.update_idletasks() # Ensures the canvas dimensions are calculated

canvas.pack(fill=tk.BOTH, expand=True)

MAX_STEPS = 20000

class Ant:
    def __init__(self, start_x, start_y, start_direction):
        self.x = start_x
        self.y = start_y
        self.direction = start_direction
        self.steps_taken = 0

        ant_x0 = (self.x * SQUARE_SIZE) + QUARTER_SQUARE_SIZE
        ant_y0 = (self.y * SQUARE_SIZE) + QUARTER_SQUARE_SIZE
        ant_x1 = ant_x0 + HALF_SQUARE_SIZE
        ant_y1 = ant_y0 + HALF_SQUARE_SIZE

        self.canvas_id = canvas.create_rectangle(ant_x0, ant_y0, ant_x1, ant_y1, fill="red", outline="black")

    def move(self, grid):
        dx = 0
        dy = 0

        for _ in range(STEPS_PER_UPDATE):

            # get the cell and its color
            cell_id = grid[self.y][self.x]
            cell_color = canvas.itemcget(cell_id, "fill")

            # determine the direction of rotation
            # directions are defined clockwise, so +/- 1 means clockwise/counterclockwise turning.
            if cell_color == LIGHT:
                self.direction = (self.direction + 1) % 4
            else:
                self.direction = (self.direction - 1) % 4

            # before moving, toggle the cell color
            canvas.itemconfig(cell_id, fill= LIGHT if cell_color == DARK else DARK)

            # move the ant in the new direction
            if self.direction == UP:
                self.y -= 1
                dy -= SQUARE_SIZE
            elif self.direction == RIGHT:
                self.x += 1
                dx += SQUARE_SIZE
            elif self.direction == DOWN:
                self.y += 1
                dy += SQUARE_SIZE
            elif self.direction == LEFT:
                self.x -= 1
                dx -= SQUARE_SIZE

        self.steps_taken += STEPS_PER_UPDATE

        canvas.move(self.canvas_id, dx, dy)

def render_and_update(grid, ant):
    ant.move(grid)

    if (ant.steps_taken < MAX_STEPS):
        root.after(UPDATE_DELAY, lambda : render_and_update(grid, ant))
    else:
        print("Finished simulation. Reached MAX_STEPS limit.")

def newSquare(x, y):

    x1 = x * SQUARE_SIZE
    y1 = y * SQUARE_SIZE
    x2 = x1 + SQUARE_SIZE
    y2 = y1 + SQUARE_SIZE

    return canvas.create_rectangle(x1, y1, x2, y2, fill=LIGHT, outline="black")

def initGrid():
    # todo: bind grid to canvas size
    grid = [[newSquare(x, y) for x in range(50)] for y in range(50)]

    return grid

def run():    
    root.title("Antomata")

    grid = initGrid()
    ant = Ant(20, 20, UP)

    render_and_update(grid, ant)
    root.mainloop()

if __name__ == "__main__":
    run()
