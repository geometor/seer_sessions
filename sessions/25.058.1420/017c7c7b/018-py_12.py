"""
1.  **Initialization:** Begin with the input grid.
2.  **Color Substitution:** Identify all rows that contain one or more blue (1) pixels. Change all blue pixels in these rows to red (2).
3.  **Conditional Row Insertion:** Iterate through the rows of the grid. If a row contains blue (now red) pixels AND the *following* row *also* contains blue (now red) pixels, insert a new row of all white (0) pixels immediately *below* the current row.
4. **Output:** The final, modified grid is the output.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows_with_blue = []

    # Color Substitution: change blue to red and record rows with blue
    for i in range(output_grid.shape[0]):
        if 1 in output_grid[i]:
            rows_with_blue.append(i)
            for j in range(output_grid.shape[1]):
                if output_grid[i, j] == 1:
                    output_grid[i, j] = 2

    # Conditional Row Insertion
    expanded_grid = []
    for i in range(output_grid.shape[0]):
        expanded_grid.append(output_grid[i])
        if i in rows_with_blue and i + 1 in rows_with_blue:  # Check if current and next row have blue
            expanded_grid.append(np.zeros(output_grid.shape[1], dtype=int)) #insert blank row

    output_grid = np.array(expanded_grid)
    return output_grid