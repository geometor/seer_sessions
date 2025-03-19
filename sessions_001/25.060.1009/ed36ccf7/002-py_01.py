"""
The transformation can be described as a 90-degree clockwise rotation of a specific subset of the input grid data, namely values that form a colored cross.

1.  **Identify the "colored cross":** Find the positions where non-zero value exists and is not equal to the value in the center of input, and create an image that contains a "colored cross" by swapping this non-zero value with values equal to the value in the center of the input.

2.  **Rotate:** Rotate only the elements in the colored cross 90 degrees clockwise. The center cell and any cell who's initial value is equal to the initial value of center remains unchanged.

3. **Construct Output:** Create output grid from the data in step 2.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by rotating a "colored cross" 90 degrees clockwise.
    """
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    center_value = input_grid[rows // 2, cols // 2]

    # Identify the "colored cross" elements (non-zero and not equal to center)
    cross_elements = []
    for i in range(rows):
        for j in range(cols):
            if input_grid[i, j] != center_value:
                cross_elements.append((i, j))

    # Rotate the cross elements 90 degrees clockwise
    for i, j in cross_elements:
        new_i, new_j = j, rows - 1 - i
        output_grid[new_i, new_j] = input_grid[i,j]
        if (new_i,new_j) not in cross_elements:
          output_grid[i,j]=center_value


    return output_grid.tolist()