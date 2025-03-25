"""
The transformation rule is as follows:

1.  **Input:** A 4x4 grid of integers (0-9).

2.  **Output Dimensions:** The output grid is 4x20 (height same as input, width is 5 times input width).

3.  **Column Pairing:**  Conceptually pair the columns of the input grid: (column 0 with column 1) and (column 2 with column 3).

4.  **Element Repetition:** The program constructs each output row by using the input row values, repeating each 5 times, and concatenating those sets.

5. **Row Building:**
     - For each row in the output grid, the row is built from each of the values in the paired column sets of the input row.
     - The output row contains 5 instances of the paired elements, concatenated together.

6.  **Output:** The resulting 4x20 grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_height = input_height
    output_width = input_width * 5
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through rows and columns of the input grid.
    for row_index in range(input_height):
        output_row = []
        for col_index in range(input_width):
            # Repeat each element in input 5 times
            output_row.extend([input_grid[row_index, col_index]] * 5)
        output_grid[row_index] = np.array(output_row)
    return output_grid