"""
The transformation rule is as follows:

1.  **Determine Output Dimensions:** The output grid has the same width as the input grid. The output grid's height is three times the height of the input grid.
2.  **Replicate Rows:** Each row in the input grid is copied to the output grid three times in sequence. That is:
     *   Input row 1 is copied to output rows 1, 2, and 3.
     *   Input row 2 (if it exists) is copied to output rows 4, 5, and 6.
     *   Input row 3 (if it exists) is copied to output rows 7, 8, and 9 and so on.
3. **Maintain color:** The copied rows retain original color values.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    input_height, input_width = input_grid.shape
    output_height = input_height * 3
    output_width = input_width

    # Initialize the output grid with the calculated dimensions.
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through the input rows and replicate each three times.
    for i in range(input_height):
        for j in range(3):
            output_grid[i * 3 + j] = input_grid[i]

    return output_grid