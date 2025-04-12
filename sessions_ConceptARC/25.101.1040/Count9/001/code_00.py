"""
This module transforms an input grid based on the following rule:

1. Identify all distinct contiguous objects in the input grid. An object is defined as a group of one or more connected pixels of the same color, where the color is not the background color (white, 0). Connectivity includes horizontal, vertical, and diagonal adjacency (8-way connectivity).
2. Count the total number of these distinct non-background objects.
3. Create a new output grid that has a height of 1 and a width equal to the total count of objects found.
4. Fill the entire output grid with the background color (white, 0).
"""

import collections

def _find_objects(grid: list[list[int]]) -> int:
    """
    Finds and counts all distinct contiguous non-background objects in the grid.
    Uses Breadth-First Search (BFS) with 8-way connectivity.

    Args:
        grid: The input grid (list of lists of integers).

    Returns:
        The total count of distinct non-background objects.
    """
    if not grid or not grid[0]:
        return 0

    rows = len(grid)
    cols = len(grid[0])
    visited = set()  # Keep track of visited cells (r, c)
    object_count = 0
    background_color = 0

    # Define 8 directions for neighbors (horizontal, vertical, diagonal)
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    # Iterate through each cell of the grid
    for r in range(rows):
        for c in range(cols):
            # Check if the cell is a non-background color and hasn't been visited yet
            if grid[r][c] != background_color and (r, c) not in visited:
                # Found the start of a new object
                object_count += 1
                object_color = grid[r][c] # Get the color of the current object
                
                # Start BFS to find all connected cells of the same color
                queue = collections.deque([(r, c)])
                visited.add((r, c)) # Mark the starting cell as visited

                while queue:
                    curr_r, curr_c = queue.popleft()

                    # Explore all 8 neighbors
                    for dr, dc in directions:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check if the neighbor is within the grid bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Check if the neighbor has the same color as the object 
                            # and has not been visited yet
                            if grid[nr][nc] == object_color and (nr, nc) not in visited:
                                visited.add((nr, nc)) # Mark neighbor as visited
                                queue.append((nr, nc)) # Add neighbor to the queue to explore from
    
    return object_count

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Transforms the input grid by counting non-background objects and creating 
    a corresponding white output row.

    Args:
        input_grid: A list of lists representing the input grid with integer color values.

    Returns:
        A list of lists representing the output grid (a single row of background color).
    """
    # Find and count all distinct non-background objects in the input grid
    num_objects = _find_objects(input_grid)
    
    # Define the background color
    background_color = 0
    
    # Create the output grid: a single row with width equal to the number of objects,
    # filled with the background color.
    # If num_objects is 0, this correctly creates an empty inner list `[[]]`, 
    # which might need adjustment depending on expected output for zero objects.
    # Based on examples, a 1xN grid is expected. If N=0, maybe `[]` or `[[0]]`?
    # The examples always show N > 0. Let's assume N >= 1. If N=0, result should be `[]`?
    # Standard interpretation would be a 1x0 grid, often represented as `[[]]` or `[]`.
    # Let's stick to `[[0] * num_objects]` which gives `[[]]` for `num_objects = 0`.
    # If the ARC framework expects `[]` for an empty grid, this might need adjustment.
    # Let's assume `[[0] * num_objects]` is the correct representation for a 1xN grid.
    # If num_objects is 0, it will produce `[[]]`. If the requirement is truly an empty list `[]`
    # for 0 objects, we add a check. Let's assume `[[]]` is fine for now.
    
    # Correction: A 1xN grid is `[[val1, val2, ..., valN]]`.
    # A 1x0 grid should probably be `[]` (no rows) or `[[]]` (one empty row).
    # Given the examples are 1x3, 1x4, etc., `[[0]*N]` seems right.
    # If N=0, `[[0]*0]` becomes `[[]]`. Let's refine this slightly.
    if num_objects == 0:
         output_grid = [] # Represent a 0-width grid as an empty list of rows
    else:
         output_grid = [[background_color] * num_objects] # Create a 1xN grid

    return output_grid