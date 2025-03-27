```python
"""
1.  **Input Grouping:** Divide the input grid into non-overlapping 3x3 blocks, starting from the top-left corner (0,0), and moving in steps of 3.
2.  **Color Presence:** For each 3x3 block, check if there are *any* non-zero colors present.
3.  **Output Grid Creation:** Create an output grid with dimensions equal to the input grid dimensions divided by 3 (integer division).
4.  **Output Population:**
    *   For each 3x3 block in the input:
        *   Calculate corresponding output position (row index // 3, column index // 3).
        *   If the 3x3 block contains *any* non-zero colors, copy non-zero colors of the 3x3 block into the output grid.
"""

import numpy as np

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # Create output grid
    output_rows = rows // 3
    output_cols = cols // 3
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Iterate through 3x3 blocks (non-overlapping)
    for i in range(0, rows - rows % 3, 3):
        for j in range(0, cols - cols % 3, 3):
            # Define the 3x3 block
            block = input_grid[i:i+3, j:j+3]

            # Check for non-zero colors
            if np.any(block != 0):
                # Determine output position
                output_row = i // 3
                output_col = j // 3
                
                #find the first non zero element of block
                non_zero_elements = block[block != 0]
                if non_zero_elements.size > 0:
                   output_grid[output_row,output_col] = non_zero_elements[0]


    return output_grid.tolist()
```