import tkinter as tk
from enums import GridColor, Direction4, Mode

SQUARE_SIZE = 16
HALF_SQUARE_SIZE = SQUARE_SIZE // 2
QUARTER_SQUARE_SIZE = SQUARE_SIZE // 4

STEPS_PER_UPDATE = 1
UPDATES_PER_SECOND = 10
UPDATE_DELAY = 1000 // UPDATES_PER_SECOND

GRID_WIDTH = 100
GRID_LENGTH = 100

CANVAS_WIDTH = SQUARE_SIZE * GRID_WIDTH
CANVAS_HEIGHT = SQUARE_SIZE * GRID_LENGTH

MIN_WINDOW_WIDTH = 320
MIN_WINDOW_HEIGHT = 320

MAX_WINDOW_WIDTH = 640
MAX_WINDOW_HEIGHT = 640

MAX_STEPS = 20000

_state = {
    "grid": None,
    "ant": None,
    "mode": Mode.RUNNING,
    "steps_taken": 0
}

root = tk.Tk()
grid_canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)

root.maxsize(MAX_WINDOW_WIDTH, MAX_WINDOW_HEIGHT)
root.minsize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
root.update_idletasks() # Ensures the canvas dimensions are calculated

grid_canvas.pack(fill=tk.BOTH, expand=True)

class Ant:
    def __init__(self, start_x, start_y, start_direction):
        self.x = start_x
        self.y = start_y
        self.direction = start_direction
        self.steps_taken = 0
        self.move_history = []

        ant_x0 = (self.x * SQUARE_SIZE) + QUARTER_SQUARE_SIZE
        ant_y0 = (self.y * SQUARE_SIZE) + QUARTER_SQUARE_SIZE
        ant_x1 = ant_x0 + HALF_SQUARE_SIZE
        ant_y1 = ant_y0 + HALF_SQUARE_SIZE

        self.canvas_id = grid_canvas.create_rectangle(ant_x0, ant_y0, ant_x1, ant_y1, fill="red", outline="black")

    def move_forward(self, grid):
        dx = 0
        dy = 0

        for _ in range(STEPS_PER_UPDATE):
            # get the cell and its color
            cell_id = grid[self.y][self.x]
            cell_color = grid_canvas.itemcget(cell_id, "fill")

            # record the direction before moving
            self.move_history.append(self.direction)

            # determine the direction of rotation
            # directions are defined clockwise, so +/- 1 means clockwise/counter-clockwise turning.
            if cell_color == GridColor.LIGHT:
                self.direction = (self.direction + 1) % 4
            else:
                self.direction = (self.direction - 1) % 4

            # before moving, toggle the cell color
            grid_canvas.itemconfig(cell_id, fill = GridColor.LIGHT if cell_color == GridColor.DARK else GridColor.DARK)

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

        grid_canvas.move(self.canvas_id, dx, dy)

    def move_backward(self, grid):
        if len(self.move_history) == 0:
            print("Cannot move backwards; reached teh starting position.")
            return

        dx = 0
        dy = 0

        for _ in range(STEPS_PER_UPDATE):
            # move the ant backwards in the current direction
            if self.direction == Direction4.UP:
                self.y += 1
                dy += SQUARE_SIZE
            elif self.direction == Direction4.RIGHT:
                self.x -= 1
                dx -= SQUARE_SIZE
            elif self.direction == Direction4.DOWN:
                self.y -= 1
                dy -= SQUARE_SIZE
            elif self.direction == Direction4.LEFT:
                self.x += 1
                dx += SQUARE_SIZE

            # set the previous direcion from the move history
            self.direction = self.move_history.pop()

            # get the old cell and its color
            cell_id = grid[self.y][self.x]
            cell_color = grid_canvas.itemcget(cell_id, "fill")

            # toggle the cell color to return it to its old value
            grid_canvas.itemconfig(cell_id, fill = GridColor.LIGHT if cell_color == GridColor.DARK else GridColor.DARK)

        _state["steps_taken"] -= STEPS_PER_UPDATE

        grid_canvas.move(self.canvas_id, dx, dy)

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

    return grid_canvas.create_rectangle(x1, y1, x2, y2, fill=GridColor.LIGHT, outline="black")

def init_grid():
    # todo: bind grid to canvas size
    grid = [[new_grid_square(x, y) for x in range(GRID_WIDTH)] for y in range(GRID_LENGTH)]

    return grid

def on_mouse_press(event):
    # This sets the anchor point for dragging the canvas content
    grid_canvas.scan_mark(event.x, event.y)

def on_mouse_motion(event):
    # When dragging with the middle mouse button, scroll the canvas
    grid_canvas.scan_dragto(event.x, event.y, gain=1)

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
    _state["ant"].move_backward(_state["grid"])

def on_exit(event=None):
    print("Stopping simulation.")
    root.destroy()

def on_start():
    print("Starting simulation.")
    root.title("Antomata")

    _state["grid"] = init_grid()

    ant_start_x = GRID_WIDTH // 2
    ant_start_y = GRID_LENGTH // 2

    _state["ant"] = Ant(ant_start_x, ant_start_y, Direction4.UP)

    # A small hack to ensure the window is rendered before centering.
    root.after(100, center_view_on_ant)

def bindEventHandlers():
    grid_canvas.bind("<ButtonPress-1>", on_mouse_press)
    grid_canvas.bind("<B1-Motion>", on_mouse_motion)

    root.bind("<space>", on_running_toggle)
    root.bind("<Left>", on_step_backward)
    root.bind("<Right>", on_step_forward)
    root.bind("<comma>", on_step_backward)
    root.bind("<period>", on_step_forward)
    root.bind("q", on_exit)

def center_view_on_ant():
    x = _state["ant"].x * SQUARE_SIZE
    y = _state["ant"].y * SQUARE_SIZE

    size = (root.winfo_width(), root.winfo_height())

    drag_x = int((size[0] / 2) - x)
    drag_y = int((size[1] / 2) - y)

    print("ant:  " + str([x, y]))
    print("size: " + str(size))
    print("drag: " + str([drag_x, drag_y]))

    grid_canvas.scan_dragto(drag_x, drag_y, gain=1)

def run():
    bindEventHandlers()

    on_start()

    render_and_update()

    root.mainloop()

if __name__ == "__main__":
    run()
