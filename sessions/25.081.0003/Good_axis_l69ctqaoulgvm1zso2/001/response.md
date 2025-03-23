```python
"""
Replaces white pixels in columns with azure pixels based on the position of a horizontal line of red and azure pixels.
"""

import numpy as np

def find_control_row(grid):
    # Find the row that is all red except for possibly the last element.
    rows, cols = grid.shape
    for r in range(rows):
        if np.all(grid[r, :-1] == 2) and grid[r,-1] !=0 and len(np.unique(grid[r,:]))==2:
            return r
    return -1

def find_all_white_columns(grid):
    #find columns that are all white
    rows, cols = grid.shape
    white_cols = []
    for c in range(cols):
        if np.all(grid[:,c] == 0):
            white_cols.append(c)

    return white_cols

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    grid = np.array(input_grid)  # Convert to NumPy array for easier manipulation
    rows, cols = grid.shape
    output_grid = np.copy(grid)  # Initialize output_grid as a copy of input_grid

    control_row_index = find_control_row(grid)
    
    if control_row_index != -1:
        white_cols = find_all_white_columns(grid)
        # Apply the replacement rule
        for c in range(cols):
            if c in white_cols:
                for r in range(control_row_index):
                    if output_grid[r,c] == 0:
                        
                        for c2 in range(cols):
                            if grid[control_row_index,c2] == 2 and grid[control_row_index:,c] == 8: #find azure in same column as white and red
                                output_grid[r,c]=0 #set intersection of red and white to white
                            elif  grid[control_row_index:,c] != 8: #otherwise put azure if no azure below
                                output_grid[r,c] = 8
                            
    return output_grid.tolist()
```