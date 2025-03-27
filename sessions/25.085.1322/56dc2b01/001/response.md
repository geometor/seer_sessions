```python
import numpy as np

# Define color constants
WHITE = 0
BLUE = 1
RED = 2
GREEN = 3
YELLOW = 4
GRAY = 5
MAGENTA = 6
ORANGE = 7
AZURE = 8
MAROON = 9

def find_pixels(grid, color_code):
    """Finds all coordinates of pixels with a given color_code."""
    pixels = np.argwhere(grid == color_code)
    # Convert numpy coordinates (row, col) to tuples
    return [tuple(p) for p in pixels]

def get_bounding_box(pixels):
    """Calculates the bounding box (min_row, min_col, max_row, max_col) for a set of pixels."""
    if not pixels:
        return None
    rows = [p[0] for p in pixels]
    cols = [p[1] for p in pixels]
    return min(rows), min(cols), max(rows), max(cols)

def transform(input_grid):
    """
    Moves green object(s) (color 3) towards a stationary red barrier (color 2) until adjacent, 
    then places an azure marker line/column (color 8) adjacent to the moved green object(s) 
    on the side opposite the barrier, spanning the grid dimension.
    """
    
    # Convert input list of lists to a numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape

    # Initialize output_grid with the background color (white)
    output_grid = np.full_like(grid, WHITE)

    # 1. Identify green (movable) and red (barrier) pixels
    green_pixels = find_pixels(grid, GREEN)
    red_pixels = find_pixels(grid, RED)

    # Handle cases where objects might be missing (though not expected based on examples)
    if not green_pixels or not red_pixels:
        return input_grid # Or potentially return an empty grid or raise error

    # 2. Determine bounding boxes
    green_bb = get_bounding_box(green_pixels)
    red_bb = get_bounding_box(red_pixels)

    green_min_row, green_min_col, green_max_row, green_max_col = green_bb
    red_min_row, red_min_col, red_max_row, red_max_col = red_bb

    # 3. Determine movement direction
    dr, dc = 0, 0 # Change in row, change in column
    direction = None

    # Check relative positions - assumes clear separation along one axis
    if green_max_row < red_min_row:
        direction = "DOWN"
        dr = red_min_row - green_max_row - 1
    elif green_min_row > red_max_row:
        direction = "UP"
        dr = red_max_row - green_min_row + 1 # Note: dr will be negative
    elif green_max_col < red_min_col:
        direction = "RIGHT"
        dc = red_min_col - green_max_col - 1
    elif green_min_col > red_max_col:
        direction = "LEFT"
        dc = red_max_col - green_min_col + 1 # Note: dc will be negative
    else:
         # This case suggests overlap or adjacent start - might need refinement
         # For now, assume examples guarantee initial separation
         return grid.tolist() # Or handle error

    # 4. Place the stationary barrier (red pixels) onto the output grid
    for r, c in red_pixels:
        output_grid[r, c] = RED

    # 5. Calculate new positions for green pixels and place them
    moved_green_pixels = []
    for r, c in green_pixels:
        new_r, new_c = r + dr, c + dc
        # Check bounds before placing, though movement logic should keep it inbound
        if 0 <= new_r < height and 0 <= new_c < width:
            output_grid[new_r, new_c] = GREEN
            moved_green_pixels.append((new_r, new_c))
        else:
            # Handle unexpected out-of-bounds movement if necessary
            pass 
            
    # If no green pixels were successfully moved (e.g., due to bounds), return early
    if not moved_green_pixels:
        # This might happen if the initial configuration is strange
        # or movement calculation leads outside. Return current state.
         return output_grid.tolist()


    # 6. Determine marker position and draw it
    moved_green_bb = get_bounding_box(moved_green_pixels)
    mg_min_row, mg_min_col, mg_max_row, mg_max_col = moved_green_bb

    if direction == "DOWN":
        marker_row = mg_min_row - 1
        if 0 <= marker_row < height:
            output_grid[marker_row, :] = AZURE
    elif direction == "UP":
        marker_row = mg_max_row + 1
        if 0 <= marker_row < height:
            output_grid[marker_row, :] = AZURE
    elif direction == "RIGHT":
        marker_col = mg_min_col - 1
        if 0 <= marker_col < width:
            output_grid[:, marker_col] = AZURE
    elif direction == "LEFT":
        marker_col = mg_max_col + 1
        if 0 <= marker_col < width:
            output_grid[:, marker_col] = AZURE

    # 7. Convert the final numpy grid back to a list of lists
    return output_grid.tolist()
```