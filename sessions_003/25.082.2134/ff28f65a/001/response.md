```python
"""
Detects 2x2 red blocks in pairs of input rows and represents their presence with '1's in a 3x3 (or smaller) output grid.
"""

import numpy as np

def find_red_blocks(input_grid):
    """Finds all 2x2 blocks of red (value 2) pixels in the input grid."""
    red_blocks = []
    for r in range(input_grid.shape[0] - 1):
        for c in range(input_grid.shape[1] - 1):
            if (input_grid[r, c] == 2 and input_grid[r + 1, c] == 2 and
                input_grid[r, c + 1] == 2 and input_grid[r + 1, c + 1] == 2):
                red_blocks.append((r, c))  # Store the top-left corner coordinates
    return red_blocks

def transform(input_grid):
    """Transforms the input grid according to the defined rule."""
    input_grid = np.array(input_grid)
    output_grid = np.zeros((3, 3), dtype=int)
    output_rows = []

    for i in range(0, input_grid.shape[0], 2):  # Iterate through pairs of rows
        output_row = []
        
        #Check that the row actually exists.
        if(i+1 < input_grid.shape[0]):
            combined_rows = np.vstack((input_grid[i], input_grid[i+1]))
        else:
            combined_rows = np.array([input_grid[i]])

        red_blocks = find_red_blocks(combined_rows) #find in two rows.

        # Populate based on length of combined rows.
        row_idx = 0
        for j in range(0, combined_rows.shape[1], 2):
            block_present = False
            for r, c in red_blocks:
               if(j <= c < j + 2): # check if block in current group
                   block_present = True
                   break

            if block_present:
                output_row.append(1)
            else:
                 output_row.append(0)

        output_rows.append(output_row)

    # Convert to numpy and trim.
    max_width = 0
    for row in output_rows:
        max_width = max(max_width, len(row))
    
    max_width = min(3, max_width) # limit
    
    final_grid = np.zeros((3, max_width), dtype=int)

    for i, row in enumerate(output_rows):
        for j in range(min(len(row), max_width)):
            final_grid[i,j] = row[j]

    return final_grid.tolist()
```