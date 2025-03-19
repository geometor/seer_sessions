"""
1.  **Initialization:** Start with the given input grid.
2.  **Color Substitution:** Iterate through each pixel in the input grid. If a pixel is blue (value 1), change it to red (value 2). If a pixel is white (value 0), it does not change and remains 0.
3. **Vertical Expansion:** Expand the new grid, by repeating each existing row by 1.5, that is, add half as many rows to each row by copying the row content. Since fractions are not possible, the total length can be achieved by tripling the number of original rows and subsequently removing 1/3.
4. The result will be the output grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Color Substitution: change blue to red
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            if output_grid[i, j] == 1:
                output_grid[i, j] = 2

    # Vertical Expansion: Increase height
    expanded_grid = []
    for row in output_grid:
      expanded_grid.append(row)
    
    #add half of the orignal
    num_rows_to_add = len(output_grid) // 2
    for i in range(num_rows_to_add):
      expanded_grid.append(output_grid[i])


    output_grid = np.array(expanded_grid)

    return output_grid