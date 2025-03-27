```python
"""
Transforms a 12x6 input grid into a 3x6 output grid by combining four stacked 3x6 subgrids.
The input grid is treated as four stacked 3x6 subgrids.
For each cell (r, c) in the output grid, its color is determined by checking the corresponding stack of cells
in the input subgrids: input[r, c], input[r+3, c], input[r+6, c], and input[r+9, c].
The output color priority rule is:
1. If the bottom-most pixel in the stack (input[r+9, c]) is Azure (8), the output color is Azure (8).
2. Otherwise, the output color is the color of the first non-white (non-zero) pixel encountered when searching the stack from top to bottom: input[r, c], input[r+3, c], input[r+6, c], input[r+9, c].
3. If all four corresponding input cells are white, the output cell remains white (0).
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the described transformation rule to the input grid.
    """

    # Get input dimensions
    input_height, input_width = input_grid.shape

    # Calculate output dimensions (assuming input height is divisible by 4)
    output_height = input_height // 4
    output_width = input_width

    # Initialize the output grid with white (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each cell of the *output* grid
    for r in range(output_height):
        for c in range(output_width):
            # Identify the stack of four corresponding input pixels
            p1 = input_grid[r, c]
            p2 = input_grid[r + output_height, c]       # Corresponds to r + 3
            p3 = input_grid[r + 2 * output_height, c]   # Corresponds to r + 6
            p4 = input_grid[r + 3 * output_height, c]   # Corresponds to r + 9

            # Apply the priority rule
            # Rule 1: Check if the bottom-most pixel (p4) is Azure (8)
            if p4 == 8:
                output_grid[r, c] = 8
            # Rule 2: Otherwise, find the first non-white pixel from top to bottom
            elif p1 != 0:
                output_grid[r, c] = p1
            elif p2 != 0:
                output_grid[r, c] = p2
            elif p3 != 0:
                output_grid[r, c] = p3
            # Rule 2 continued: If p1, p2, p3 were white, use p4 (could be non-8 color or white)
            else:
                output_grid[r, c] = p4
            # Rule 3 (Implicit): If all p1, p2, p3, p4 are 0, the initial value of 0 remains.

    return output_grid
```