```python
import numpy as np
from collections import deque

"""
Perform a flood fill transformation starting from the single red pixel (2) in the input grid.

1.  Identify the single red pixel in the input grid; this is the starting point for the transformation.
2.  Perform a flood fill operation starting from this red pixel.
3.  The flood fill spreads only to orthogonally adjacent white pixels (0).
4.  The flood fill is blocked by azure pixels (8) and the boundaries of the grid. Azure pixels remain unchanged.
5.  All white pixels reachable by the flood fill (without crossing azure pixels or grid boundaries) change their color to red (2).
6.  The original starting red pixel remains red.
7.  White pixels that are not reachable by the flood fill remain white.
8.  The final output grid contains the original azure pixels, the original red pixel, the newly filled red pixels, and the remaining white pixels.
"""

def find_start_pixel(grid: np.ndarray, color: int) -> tuple[int, int] | None:
    """Finds the coordinates (row, col) of the first pixel with the specified color."""
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                return (r, c)
    return None # Should not happen in this task if a start pixel always exists

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies a flood fill transformation starting from the red pixel (2),
    filling adjacent white pixels (0) until blocked by azure pixels (8)
    or grid boundaries.
    """
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Define the colors involved in the transformation
    fill_color = 2  # Red - the color to fill with and the start pixel color
    background_color = 0 # White - the color of pixels to be filled
    barrier_color = 8 # Azure - the color that blocks the fill

    # 1. Find the starting red pixel coordinates
    start_coord = find_start_pixel(input_grid, fill_color)
    
    # If no starting pixel is found, return the original grid (edge case)
    if start_coord is None:
        print("Warning: No start pixel (red=2) found.")
        return output_grid 

    # 2. Initialize data structures for Breadth-First Search (BFS) flood fill
    # Queue stores coordinates (row, col) to be processed
    queue = deque([start_coord])
    # Set to keep track of visited coordinates to prevent infinite loops and re-processing
    visited = set([start_coord])

    # Define the four orthogonal directions (change in row, change in col)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Right, Left, Down, Up

    # 3. Start the flood fill process
    while queue:
        # Get the current coordinate from the front of the queue
        r, c = queue.popleft()

        # The starting pixel itself is already the correct color (red),
        # so we mainly process it to find its neighbors.

        # 4. Explore orthogonal neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc # Calculate neighbor coordinates

            # Check if the neighbor is within the grid boundaries
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbor_coord = (nr, nc)
                
                # Check if the neighbor has already been visited
                if neighbor_coord not in visited:
                    # Mark the neighbor as visited *before* checking its color
                    visited.add(neighbor_coord) 
                    
                    # Check the neighbor's color in the *original* input grid
                    neighbor_color = input_grid[nr, nc]

                    # 5. If the neighbor is a white pixel, fill it and add to queue
                    if neighbor_color == background_color:
                        output_grid[nr, nc] = fill_color # Change color in output
                        queue.append(neighbor_coord) # Add to queue for further exploration
                        
                    # 6. If the neighbor is a barrier (azure) or already the fill color (red), 
                    # it stops the fill in this direction, but we've already marked it visited.
                    # No further action needed for these pixels.
                    
                    # Implicitly, if the neighbor is any other color, it also acts as a barrier
                    # and is ignored after being marked visited.

    # 8. Return the modified grid
    return output_grid
```