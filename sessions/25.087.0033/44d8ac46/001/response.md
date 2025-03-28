```python
import numpy as np
from collections import deque

"""
Identifies contiguous regions of white (0) pixels that are fully enclosed by gray (5) pixels 
within the input grid. These enclosed white regions are then filled with red (2) in the 
output grid. All other pixels (gray pixels and white pixels not fully enclosed) remain 
unchanged. A white region is considered fully enclosed if it has no path to the grid's 
boundary consisting only of white pixels.
"""

def transform(input_grid):
    """
    Fills enclosed white regions within gray shapes with red.

    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed grid with enclosed white regions filled red.
    """
    
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = np.copy(grid)
    rows, cols = grid.shape

    # Create a boolean grid to track white pixels reachable from the boundary
    is_reachable = np.full((rows, cols), False, dtype=bool)
    
    # Use a queue for Breadth-First Search (BFS)
    queue = deque()

    # Initialize the BFS queue with all white pixels on the boundary
    for r in range(rows):
        for c in [0, cols - 1]: # Left and right columns
            if grid[r, c] == 0 and not is_reachable[r, c]:
                is_reachable[r, c] = True
                queue.append((r, c))
    for c in range(cols):
        for r in [0, rows - 1]: # Top and bottom rows
             # Avoid adding corners twice
            if grid[r, c] == 0 and not is_reachable[r, c]:
                is_reachable[r, c] = True
                queue.append((r, c))

    # Perform BFS to find all white pixels connected to the boundary
    while queue:
        r, c = queue.popleft()

        # Check 4-directional neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if the neighbor is within bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if the neighbor is white and hasn't been reached yet
                if grid[nr, nc] == 0 and not is_reachable[nr, nc]:
                    is_reachable[nr, nc] = True
                    queue.append((nr, nc))

    # Iterate through the grid and change enclosed white pixels to red
    for r in range(rows):
        for c in range(cols):
            # If a pixel is white (0) but was not reached by the BFS, it's enclosed
            if grid[r, c] == 0 and not is_reachable[r, c]:
                output_grid[r, c] = 2 # Change to red

    return output_grid.tolist() # Return as list of lists if needed, or keep as np.ndarray
```