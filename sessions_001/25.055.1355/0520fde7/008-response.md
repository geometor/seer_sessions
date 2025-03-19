# 0520fde7 • 008 • example_2 • investigate_coder

---
```python
"""
1.  **Identify the Center:** Locate the vertical line of gray (value 5) pixels in the input grid. This line serves as a vertical center marker.
2.  **Extract Subgrid:** Extract a 3x3 subgrid centered around the identified gray line. Specifically, take the pixels one column to the left and one column to the right of the center column, and all three rows.
3.  **Recolor:** Within the extracted 3x3 subgrid, change all blue (value 1) pixels to red (value 2). Leave white (value 0) unchanged.
4. **Output:** present extracted and recolored subgrid.
"""

import numpy as np

def find_gray_column(grid):
    # Find the column index of the gray (5) line
    rows, cols = grid.shape
    for j in range(cols):
        if all(grid[:, j] == 5):
            return j
    return -1  # Return -1 if no gray column is found

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find center column index
    center_col = find_gray_column(input_grid)

    # Initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Handle if no gray column exists
    if center_col == -1 :
        rows, cols = input_grid.shape
        if(rows >= 3 and cols >= 3):
            output_grid = input_grid[0:3, 0:3].copy()
            output_grid[input_grid[0:3, 0:3] == 1] = 2
            return output_grid
        else:
          return input_grid

    # Extract 3x3 subgrid
    start_col = max(0, center_col - 1)
    end_col = min(input_grid.shape[1], center_col + 2)
    
    subgrid = input_grid[:, start_col:end_col]

    if subgrid.shape[1] < 3:
        padding = 3- subgrid.shape[1]
        pad_left = padding //2
        pad_right = padding - pad_left
        
        subgrid = np.pad(subgrid, ((0,0),(pad_left, pad_right)), mode='constant', constant_values=0 )
    
    output_grid = subgrid.copy()


    # Recolor blue (1) to red (2)
    output_grid[output_grid == 1] = 2

    return output_grid
```
