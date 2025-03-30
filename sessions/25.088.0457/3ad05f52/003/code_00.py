import numpy as np
from collections import deque

"""
Transformation Rule:

1. Identify the boundary color (Azure, 8), the background color (White, 0), and the fill color (the single color present in the input grid that is neither White nor Azure).
2. Create a copy of the input grid to serve as the output grid.
3. Find all pixels in the input grid that initially have the fill color. These locations act as "seeds" for the fill operation.
4. Initialize a queue for a Breadth-First Search (BFS) and add all seed locations to it.
5. Initialize a 'visited' set or boolean array to keep track of pixels added to the queue or processed, initially containing the seed locations. Mark the seed locations as the fill color in the output grid (they already are, but this ensures consistency).
6. While the queue is not empty:
    a. Dequeue a pixel location (r, c).
    b. Check its four adjacent neighbors (up, down, left, right).
    c. For each neighbor (nr, nc):
        i. Check if the neighbor is within the grid boundaries.
        ii. Check if the neighbor's color in the *input* grid is the background color (White, 0).
        iii. Check if the neighbor has *not* been visited yet.
        iv. If all conditions are met:
            - Mark the neighbor as visited.
            - Change the neighbor's color in the *output* grid to the fill color.
            - Enqueue the neighbor's location (nr, nc).
7. Return the modified output grid.

This process effectively performs a flood fill starting from all initial fill color pixels, spreading only to adjacent white pixels and stopping at azure boundaries (because the check in 6.c.ii fails for azure pixels) or other non-white pixels.
"""

def transform(input_grid):
    """
    Fills white regions adjacent to existing fill-color pixels within azure boundaries.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    rows, cols = grid.shape

    # --- Identify boundary, background, and fill colors ---
    boundary_color = 8 # Azure
    background_color = 0 # White
    
    # Find the unique fill color (not 0 or 8)
    unique_colors = np.unique(grid)
    fill_color = -1 # Initialize with an invalid color
    for color in unique_colors:
        if color != background_color and color != boundary_color:
            fill_color = color
            break
    
    # If no specific fill color is found besides white and azure, 
    # there might be nothing to fill, return the original grid.
    # (Examples show a fill color is always present when changes occur).
    if fill_color == -1:
        # Check if any white pixels exist at all. If not, still return original.
        # This handles cases where the grid might only contain boundary/background
        # or is entirely one color. Although unlikely based on examples.
         if background_color not in unique_colors:
             return output_grid.tolist()
         # If only background and boundary exist, technically no fill color is defined.
         # However, the logic might imply filling *everything* not connected to outside.
         # Let's stick to the "fill from seed" rule for now. If no seed, no fill.
         return output_grid.tolist()


    # --- Initialize BFS queue and visited set/array ---
    queue = deque()
    visited = np.zeros_like(grid, dtype=bool)

    # Find all initial fill color pixels ("seeds") and add them to the queue
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == fill_color:
                if not visited[r, c]: # Should always be false here initially, but good practice
                    queue.append((r, c))
                    visited[r, c] = True
                    # Ensure the seed locations are colored in the output (they should be already)
                    output_grid[r, c] = fill_color 

    # --- Perform BFS (Flood Fill) ---
    while queue:
        r, c = queue.popleft()

        # Check neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if neighbor is background color (White) in the *original* grid
                # and hasn't been visited yet.
                if grid[nr, nc] == background_color and not visited[nr, nc]:
                    visited[nr, nc] = True
                    output_grid[nr, nc] = fill_color # Change color in output
                    queue.append((nr, nc)) # Add to queue to explore its neighbors

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()