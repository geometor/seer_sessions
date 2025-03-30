import numpy as np
from collections import deque

"""
Transforms the input grid by identifying connected regions of non-green pixels 
that are enclosed by green pixels (color 3) or the grid boundary. These 
enclosed regions are filled with azure (color 8). Green pixels act as barriers 
and remain unchanged. Other non-green pixels not part of an enclosed region also 
remain unchanged.

The logic uses a flood fill approach starting from the border:
1. Initialize an output grid as a copy of the input.
2. Initialize a 'reached' grid to track pixels connected to the border.
3. Create a queue and add all non-green pixels located on the grid's border 
   to it. Mark these border pixels as 'reached'.
4. Perform a Breadth-First Search (BFS) starting from the pixels in the queue:
    a. Dequeue a pixel.
    b. Explore its 4-way adjacent neighbors.
    c. If a neighbor is within bounds, is not green (barrier), and has not 
       been reached yet, mark it as 'reached' and add it to the queue.
5. After the BFS completes, all non-green pixels connected to the border (without 
   crossing a green barrier) will be marked as 'reached'.
6. Iterate through the entire grid:
    a. If a pixel is not green and was *not* marked as 'reached', it belongs 
       to an enclosed region.
    b. Change the color of such enclosed pixels in the output grid to azure (8).
7. Return the modified output grid.
"""

def transform(input_grid):
    """
    Applies the flood fill transformation rule to the input grid.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists of integers.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input to a NumPy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape
    
    # Initialize the output grid as a copy of the input grid.
    output_grid = grid.copy()

    # Define barrier color and the color to fill enclosed areas
    barrier_color = 3
    fill_color = 8

    # Keep track of non-barrier cells reachable from the border
    reached = np.zeros_like(grid, dtype=bool)
    queue = deque()

    # Add all non-barrier border cells to the queue and mark them as reached
    for r in range(height):
        for c in range(width):
            # Check if the cell is on the border
            is_border = (r == 0 or r == height - 1 or c == 0 or c == width - 1)
            if is_border and grid[r, c] != barrier_color:
                if not reached[r, c]: # Avoid adding duplicates if corner/already processed
                    reached[r, c] = True
                    queue.append((r, c))

    # Perform BFS starting from the border cells
    while queue:
        curr_r, curr_c = queue.popleft()

        # Explore neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = curr_r + dr, curr_c + dc

            # Check if the neighbor is within grid bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor is not a barrier and has not been reached yet
                if grid[nr, nc] != barrier_color and not reached[nr, nc]:
                    # Mark as reached and add to the queue to explore
                    reached[nr, nc] = True
                    queue.append((nr, nc))

    # Fill the enclosed regions (non-barrier cells not reached from the border)
    for r in range(height):
        for c in range(width):
            # If a cell is not a barrier and was not reached by the BFS
            if grid[r, c] != barrier_color and not reached[r, c]:
                # It's an enclosed cell, fill it with the fill_color
                output_grid[r, c] = fill_color

    # Convert the result back to a standard list of lists format
    return output_grid.tolist()