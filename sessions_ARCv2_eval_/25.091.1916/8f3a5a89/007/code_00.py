import numpy as np
from collections import deque

"""
Identify the single connected component of gray (8) pixels that is cardinally 
adjacent to the single magenta (6) pixel or reachable from those adjacent gray 
pixels via cardinal gray-to-gray steps (this is the 'reachable area' R). Blue (1) 
pixels act as barriers during this reachability check.

Then, create the output grid based on the following rules:
1. Magenta (6) pixels remain magenta.
2. Gray (8) pixels within the reachable area R remain gray.
3. Gray (8) pixels *outside* the reachable area R become orange (7).
4. Blue (1) pixels that are cardinally adjacent to any gray pixel within the 
   reachable area R become gray (8).
5. Blue (1) pixels that are *not* cardinally adjacent to any gray pixel in R 
   remain blue (1).
"""

def find_pixel(grid, color):
    """
    Finds the coordinates (row, col) of the first pixel with the specified color.

    Args:
        grid: The numpy array representing the grid.
        color: The integer color value to find.

    Returns:
        A tuple (row, col) if found, otherwise None.
    """
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                return (r, c)
    return None

def find_reachable_gray_component(grid, start_pos):
    """
    Performs a Breadth-First Search (BFS) starting from the gray (8) neighbors
    of the start_pos (magenta pixel) to find all connected gray pixels,
    respecting blue (1) barriers.

    Args:
        grid: The numpy array representing the input grid.
        start_pos: A tuple (row, col) representing the coordinates of the
                   magenta (6) pixel.

    Returns:
        A set of tuples, where each tuple is the (row, col) coordinate of a
        gray pixel belonging to the connected component adjacent to the magenta pixel.
    """
    rows, cols = grid.shape
    component_pixels_r = set() # Stores (r, c) of gray pixels in the reachable component R
    queue = deque()
    
    if start_pos is None: # Handle case where magenta is missing
        return component_pixels_r
        
    start_r, start_c = start_pos

    # --- Step 1: Find initial gray neighbors of the magenta start point ---
    # These are the entry points into the gray component we want to identify.
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # Cardinal directions
        nr, nc = start_r + dr, start_c + dc
        
        # Check if neighbor is within grid bounds
        if 0 <= nr < rows and 0 <= nc < cols:
            # Check if the neighbor is gray (8)
            if grid[nr, nc] == 8:
                # Add to set and queue if not already present
                if (nr, nc) not in component_pixels_r:
                    component_pixels_r.add((nr, nc))
                    queue.append((nr, nc))

    # --- Step 2: Perform BFS starting from these initial gray neighbors ---
    while queue:
        r, c = queue.popleft() # Get the next gray pixel to explore from

        # Explore cardinal neighbors of the current gray pixel
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within grid bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if the neighbor is gray (8) AND not already visited/added
                if grid[nr, nc] == 8 and (nr, nc) not in component_pixels_r:
                    component_pixels_r.add((nr, nc))
                    queue.append((nr, nc)) # Add valid gray neighbor to queue
                    
    return component_pixels_r

def is_blue_adjacent_to_reachable_gray(r, c, grid, reachable_gray_set):
    """
    Checks if a blue pixel at (r, c) is cardinally adjacent to any gray pixel
    that belongs to the reachable_gray_set.

    Args:
        r, c: Coordinates of the blue pixel.
        grid: The input numpy array.
        reachable_gray_set: The set 'R' of reachable gray pixel coordinates.

    Returns:
        True if adjacent to a reachable gray pixel, False otherwise.
    """
    rows, cols = grid.shape
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # Cardinal directions
        nr, nc = r + dr, c + dc
        # Check bounds and if the neighbor is gray and in the reachable set
        if 0 <= nr < rows and 0 <= nc < cols:
            if grid[nr, nc] == 8 and (nr, nc) in reachable_gray_set:
                return True
    return False


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.
    """
    rows, cols = input_grid.shape
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # --- Step 1: Locate the single magenta (6) pixel ---
    magenta_pos = find_pixel(input_grid, 6)
    # Note: Examples guarantee magenta exists, but robust code might handle absence.

    # --- Step 2: Identify the reachable gray component R ---
    reachable_gray_coords = find_reachable_gray_component(input_grid, magenta_pos)

    # --- Step 3: Iterate and transform pixels based on rules ---
    for r in range(rows):
        for c in range(cols):
            pixel_color = input_grid[r, c]
            
            # Rule 3: Gray (8) pixels outside R become Orange (7)
            if pixel_color == 8:
                if (r, c) not in reachable_gray_coords:
                    output_grid[r, c] = 7
                # Else (if it's in R), it remains 8 (due to copy) - Rule 2
                
            # Rule 4 & 5: Blue (1) pixels transformation
            elif pixel_color == 1:
                if is_blue_adjacent_to_reachable_gray(r, c, input_grid, reachable_gray_coords):
                    # Rule 4: Blue adjacent to reachable gray becomes gray
                    output_grid[r, c] = 8
                # Else, it remains 1 (due to copy) - Rule 5
                
            # Rule 1: Magenta remains magenta (due to copy)

    # --- Step 4: Return the modified grid ---
    return output_grid