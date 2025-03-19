"""
1.  **Initialize Output:** Create an output grid of the same width as the input grid. The height will be determined dynamically. Fill the first row of the output grid with black pixels (color 0).

2.  **Identify Repeating Pattern:** Find the largest repeating horizontal color sequence that appears on at least two *adjacent* rows within the input grid. The position of the repeating pattern can be anywhere. Consider horizontal sequences of length 2 or greater.

3.  **Copy Pattern:** Copy the identified repeating color sequence to the second row of the output grid. If the sequence appears at the start of multiple rows of the same width, prefer copying a sequence as wide as possible (leftmost color to the rightmost color of that sequence). Start the copy at the column index where the pattern begins in the input grid. Fill empty spaces with 0.

4.  **Duplicate Rows:** For each row of the identified repeating pattern, create two rows in the output grid, and copy the content to both created rows.

5.  **Repeat duplication:** Do steps 3 and 4 until the output grid has been filled.
"""

import numpy as np

def find_repeating_pattern(input_grid):
    """Finds the largest repeating horizontal sequence across adjacent rows."""
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    max_pattern = []
    max_len = 0
    start_row = -1
    start_col = -1

    for r1 in range(rows - 1):
        for r2 in range(r1 + 1, rows):
            if r2 - r1 > 1: # must be adjacent rows
                continue
            for length in range(2, cols + 1):  # Pattern lengths from 2 to full width
                for c1 in range(cols - length + 1):
                    pattern1 = input_grid[r1, c1:c1+length]
                    for c2 in range(cols - length + 1):
                        pattern2 = input_grid[r2, c2:c2+length]
                        if np.array_equal(pattern1, pattern2):
                            if length > max_len:
                                max_len = length
                                max_pattern = pattern1.tolist()
                                start_row = r1
                                start_col = c1
    return max_pattern, start_row, start_col

def transform(input_grid):
    # Initialize output grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((1, cols), dtype=int) # Start with the black row

    # Identify Repeating Pattern
    pattern, start_row, start_col = find_repeating_pattern(input_grid)

    # Copy Pattern to the second row of output
    if pattern:
        second_row = np.zeros(cols, dtype=int)
        second_row[start_col:start_col + len(pattern)] = pattern
        output_grid = np.vstack([output_grid, second_row.reshape(1, -1)])


    # Duplicate Rows based on pattern
        pattern_rows = []

        for r in range(rows):
          if start_col + len(pattern) <= cols: #check if full pattern can be in this row
            if np.array_equal(input_grid[r, start_col:start_col+len(pattern)], pattern):
                pattern_rows.append(input_grid[r,:])

        for row_data in pattern_rows:
            output_grid = np.vstack([output_grid, row_data.reshape(1,-1)])
            output_grid = np.vstack([output_grid, row_data.reshape(1,-1)])
    else: # case when there is no pattern, copy input
        for r in range(rows):
            output_grid = np.vstack([output_grid, input_grid[r, :]])
            output_grid = np.vstack([output_grid, input_grid[r, :]])



    return output_grid.tolist()