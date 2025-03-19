"""
1.  **Identify Initial Gray Region:** Find the length of the contiguous gray (value 5) region at the beginning of the first row of the input grid. Let this length be `gray_length`.
2.  **Determine Output Height:** The output grid's height is calculated as `gray_length + input_height - 1`.
3.  **Copy First Row:** Copy the first row of the input grid to the first row of the output grid.
4. **Extend the gray region:** For each new row, add a number of gray(5) pixels equal to the index of the output row.
5.  **Copy Remaining Pixels:** Copy the remaining non-gray pixels from the first row of the input grid to the corresponding positions in all new rows.
"""

import numpy as np

def get_gray_length(input_grid):
    """Calculates the length of the initial contiguous gray region in the first row."""
    gray_length = 0
    for pixel in input_grid[0]:
        if pixel == 5:
            gray_length += 1
        else:
            break
    return gray_length

def transform(input_grid):
    input_grid = np.array(input_grid)
    input_height, input_width = input_grid.shape

    # 1. Identify Initial Gray Region
    gray_length = get_gray_length(input_grid)

    # 2. Determine Output Height
    output_height = gray_length + input_height - 1

    # Initialize output_grid
    output_grid = np.zeros((output_height, input_width), dtype=int)

    # 3. Copy First Row
    output_grid[0] = input_grid[0]

    # 4. & 5. Extend and Copy
    for row_index in range(1, output_height):
        # Add gray pixels based on row index
        for i in range(row_index + 1):
          if i < input_width:
            output_grid[row_index, i] = 5

        # copy non-gray pixels
        non_gray_start = gray_length
        if non_gray_start < input_width:
            output_grid[row_index, non_gray_start:] = input_grid[0, non_gray_start:]

    return output_grid