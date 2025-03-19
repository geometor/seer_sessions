"""
1.  **Initialization:** Create an output grid initially filled with gray (5).

2.  **Connected Component Check:** Identify all pixels in the input grid. For each *non-gray* pixel, check if it's part of a connected component of the *same* color. A connected component is a group of two or more orthogonally contiguous (adjacent up, down, left, or right, but not diagonally) pixels with the same color.

3.  **Expansion:** If a non-gray pixel is part of a connected component of size greater than 1, then expand it into a 3x3 block of the *same* color in the output grid, centered at the original pixel's location. The expansion should *not* overwrite existing colors in the output.

4.  **Singular Pixel Handling:** If a non-gray pixel is *not* part of a connected component (i.e. it is isolated or has a count of only 1) then in the output grid, that pixel becomes *gray*.

5. **Gray Pixel Handling**: Gray pixels in the input are unchanged, and are overridden when non-grey pixels are expanded into their area.

6. **Output:** Return the output grid.
"""

import numpy as np
from collections import deque

def get_connected_component(grid, start_row, start_col, color):
    """Finds a connected component of a given color using Breadth-First Search (BFS)."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    queue = deque([(start_row, start_col)])
    component = []

    while queue:
        row, col = queue.popleft()
        if (0 <= row < rows and 0 <= col < cols and
                grid[row, col] == color and not visited[row, col]):
            visited[row, col] = True
            component.append((row, col))
            # Add orthogonal neighbors
            queue.append((row + 1, col))
            queue.append((row - 1, col))
            queue.append((row, col + 1))
            queue.append((row, col - 1))
    return component

def transform(input_grid):
    """Transforms the input grid according to the defined rule."""

    rows, cols = input_grid.shape
    output_grid = np.full((rows, cols), 5)  # Initialize with gray (5)

    processed = np.zeros((rows, cols), dtype=bool) # track what has been processed

    for i in range(rows):
        for j in range(cols):
            if not processed[i,j]:
                if input_grid[i, j] != 5:
                    # Connected Component Check
                    component = get_connected_component(input_grid, i, j, input_grid[i, j])
                    
                    if len(component) > 1:
                        # Expansion
                        for r, c in component:
                            processed[r,c] = True #mark as processed
                            for x in range(max(0, r - 1), min(rows, r + 2)):
                                for y in range(max(0, c - 1), min(cols, c + 2)):
                                    if output_grid[x,y] == 5: #only change if it hasn't been set
                                        output_grid[x, y] = input_grid[i, j]
                    else:
                        # Singular Pixel Handling, must be processed here.
                        output_grid[i,j] = 5 #set to grey
                        processed[i,j] = True
                else:
                    #grey pixel handling
                    processed[i,j] = True

    return output_grid