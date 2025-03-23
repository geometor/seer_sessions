"""
1.  **Initialization:** Create an output grid of the same dimensions as the input grid, initially filled with zeros.

2.  **Row Iteration:** Iterate through the rows of the input grid from top to bottom (index `i` from 0 to rows - 1).

3.  **Adjacent Row Comparison:** compare row `i` with row `i+1`.

4.  **Uniform Rows:** If all elements within row `i` and `i+1` of the input grid are identical, fill the entire row `i` of the *output* grid with the value 5.

5. **Non-uniform rows and Alternating Diagonals:**
    *   If a row has non-uniform elements (mix of colors) *and* is different from the following row, the output grid will have a '5' placed diagonally.
    *   The diagonals alternate.  If `i` is even, the '5' is placed at `output_grid[i][i]`. If `i` is odd, the '5' is placed at `output_grid[i][rows - 1 - i]`.

6.  **Zero Padding:**  After processing all rows, any remaining cells in the output grid that have not been assigned a value (i.e., are still 0) remain 0.
"""

import numpy as np

def _is_row_uniform(row):
    """Checks if all elements in a row are identical."""
    return np.all(row == row[0])

def transform(input_grid):
    # Initialize output_grid with zeros
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Iterate through rows
    for i in range(rows):
        # Adjacent Row Comparison (handle last row separately)
        if i < rows - 1:
            adjacent_rows_same = np.array_equal(input_grid[i], input_grid[i+1])
            current_row_uniform = _is_row_uniform(input_grid[i])
            next_row_uniform = _is_row_uniform(input_grid[i+1])

            # Uniform Rows: fill row i with 5s if current and next row are uniform and same
            if current_row_uniform and next_row_uniform and adjacent_rows_same:
                output_grid[i, :] = 5

            # Alternating Diagonals
            elif not adjacent_rows_same :
                if i % 2 == 0:
                    output_grid[i, i] = 5
                else:
                    output_grid[i, rows - 1 - i] = 5
        
        #handle last row - diagonal
        else:
          if i % 2 == 0:
            output_grid[i,i] = 5
          else:
            output_grid[i, rows - 1 - i] = 5

    return output_grid