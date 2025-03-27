```python
import numpy as np

"""
Transforms a 12x6 input grid into a 3x6 output grid by combining four stacked 3x6 subgrids.

The input grid is treated as four stacked 3x6 subgrids (rows 0-2, 3-5, 6-8, 9-11).
For each cell (r, c) in the 3x6 output grid, its color is determined by examining the stack of four corresponding cells
in the input subgrids:
p1 = input[r, c]       (top layer)
p2 = input[r+3, c]     (second layer)
p3 = input[r+6, c]     (third layer)
p4 = input[r+9, c]     (bottom layer)

The transformation rule follows these steps:
1. Find the color of the first non-white (non-zero) pixel encountered when scanning the stack from top to bottom (p1 -> p4). Let this color be 'first_color'. If all pixels are white, 'first_color' is white (0).
2. Apply an override rule: If 'first_color' is Red (2) AND the bottom-most pixel in the stack (p4) is Azure (8), then the output pixel color is Azure (8).
3. Default rule: If the override rule does not apply, the output pixel color is 'first_color'.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the described transformation rule to the input grid.
    """

    # Get input dimensions
    input_height, input_width = input_grid.shape

    # Calculate output dimensions
    # Assuming input height is always 4 times the output height
    output_height = input_height // 4
    output_width = input_width

    # Initialize the output grid with white (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Define color constants for clarity
    WHITE = 0
    RED = 2
    AZURE = 8

    # Iterate through each cell of the *output* grid
    for r in range(output_height):
        for c in range(output_width):
            # Identify the stack of four corresponding input pixels
            p1 = input_grid[r, c]
            p2 = input_grid[r + output_height, c]       # Corresponds to r + 3
            p3 = input_grid[r + 2 * output_height, c]   # Corresponds to r + 6
            p4 = input_grid[r + 3 * output_height, c]   # Corresponds to r + 9

            # Step 1: Find the first non-white pixel color from top to bottom
            first_color = WHITE
            if p1 != WHITE:
                first_color = p1
            elif p2 != WHITE:
                first_color = p2
            elif p3 != WHITE:
                first_color = p3
            else:
                # If p1, p2, p3 are white, the 'first' color is whatever p4 is
                # (including white if p4 is also white)
                first_color = p4

            # Step 2: Apply the override rule
            # Check if the first non-white color found was Red AND the bottom layer is Azure
            if first_color == RED and p4 == AZURE:
                output_grid[r, c] = AZURE
            # Step 3: Default rule
            else:
                # Otherwise, the output color is the first non-white color found
                output_grid[r, c] = first_color

    return output_grid
```