import numpy as np
from collections import deque

"""
Transformation Rule Natural Language Description:

1. Identify all distinct contiguous objects composed of blue (1) pixels in the input grid using 4-way adjacency (up, down, left, right).
2. Determine the set of all white (0) pixels that are reachable from the border of the grid by traversing only adjacent (4-way) white pixels. This can be done using a flood fill starting from all border white pixels. White pixels *not* in this set are considered "unreachable" or part of a "hole".
3. Create an output grid, initially identical to the input grid.
4. For each identified blue object:
    a. Check if any pixel belonging to the blue object is adjacent (4-way) to a white pixel that is "unreachable" (i.e., not reachable from the border, as determined in step 2).
    b. If such an adjacent unreachable white pixel exists (meaning the blue object borders or encloses a hole), change the color of *all* pixels belonging to that specific blue object from blue (1) to red (2) in the output grid.
5. Leave all other pixels (original non-blue pixels, and blue pixels belonging to objects that do not border/enclose holes) unchanged.
"""

def find_objects(grid, color):
    """
    Finds all contiguous objects of a specific color using 4-way adjacency.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list: A list of lists, where each inner list contains the 
              coordinates (row, col) of pixels belonging to a single object.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            # If we find a pixel of the target color that hasn't been visited
            if grid[r, c] == color and not visited[r, c]:
                obj_pixels = []
                # Start a Breadth-First Search (BFS) from this pixel
                q = deque([(r, c)])
                visited[r, c] = True
                while q:
                    row, col = q.popleft()
                    obj_pixels.append((row, col))
                    # Explore 4-way adjacent neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds and if the neighbor is the same color and unvisited
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                # Add the found object (list of pixel coordinates) to our list
                if obj_pixels:
                    objects.append(obj_pixels)
    return objects

def flood_fill_background(grid, background_color=0):
    """
    Performs a flood fill from border pixels of the specified background_color.

    Args:
        grid (np.array): The input grid.
        background_color (int): The color to flood fill from the border (default 0).

    Returns:
        np.array: A boolean mask where True indicates a pixel of background_color
                  is reachable from the border.
    """
    height, width = grid.shape
    reachable_mask = np.zeros_like(grid, dtype=bool)
    q = deque()

    # Seed the queue with all border pixels of the background color
    for r in range(height):
        if grid[r, 0] == background_color and not reachable_mask[r, 0]:
            q.append((r, 0))
            reachable_mask[r, 0] = True
        if grid[r, width - 1] == background_color and not reachable_mask[r, width - 1]:
            q.append((r, width - 1))
            reachable_mask[r, width - 1] = True
    for c in range(width): # Use range(width) to include corners correctly
        if grid[0, c] == background_color and not reachable_mask[0, c]:
             q.append((0, c))
             reachable_mask[0, c] = True
        if grid[height - 1, c] == background_color and not reachable_mask[height - 1, c]:
            q.append((height - 1, c))
            reachable_mask[height - 1, c] = True
            
    # Perform BFS from the border pixels
    while q:
        r, c = q.popleft()
        # Explore 4-way neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check bounds, if neighbor is background_color, and not already marked reachable
            if 0 <= nr < height and 0 <= nc < width and \
               grid[nr, nc] == background_color and not reachable_mask[nr, nc]:
                reachable_mask[nr, nc] = True
                q.append((nr, nc))
                
    return reachable_mask

def has_adjacent_hole(grid, obj_pixels, background_reachable_mask, hole_color=0):
    """
    Checks if any pixel in the object is adjacent to an unreachable pixel 
    of the specified hole_color.

    Args:
        grid (np.array): The input grid.
        obj_pixels (list): List of (row, col) coordinates for the object.
        background_reachable_mask (np.array): Boolean mask from flood_fill_background.
        hole_color (int): The color representing holes (default 0).

    Returns:
        bool: True if the object is adjacent to a hole pixel, False otherwise.
    """
    height, width = grid.shape
    
    # Check neighbors for every pixel in the object
    for r, c in obj_pixels:
        # Explore 4-way neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check if neighbor is within bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor is the hole_color AND was NOT reached 
                # by the background flood fill (meaning it's part of a hole)
                if grid[nr, nc] == hole_color and not background_reachable_mask[nr, nc]:
                    # Found an adjacent hole pixel
                    return True
                    
    # No adjacent hole pixels found after checking all object pixels' neighbors
    return False 

def transform(input_grid):
    """
    Transforms the input grid by changing blue objects (color 1) to red (color 2) 
    if they enclose or are adjacent to any white pixels (color 0) that are not 
    reachable from the grid border.

    Args:
        input_grid (list): A list of lists representing the input grid.

    Returns:
        list: A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to numpy array for efficient processing
    input_grid_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid_np)
    
    # Define colors
    blue_color = 1
    red_color = 2
    white_color = 0 # Color considered for holes

    # Step 1: Find all white pixels reachable from the border
    background_reachable_mask = flood_fill_background(input_grid_np, white_color)
    
    # Step 2: Find all distinct blue objects
    blue_objects = find_objects(input_grid_np, blue_color)
    
    # Step 3: Check each blue object for adjacency to holes and update output grid
    for obj_pixels in blue_objects:
        # Check if the object is adjacent to any unreachable white pixel (a hole)
        if has_adjacent_hole(input_grid_np, obj_pixels, background_reachable_mask, white_color):
            # If it borders a hole, change all its pixels to red in the output grid
            for r, c in obj_pixels:
                output_grid[r, c] = red_color

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()