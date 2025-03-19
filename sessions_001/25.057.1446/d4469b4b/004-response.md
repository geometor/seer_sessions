# d4469b4b • 004 • refine_coder

---
```python
"""
1.  **Determine Output Dimensions:** Calculate the output grid dimensions by subtracting 2 from both the input grid's height and width.
2.  **Iterate Subgrids:** Iterate through all possible 2x2 subgrids within the input grid.  The top-left corners of these subgrids will range from (0,0) up to (height - 2, width - 2).
3.  **Condensation Rule:** For each 2x2 subgrid:
    *   If any pixel within the subgrid is red (value 2), set the corresponding pixel in the output grid to gray (value 5).
    *   If all pixels within the 2x2 subgrid are white (value 0) or any other non-red color, set the corresponding output pixel to white/0.
4.  **Output:** Construct the output grid with the calculated dimensions and filled according to the condensation rule applied to each 2x2 subgrid.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_rows = rows - 2
    output_cols = cols - 2
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Iterate through all possible 2x2 subgrids
    for i in range(output_rows):
        for j in range(output_cols):
            # Extract the 2x2 subgrid
            subgrid = input_grid[i:i+2, j:j+2]

            # Apply the condensation rule
            if 2 in subgrid:
                output_grid[i, j] = 5  # Set to gray
            else:
                output_grid[i, j] = 0  # Set to white

    return output_grid.tolist()
```

