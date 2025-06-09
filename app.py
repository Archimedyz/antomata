import tkinter as tk
from enums import GridColor, Direction4, Mode

SQUARE_SIZE = 16
HALF_SQUARE_SIZE = SQUARE_SIZE / 2
QUARTER_SQUARE_SIZE = SQUARE_SIZE / 4

STEPS_PER_UPDATE = 1
UPDATES_PER_SECOND = 5
UPDATE_DELAY = 1000 // UPDATES_PER_SECOND

CANVAS_WIDTH = 640
CANVAS_HEIGHT = 640

MIN_WINDOW_WIDTH = 320
MIN_WINDOW_HEIGHT = 320

_state = {
    "grid": None,
    "ant": None,
    "mode": Mode.RUNNING,
    "steps_taken": 0
}

root = tk.Tk()
canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)

root.minsize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
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

    def move_forward(self, grid):
        dx = 0
        dy = 0

        for _ in range(STEPS_PER_UPDATE):

            # get the cell and its color
            cell_id = grid[self.y][self.x]
            cell_color = canvas.itemcget(cell_id, "fill")

            # determine the direction of rotation
            # directions are defined clockwise, so +/- 1 means clockwise/counterclockwise turning.
            if cell_color == GridColor.LIGHT:
                self.direction = (self.direction + 1) % 4
            else:
                self.direction = (self.direction - 1) % 4

            # before moving, toggle the cell color
            canvas.itemconfig(cell_id, fill = GridColor.LIGHT if cell_color == GridColor.DARK else GridColor.DARK)

            # move the ant in the new direction
            if self.direction == Direction4.UP:
                self.y -= 1
                dy -= SQUARE_SIZE
            elif self.direction == Direction4.RIGHT:
                self.x += 1
                dx += SQUARE_SIZE
            elif self.direction == Direction4.DOWN:
                self.y += 1
                dy += SQUARE_SIZE
            elif self.direction == Direction4.LEFT:
                self.x -= 1
                dx -= SQUARE_SIZE

        _state["steps_taken"] += STEPS_PER_UPDATE

        canvas.move(self.canvas_id, dx, dy)

    def move_backward():
        print("move_backward() - not implemented yet...")

def render_and_update():
    if _state["mode"] == Mode.RUNNING:
        _state["ant"].move_forward(_state["grid"])

    if (_state["steps_taken"] > MAX_STEPS):
        print("Finished simulation. Reached MAX_STEPS limit.")
        # stop the loop once we've passed the max steps
        return

    root.after(UPDATE_DELAY, render_and_update)

def new_grid_square(x, y):
    x1 = x * SQUARE_SIZE
    y1 = y * SQUARE_SIZE
    x2 = x1 + SQUARE_SIZE
    y2 = y1 + SQUARE_SIZE

    return canvas.create_rectangle(x1, y1, x2, y2, fill=GridColor.LIGHT, outline="black")

def init_grid():
    # todo: bind grid to canvas size
    grid = [[new_grid_square(x, y) for x in range(50)] for y in range(50)]

    return grid

def on_mouse_press(event):
    # This sets the anchor point for dragging the canvas content
    canvas.scan_mark(event.x, event.y)

def on_mouse_motion(event):
    # When dragging with the middle mouse button, scroll the canvas
    canvas.scan_dragto(event.x, event.y, gain=1)

def on_running_toggle(event=None):
    if _state["mode"] == Mode.RUNNING:
        _state["mode"] = Mode.STEP_THRU
    elif _state["mode"] == Mode.STEP_THRU:
        _state["mode"] = Mode.RUNNING
    else:
        _state["mode"] = Mode.RUNNING

    print("Simulation state toggled to: " + str(_state["mode"]))

def on_step_forward(event=None):
    _state["ant"].move_forward(_state["grid"])

def on_step_backward(event=None):
    print("not implemented yet...")

def on_exit(event=None):
    print("Stopping simulation.")
    root.destroy()

def on_start():
    print("Starting simulation.")
    root.title("Antomata")

    _state["grid"] = init_grid()
    _state["ant"] = Ant(20, 20, Direction4.UP)

    bindEventHandlers()

def bindEventHandlers():
    canvas.bind("<ButtonPress-1>", on_mouse_press)
    canvas.bind("<B1-Motion>", on_mouse_motion)

    root.bind("<space>", on_running_toggle)
    root.bind("<Left>", on_step_backward)
    root.bind("<Right>", on_step_forward)
    root.bind("<comma>", on_step_backward)
    root.bind("<period>", on_step_forward)
    root.bind("q", on_exit)

def run():
    on_start()

    render_and_update()

    root.mainloop()

if __name__ == "__main__":
    run()
