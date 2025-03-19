# 8eb1be9a • 004 • example_1 • investigate_coder

---
```python
"""
The transformation takes the azure "drawing" from the input and replicates it vertically three times with a single blank spacer. The resulting output has the pattern stacked into three sections.
"""

import numpy as np

def get_azure_rows(grid):
    # Find rows that contain azure (8) pixels.
    azure_rows = []
    for i, row in enumerate(grid):
        if 8 in row:
            azure_rows.append(i)
    return azure_rows

def extract_azure_pattern(grid, row_indices):
    # Extract the azure pixels and their column indices from the given rows.
    patterns = []
    for row_index in row_indices:
        row = grid[row_index]
        pattern = []
        for col_index, pixel in enumerate(row):
            if pixel == 8:
                pattern.append(col_index)
        patterns.append(pattern)

    return patterns
    

def transform(input_grid):
    # Convert input grid to a NumPy array for easier manipulation.
    input_grid = np.array(input_grid)
    
    # Get the height (number of rows) of the input grid.
    height = input_grid.shape[0]

    # Initialize the output grid as a 2D array of zeros with the same dimensions as the input.
    output_grid = np.zeros_like(input_grid)
    output_grid = np.tile(output_grid,(3,1))

    # Find rows that contain azure (8) pixels.
    azure_rows = get_azure_rows(input_grid)
    
    #Extract patterns
    patterns = extract_azure_pattern(input_grid, azure_rows)

    # replicate patterns into the output grid
    
    output_row = 0
    for pattern in patterns:
        for i in range(3): # do it 3 times
            for col_index in pattern:
                output_grid[output_row, col_index] = 8

            output_row += 1 #next row


    return output_grid
```
