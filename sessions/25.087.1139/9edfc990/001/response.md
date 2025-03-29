```python
import numpy as np
from collections import deque

"""
Identifies connected regions of white pixels (color 0) in the input grid.
If a connected region of white pixels is entirely enclosed (i.e., none of its pixels touch the border of the grid),
then all pixels in that region are changed to blue (color 1) in the output grid.
If a connected region of white pixels touches the border of the grid at any point,
all pixels in that region remain white (color 0) in the output grid.
All non-white pixels remain unchanged.
"""

def transform(input_grid):
    """
    Transforms the input grid by filling enclosed white regions with blue.

    Args:
        input_grid (list of lists or numpy array): The input grid.

    Returns:
        numpy array: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()  # Initialize output grid as a copy of input
    height, width = grid.shape
    
    # Keep track of visited white pixels to avoid reprocessing
    visited = np.zeros_like(grid, dtype=bool)

    # Iterate through each pixel of the grid
    for r in range(height):
        for c in range(width):
            # Check if the pixel is white (0) and hasn't been visited yet
            if grid[r, c] == 0 and not visited[r, c]:
                # Start a search (BFS) to find the connected component of white pixels
                component_pixels = []
                touches_border = False
                queue = deque([(r, c)])
                visited[r, c] = True # Mark starting pixel as visited

                while queue:
                    curr_r, curr_c = queue.popleft()
                    component_pixels.append((curr_r, curr_c))

                    # Check if the current pixel is on the border
                    if curr_r == 0 or curr_r == height - 1 or curr_c == 0 or curr_c == width - 1:
                        touches_border = True

                    # Explore neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        next_r, next_c = curr_r + dr, curr_c + dc

                        # Check if the neighbor is within grid bounds
                        if 0 <= next_r < height and 0 <= next_c < width:
                            # Check if the neighbor is white and not visited
                            if grid[next_r, next_c] == 0 and not visited[next_r, next_c]:
                                visited[next_r, next_c] = True # Mark neighbor as visited
                                queue.append((next_r, next_c)) # Add neighbor to queue

                # After finding the whole component, check if it touched the border
                if not touches_border:
                    # If the component did not touch the border, change its pixels to blue (1)
                    for px_r, px_c in component_pixels:
                        output_grid[px_r, px_c] = 1
                # If the component touched the border, its pixels remain white (0),
                # which is already the case in the copied output_grid.

    return output_grid.tolist() # Return as list of lists if needed, otherwise output_grid

```