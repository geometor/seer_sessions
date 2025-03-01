# 3428a4f5 • 002 • example_4 • investigate_coder

---
```python
"""
1.  **Identify** the horizontal line of yellow (4) pixels in the input grid. This line acts as a delimiter.
2.  **Consider** only the grid of pixels *above* the yellow line.
3.  **Transform** all red (2) pixels in this region to green (3).
4.  **Transform** a *subset* of white (0) pixels to green (3). White becomes
    green *only if* the white is immediately diagonally or adjacent to a green
    (previously red) pixel.
5.  **Output** this transformed region above the yellow line as a new grid. The yellow row, and everything below it, is discarded.
"""

import numpy as np

def find_yellow_line(grid):
    """Finds the row index of the horizontal yellow line."""
    for i, row in enumerate(grid):
        if all(pixel == 4 for pixel in row):
            return i
    return -1  # Should not happen in valid input

def transform(input_grid):
    """Transforms the input grid according to the rules."""
    input_grid = np.array(input_grid)
    yellow_line_row = find_yellow_line(input_grid)

    # Consider only the region above the yellow line
    output_grid = input_grid[:yellow_line_row].copy()

     # Transform red to green
    output_grid[output_grid == 2] = 3
    
    # Get dimensions of the output region
    rows, cols = output_grid.shape
    
    # Create a copy to store the final changes to propagate green
    final_output_grid = output_grid.copy()

    # Iterate to propagate green to adjacent whites
    while True:
        changed = False
        temp_grid = final_output_grid.copy()
        for r in range(rows):
            for c in range(cols):
                if temp_grid[r, c] == 0:  # If white
                    # Check neighbors (including diagonals)
                    for i in range(max(0, r - 1), min(rows, r + 2)):
                        for j in range(max(0, c - 1), min(cols, c + 2)):
                            if temp_grid[i, j] == 3:  # If neighbor is green
                                final_output_grid[r, c] = 3  # Change white to green
                                changed = True
                                break
                        if changed:
                            break
        if not changed:  # if no change to the grid
            break
    
    return final_output_grid.tolist()
```
