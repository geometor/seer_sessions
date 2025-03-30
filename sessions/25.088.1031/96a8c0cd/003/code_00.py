import numpy as np
from collections import deque

"""
Perform a flood fill operation starting from the single red (2) pixel in the input grid.
The fill color is red (2).
The fill expands to adjacent white (0) pixels (up, down, left, right).
The fill stops expanding when it encounters a blue (1) pixel, a green (3) pixel, or the grid boundary.
The original red, blue, and green pixels remain unchanged. White pixels not reachable from the red seed
through a path of white pixels (without crossing blue or green) also remain unchanged.
"""

def find_seed_point(grid, color):
    """Finds the coordinates (row, col) of the first pixel with the specified color."""
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                return (r, c)
    return None # Should not happen based on task description if seed always exists

def transform(input_grid):
    """
    Applies a bounded flood fill originating from the red pixel (2), filling
    reachable white pixels (0) with red (2), bounded by blue (1), green (3),
    and grid edges.

    Args:
        input_grid (np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed output grid.
    """
    rows, cols = input_grid.shape
    # Initialize output_grid as a copy of the input to preserve original boundary/seed pixels
    output_grid = np.copy(input_grid)

    # Define color constants based on the problem description
    background_color = 0 # White - the medium to be filled
    boundary_color_1 = 1 # Blue - stops the fill
    seed_color = 2       # Red - the starting point of the fill
    fill_color = 2       # Red - the color used to fill
    boundary_color_2 = 3 # Green - stops the fill

    # 1. Find the starting point for the flood fill (the single red pixel)
    seed_coords = find_seed_point(input_grid, seed_color)

    # If no seed point is found (shouldn't happen per task description), return original
    if not seed_coords:
        return output_grid

    # 2. Perform a Breadth-First Search (BFS) to find all white cells reachable from the seed
    #    without crossing boundaries (blue, green, or grid edges).
    reachable_white_cells = set() # Store coordinates of white cells to be filled
    queue = deque([seed_coords])     # Queue for BFS, starting with the seed
    visited = {seed_coords}          # Set to keep track of all visited coordinates (seed, white, boundary)

    while queue:
        # Get the next coordinate to process
        r, c = queue.popleft()

        # Explore the 4 adjacent neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if the neighbor is within the grid boundaries
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue # Skip if out of bounds

            # Check if the neighbor has already been visited
            if (nr, nc) in visited:
                continue # Skip if already processed

            # Mark the neighbor as visited to prevent reprocessing
            visited.add((nr, nc))

            # Get the color of the neighbor in the *original* input grid
            neighbor_color = input_grid[nr, nc]

            # If the neighbor is a white pixel (background_color):
            # It's part of the area to be filled. Add it to our set of
            # reachable white cells and add it to the queue to explore from it.
            if neighbor_color == background_color:
                reachable_white_cells.add((nr, nc))
                queue.append((nr, nc))

            # If the neighbor is a boundary color (blue or green) or any other non-white color:
            # The fill stops here for this path. We've already marked it as visited,
            # so we don't need to do anything else (specifically, don't add it to the queue).

    # 3. Modify the output grid: Change the color of all identified reachable white cells to the fill color.
    for r_fill, c_fill in reachable_white_cells:
        output_grid[r_fill, c_fill] = fill_color

    # 4. Return the modified grid
    return output_grid