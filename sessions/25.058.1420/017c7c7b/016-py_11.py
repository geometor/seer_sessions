"""
1.  **Initialization:** Begin with the input grid.
2.  **Color Substitution:**  Identify all rows containing blue (1) pixels. Change all blue pixels on these rows to red (2).
3.  **Vertical Expansion:** For each row that contained a blue pixel (now red), insert a new row of all white (0) pixels immediately *below* it.
4. **Output:** output is the final grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows_to_duplicate = []

    # Color Substitution: change blue to red and identify rows for duplication
    for i in range(output_grid.shape[0]):
        if 1 in output_grid[i]:
            rows_to_duplicate.append(i)
            for j in range(output_grid.shape[1]):
                if output_grid[i, j] == 1:
                    output_grid[i, j] = 2

    # Vertical Expansion: Insert blank rows below rows with blue (now red) pixels
    expanded_grid = []
    for i in range(output_grid.shape[0]):
        expanded_grid.append(output_grid[i])
        if i in rows_to_duplicate:
            expanded_grid.append(np.zeros(output_grid.shape[1], dtype=int)) #insert blank row

    output_grid = np.array(expanded_grid)
    return output_grid