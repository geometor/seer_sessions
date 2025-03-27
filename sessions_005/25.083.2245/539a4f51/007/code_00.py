"""
1. Isolate Input (excluding the last column): From the input grid, create a new grid (`intermediate_grid`) that includes all rows and all columns *except* the last column.
2. Duplicate: Create a copy of `intermediate_grid`.
3. Combine: Horizontally concatenate `intermediate_grid` with its copy, creating a wider grid (`duplicated_grid`). The width of this new grid is twice the width of the `intermediate_grid`.
4. Adjust Height, using input and duplicated grids: The output grid has a fixed height relationship with the input grid - twice the height of the input grid. The final output grid should have the values from duplicated grid repeated to fill twice the height of input grid.
"""

import numpy as np

def transform(input_grid):
    # Convert input to numpy array
    input_array = np.array(input_grid)

    # 1. Isolate Input (excluding the last column)
    intermediate_array = input_array[:, :-1]

    # 2. Duplicate
    duplicated_array = np.hstack((intermediate_array, intermediate_array))

    # 3. Adjust Height and Combine (already combined in step 2)
    rows, cols = duplicated_array.shape
    output_array = np.vstack((duplicated_array, duplicated_array))
    
    return output_array.tolist()