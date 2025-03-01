# 673ef223 • 002 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Boundaries:** Locate the vertical red (2) columns on the left and right sides of the grid.

2.  **Horizontal Fill:**
    *   Identify exist azure (8) shape
    *   For each row containing azure pixels, extend those azure pixels horizontally to the left until it meets either a red column or the edge of the grid.
    *   Extend those azure shapes horizontally to the right, changing the color of pixels one by one from white(0) to azure (8) until a red(2) pixel is encountered or edge of the grid.

3.  **Yellow Insertion:**
    *   Find the leftmost azure(8) pixel.
    *    Change the color of pixel at one column to left to Yellow(4), unless azure extends to edge of input, then transform the leftmost azure pixels until a single yellow is present
"""

import numpy as np

def find_red_columns(grid):
    """Finds the leftmost and rightmost red columns."""
    rows, cols = grid.shape
    left_red_col = -1
    right_red_col = -1

    for col in range(cols):
        for row in range(rows):
            if grid[row, col] == 2:
                if left_red_col == -1:
                    left_red_col = col
                right_red_col = col
    return left_red_col, right_red_col

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find red column boundaries
    left_red_col, right_red_col = find_red_columns(input_grid)
    # Horizontal Fill and Yellow Insertion
    for row in range(rows):
        azure_indices = np.where(input_grid[row, :] == 8)[0]
        if azure_indices.size > 0 :
            
            #fill azure to the right
            if right_red_col != -1:
              end = right_red_col
            else:
              end = cols
            
            for col in range(azure_indices[-1] + 1, end):
                output_grid[row, col] = 8

            #fill azure to left
            start = 0 if left_red_col ==-1 else left_red_col+1
            for col in range(azure_indices[0]-1,start-1,-1):
                 output_grid[row,col] = 8

            # find left most azure and insert yellow
            all_azure =  np.where(output_grid[row, :] == 8)[0]
            if all_azure.size > 0:
                leftmost_azure = all_azure[0]
                if leftmost_azure > 0 :
                    output_grid[row, leftmost_azure - 1] = 4
                else :
                    #convert azure until one yellow
                    yellow_count = 0
                    for c in all_azure:
                        if yellow_count == 0:
                            output_grid[row,c] = 4
                            yellow_count+=1
                        else:
                          break
            


    return output_grid
```
