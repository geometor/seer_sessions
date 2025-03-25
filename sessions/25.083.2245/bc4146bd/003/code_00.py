"""
The transformation rule is as follows:

1.  **Column Pairing:** The input grid is divided into pairs of columns. The first pair consists of columns 0 and 1, and the second pair consists of columns 2 and 3.

2.  **Concatenation:** Within each pair, the columns are concatenated vertically.  This creates two new, longer "column" vectors, each with a length twice the height of the original grid.

3.  **Row Construction:** Each row of the output grid is constructed by a specific method based on rows of the input grid:
  - the input row and paired input row of the next column are combined.
  - for a 4 x 4 input grid, each of the column-paired sets are 8 values in length
  - the output row is formed by interleaving values from these column-paired sets:
    - take values 0, 1, 2, 3, and 4 from each column-paired input set, repeating 5 values from input set

4.  **Output Dimensions:** The output grid has the same height as the input grid, but its width is five times the input width.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid
    input_height, input_width = input_grid.shape
    output_height = input_height
    output_width = input_width * 5
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through rows
    for row_index in range(input_height):
        # Column Pairing and Concatenation
        combined_cols = []
        for col_index in range(0, input_width, 2):
          combined = np.concatenate((input_grid[:, col_index], input_grid[:,col_index+1]))
          combined_cols.append(combined)

        # Row construction with interleaving
        output_row = []

        set1 = combined_cols[0]
        set2 = combined_cols[1]

        output_row.extend(set1[row_index].repeat(5))
        output_row.extend(set2[row_index].repeat(5))

        output_grid[row_index] = np.array(output_row)


    return output_grid