import numpy as np
from collections import deque

"""
Transformation Rule:

1. Identify the single connected object (input pattern) of non-background color (white=0) in the input grid. Record its shape as relative pixel offsets (`input_pattern_shape`), its original color (`original_color`), and the coordinates of its top-left pixel (`r0`, `c0`).
2. Define a fixed 3x3 '8' pattern shape using relative offsets: `fixed_pattern_shape = [(0,0), (0,1), (0,2), (1,0), (1,2), (2,0), (2,1), (2,2)]`.
3. Define an alternate color (magenta=6) and a step size (4).
4. Create an output grid of the same dimensions as the input, filled with the background color.
5. Tile patterns across the output grid. The top-left corner of each potential tile is calculated as `(r, c) = (r0 + step_size * j, c0 + step_size * i)` for non-negative integers `i` (column index) and `j` (row index).
6. For each potential tile position `(i, j)`:
    a. If it's in the original row (`j == 0`):
        - Use the `input_pattern_shape`.
        - Use the `alternate_color` if `i % 3 == 2`, otherwise use the `original_color`.
        - Draw the pattern.
    b. If it's in a subsequent row (`j > 0`):
        - Only draw if `i % 3 == 2`.
        - If drawing, use the `fixed_pattern_shape` and the `alternate_color`.
    c. When drawing, iterate through the chosen pattern's relative offsets `(dr, dc)`. Calculate the absolute pixel coordinates `(pr, pc) = (r + dr, c + dc)`. If `(pr, pc)` is within the grid boundaries, set the output grid pixel at that location to the chosen color. This allows for partial patterns at the edges.
7. Return the final output grid.
"""

def find_pattern_details(grid):
    """
    Finds the first non-background connected object in the grid using BFS.

    Args:
        grid: numpy array representing the input grid.

    Returns:
        A tuple containing:
        - original_color (int): The color of the pattern.
        - top_left (tuple): The (row, col) of the top-left pixel of the pattern.
        - shape_offsets (list): A list of (dr, dc) offsets relative to top_left.
        Returns None if no pattern is found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    q = deque()
    pattern_pixels = []
    original_color = -1
    start_pixel = None

    # Find the first non-background pixel to start the search
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                start_pixel = (r, c)
                original_color = grid[r, c]
                break
        if start_pixel:
            break

    if not start_pixel:
        return None # No pattern found

    # Use BFS to find all connected pixels of the same color (4-connectivity)
    q.append(start_pixel)
    visited[start_pixel] = True
    min_r, min_c = start_pixel

    while q:
        r, c = q.popleft()
        pattern_pixels.append((r, c))
        min_r = min(min_r, r)
        min_c = min(min_c, c)

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and \
               not visited[nr, nc] and grid[nr, nc] == original_color:
                visited[nr, nc] = True
                q.append((nr, nc))

    if not pattern_pixels:
         return None # Should not happen

    top_left = (min_r, min_c)

    # Calculate relative offsets
    shape_offsets = sorted([(r - min_r, c - min_c) for r, c in pattern_pixels])

    return original_color, top_left, shape_offsets

def place_pattern_clipped(grid, shape_offsets, r_start, c_start, color):
    """
    Places the pattern onto the grid pixel by pixel, clipping at boundaries.

    Args:
        grid: The output grid (numpy array) to modify.
        shape_offsets: List of (dr, dc) offsets for the pattern relative to (r_start, c_start).
        r_start: The target row for the top-left corner of the pattern.
        c_start: The target column for the top-left corner of the pattern.
        color: The color to use for drawing the pattern.
    """
    rows, cols = grid.shape
    for dr, dc in shape_offsets:
        pr, pc = r_start + dr, c_start + dc
        # Check bounds before placing pixel
        if 0 <= pr < rows and 0 <= pc < cols:
            grid[pr, pc] = color

def transform(input_grid):
    """
    Applies the tiling and color transformation rule to the input grid.
    """
    # Define constants and parameters
    BACKGROUND_COLOR = 0
    ALTERNATE_COLOR = 6
    STEP_SIZE = 4
    fixed_pattern_shape = [(0,0), (0,1), (0,2), (1,0), (1,2), (2,0), (2,1), (2,2)]

    # --- Step 1 & 2: Identify input pattern and define fixed pattern ---
    details = find_pattern_details(input_grid)
    if details is None:
        # If no pattern, return an empty grid matching input size
        return np.full_like(input_grid, BACKGROUND_COLOR)

    original_color, (r0, c0), input_pattern_shape = details
    rows, cols = input_grid.shape

    # --- Step 4: Initialize output grid ---
    output_grid = np.full_like(input_grid, BACKGROUND_COLOR)

    # --- Step 5-10: Iterate through tiles and draw patterns ---
    j = 0 # Row index for tiling
    while True:
        r_base = r0 + STEP_SIZE * j
        # Optimization: If the starting row is already off-grid, stop
        if r_base >= rows:
            break

        i = 0 # Column index for tiling
        while True:
            c_base = c0 + STEP_SIZE * i
            # Optimization: If the starting column is already off-grid for this row, move to next row
            if c_base >= cols:
                break

            # Determine pattern shape, color, and if we should draw
            should_draw = False
            shape_to_draw = None
            color_to_use = -1

            if j == 0: # Original row
                should_draw = True
                shape_to_draw = input_pattern_shape
                if i % 3 == 2:
                    color_to_use = ALTERNATE_COLOR
                else:
                    color_to_use = original_color
            elif j > 0: # Subsequent rows
                if i % 3 == 2:
                    should_draw = True
                    shape_to_draw = fixed_pattern_shape
                    color_to_use = ALTERNATE_COLOR

            # Place the determined pattern if applicable
            if should_draw:
                place_pattern_clipped(output_grid, shape_to_draw, r_base, c_base, color_to_use)

            i += 1
        j += 1

    return output_grid