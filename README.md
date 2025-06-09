# Antomata

Welcome to the Anotmata repo. The original purpose of this repo is to learn some python, and to also implement Langton's Ant. As the project grows, I will also be adding more features and functionality to the app.

## What is Langton's Ant?

Langton's Ant is a cellular automata simulation (I think). We start with an empty grid of squares (cells). An _ant_ is placed on the grid and begins moving based on the following rules:

- If the current cell is white, turn to its right and move
- If the current cell is black, turn to its left and move
- Before moving in any direction, switch the color of the current cell. i.e. White to black, black to white.

The interesting thing about Langton's Ant is that initially, the ant moves around fairly chaotically, following no pattern. However, after 11000 or so steps, a pattern emerges from the chaotic movement. The ant then, following a specific pattern, moves infinitely off to one of the corners (which corner depends on the starting direction of the ant).

You can read up more about Langton's Ant on [Wikipedia](https://en.wikipedia.org/wiki/Langton%27s_ant).

## Why am I doing this?

I am mainly working because I wanted to code something for fun. I saw [a video](https://www.youtube.com/watch?v=1OxBv9Q7Uxo) in which someone used an AI Code Assistant to build out Langton's Ant. The purpose of the video was mainly focusing on the AI tools and how it faired with the development, and what the process was like, but I liked the actual simulation itself. To me, it was completely new, and I wanted to give it a go.

The secondary reason for this is to just pratcice coding and get a bit more familiar w/ Python.

## Running the app

I decided to use `tkinter` for the UI for this app, as it seems to come bundled w/ Python. So there's no additional installation requirements.

When you're ready, you can just run the `app.py` file.

### Controls

Once the simulatio is running, you can control it via your keyboard. Here's all the commands that are currently supported:

- `Q` - Quit the app. This will close the window showing the simulation and terminate the python program.
- `,` (comma) - Process a single update _backwards_ in the simulation.
- `.` (period) - Process a single update _forwards_ in the simulation.
- `Left arrow` (comma) - Process a single update _backwards_ in the simulation.
- `Right arrow` (period) - Process a single update _forwards_ in the simulation.
- `Space` - Toggle between **RUNNING** and **STEP_THRU** modes.
    - **RUNNING**: In this mode, the simulation will run on its own.
    - **STEP_THRU**: In this mode, the simulation will only update when you press the left/right arrow keys, or the comma and period keys. Each key is explained above.

> [!TIP]
> Simulating backwards is only possible in **STEP_THRU** mode. Also, you can't go further back than the beginning of the simulation.

---

That's it! You've made it to the end of the README.md! Thank you for reading this far, I appreciate you.

> [!WARNING]
> This repo is under construction! More to come in the future.

Things I want to add/implement:
- triangular & hexagonal tiling
- Display running information (current mode, steps taken, current configuration)
- Allow changing colors (Instead of white/black/red)
- Allow changing ant starting position
- Allow toggling cell colors w/ clicks (before starting, maybe even during)
- Allow changing configuration while running
