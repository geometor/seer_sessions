import numpy as np
from collections import deque

"""
Identifies the region enclosed by a red (2) frame, finds white (0) pixels within 
that region, and changes their color to red (2) *only if* they are not adjacent 
(including diagonals) to any gray (5) pixel. Pixels in the frame, gray pixels, 
external white pixels, and internal white pixels adjacent to gray pixels remain unchanged.
"""

def is_adjacent_to_color(grid, r, c, color_val):
    """
    Checks if the pixel at (r, c) has any neighbor (8-connectivity) with the specified color.

    Args:
        grid (np.ndarray): The input grid.
        r (int): Row index of the pixel.
        c (int): Column index of the pixel.
        color_val (int): The color value to check for in neighbors.

    Returns:
        bool: True if any neighbor has the specified color, False otherwise.
    """
    height, width = grid.shape
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Skip the center pixel itself
            if dr == 0 and dc == 0:
                continue
            
            nr, nc = r + dr, c + dc
            
            # Check bounds
            if 0 <= nr < height and 0 <= nc < width:
                if grid[nr, nc] == color_val:
                    return True
    return False

def transform(input_grid):
    """
    Transforms the input grid based on the refined filling rule considering gray neighbors.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert input list of lists to numpy array for efficient operations
    input_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_grid = input_np.copy()
    height, width = input_np.shape
    
    # --- Step 1: Identify externally connected white (0) pixels using BFS (Flood Fill) ---
    # Use a set to keep track of visited external white coordinates for potentially better performance
    external_white = set() 
    queue = deque()

    # Start BFS from all white pixels on the border of the grid.
    # These are guaranteed to be outside any enclosed frame or part of the background.
    for r in range(height):
        for c in [0, width - 1]: # Check first and last columns
            if input_np[r, c] == 0 and (r, c) not in external_white:
                external_white.add((r, c))
                queue.append((r, c))
    for c in range(width):
        for r in [0, height - 1]: # Check first and last rows (avoid double-checking corners)
             if input_np[r, c] == 0 and (r, c) not in external_white:
                external_white.add((r, c))
                queue.append((r, c))

    # Perform BFS to find all reachable white pixels from the outside
    while queue:
        r, c = queue.popleft()

        # Check 4 neighbors (up, down, left, right) - sufficient for flood fill
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within grid bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor is white (0) and hasn't been visited
                if input_np[nr, nc] == 0 and (nr, nc) not in external_white:
                    external_white.add((nr, nc))
                    queue.append((nr, nc))

    # --- Step 2: Fill the internal white pixels based on adjacency to gray ---
    # Iterate through every cell in the grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is white (0)
            if input_np[r, c] == 0:
                # Check if it's an *internal* white pixel (not reached by the border flood fill)
                if (r, c) not in external_white:
                    # Check if this internal white pixel is adjacent to any gray (5) pixel
                    if not is_adjacent_to_color(input_np, r, c, 5):
                        # If NOT adjacent to gray, change its color to red (2) in the output grid
                        output_grid[r, c] = 2
                    # Else (if it IS adjacent to gray), it remains white (0), which is already set by the copy.

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()