import numpy as np
import copy

"""
Identify trigger points and draw a 'shadow' pattern.

The transformation rule involves finding specific orange (7) pixels in the input grid that act as triggers. A trigger occurs at position (r, c) if:
1. The pixel at (r, c) is orange (7).
2. The pixel to its right (r, c+1) is also orange (7).
3. The pixel below it (r+1, c) is white (0).
4. The pixel diagonally below and right (r+1, c+1) is white (0).
(Bounds checks are implicit).

When a trigger is found at (r, c):
1. The pixel at (r, c) in the output grid is changed to azure (8).
2. A 'shadow' pattern is drawn starting from below and right of (r, c), but only onto pixels that are currently white (0) in the evolving output grid and are not blocked by magenta rows/columns.
3. Magenta rows/columns are determined by the positions of magenta (6) pixels in the original input grid. Any row or column containing a magenta pixel acts as a barrier.

The shadow pattern consists of:
- Yellow (4) at (r+1, c+1).
- A horizontal line of red (2) pixels starting at (r+1, c+2) and extending rightwards.
- A vertical line of red (2) pixels starting at (r+2, c+1) and extending downwards.
- A green (3) pixel placed just beyond the end of the horizontal red line, at (r+1, c + horizontal_red_length + 2).

Drawing rules:
- The shadow components (4, 2, 3) are only drawn if the target cell is within the grid bounds, the target cell's row is not a magenta row, the target cell's column is not a magenta column, AND the target cell in the current output grid is white (0).
- The red lines extend as far as possible under these constraints.
- The output grid starts as a copy of the input grid. Modifications (8, 4, 2, 3) are made based on triggers found in the input grid.
"""

def find_magenta_barriers(grid):
    """Finds rows and columns containing magenta (6) pixels."""
    magenta_rows = set()
    magenta_cols = set()
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            if grid[r, c] == 6:
                magenta_rows.add(r)
                magenta_cols.add(c)
    return magenta_rows, magenta_cols

def is_safe(r, c, height, width, magenta_rows, magenta_cols, output_grid):
    """Checks if a position is valid for drawing a shadow pixel."""
    return (0 <= r < height and
            0 <= c < width and
            r not in magenta_rows and
            c not in magenta_cols and
            output_grid[r, c] == 0) # Check if the target is currently background

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    Identifies trigger points (specific orange pixels) and draws a shadow pattern.
    """
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    height, width = input_np.shape
    
    # Find rows and columns blocked by magenta pixels
    magenta_rows, magenta_cols = find_magenta_barriers(input_np)

    # Find trigger points and store them to avoid modifying grid during iteration
    triggers = []
    for r in range(height - 1):
        for c in range(width - 1):
            # Check trigger conditions
            if (input_np[r, c] == 7 and
                input_np[r, c+1] == 7 and
                input_np[r+1, c] == 0 and
                input_np[r+1, c+1] == 0):
                triggers.append((r, c))

    # Apply transformations for each trigger
    for r, c in triggers:
        # Change trigger pixel to azure
        # Check if the trigger pixel itself is blocked (unlikely based on examples but good practice)
        if r not in magenta_rows and c not in magenta_cols:
             output_grid[r, c] = 8
        else:
             # If the trigger itself is blocked, maybe don't draw the shadow?
             # Examples suggest the 7->8 change happens regardless, but shadow might be blocked.
             # Let's assume the 7->8 change always happens if trigger conditions met on input.
             output_grid[r, c] = 8 # Change even if blocked, shadow might still draw partially.

        # Draw shadow pattern, checking safety for each pixel placement
        
        # Place yellow (4)
        tr, tc = r + 1, c + 1
        if is_safe(tr, tc, height, width, magenta_rows, magenta_cols, output_grid):
            output_grid[tr, tc] = 4

        # Place horizontal red line (2)
        h_line_len = 0
        for k in range(2, width): # Start checking from k=2 offset
            hr_r, hr_c = r + 1, c + k
            if is_safe(hr_r, hr_c, height, width, magenta_rows, magenta_cols, output_grid):
                output_grid[hr_r, hr_c] = 2
                h_line_len += 1
            else:
                break # Stop extending line if blocked or out of bounds or not white

        # Place vertical red line (2)
        for k in range(2, height): # Start checking from k=2 offset
            vr_r, vr_c = r + k, c + 1
            if is_safe(vr_r, vr_c, height, width, magenta_rows, magenta_cols, output_grid):
                output_grid[vr_r, vr_c] = 2
            else:
                break # Stop extending line if blocked or out of bounds or not white

        # Place green (3)
        # Position is (r+1, c + length_of_red_starting_at_k=2 + 2)
        # Example: trigger (4,12). Red at (5,14), (5,15). len=2. Green at (5, 12+2+2) = (5,16).
        gr_r, gr_c = r + 1, c + h_line_len + 2 
        if is_safe(gr_r, gr_c, height, width, magenta_rows, magenta_cols, output_grid):
            output_grid[gr_r, gr_c] = 3

    return output_grid.tolist()