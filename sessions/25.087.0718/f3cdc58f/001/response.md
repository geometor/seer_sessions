```python
"""
This module transforms an input grid based on the counts of specific colors (1, 2, 3, 4).
It counts the occurrences of blue (1), red (2), green (3), and yellow (4) pixels in the input grid.
Based on these counts, it constructs vertical columns in the output grid.
The output grid is initialized to all white (0).
A blue column is drawn in column 0, with height equal to the count of blue pixels in the input.
A red column is drawn in column 1, with height equal to the count of red pixels.
A green column is drawn in column 2, with height equal to the count of green pixels.
A yellow column is drawn in column 3, with height equal to the count of yellow pixels.
All columns are bottom-aligned, starting from the last row and extending upwards.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by counting specific colors (1, 2, 3, 4) and drawing
    corresponding, bottom-aligned columns in the output grid.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input list of lists to a numpy array for efficient operations
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize output_grid with the same dimensions as input, filled with white (0)
    output_np = np.zeros((height, width), dtype=int)

    # Define the target colors and their corresponding output column indices
    color_to_column = {
        1: 0,  # blue -> column 0
        2: 1,  # red -> column 1
        3: 2,  # green -> column 2
        4: 3,  # yellow -> column 3
    }

    # Iterate through the target colors
    for color, col_idx in color_to_column.items():
        # Count the occurrences of the current color in the input grid
        count = np.count_nonzero(input_np == color)

        # If the color exists in the input grid
        if count > 0:
            # Calculate the start row for the column (bottom-aligned)
            # Ensure start_row is not negative if count exceeds height (though ARC grids are max 30x30)
            start_row = max(0, height - count)

            # Fill the corresponding column in the output grid with the color
            # from start_row down to the last row (height - 1)
            output_np[start_row:height, col_idx] = color

    # Convert the numpy array back to a list of lists for the expected output format
    output_grid = output_np.tolist()

    return output_grid
```