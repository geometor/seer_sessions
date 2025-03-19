"""
1.  **Duplicate:** For every pixel in the input grid, create a 2x2 block of the same color in the output grid.
2.  **Conditional Mirroring:**
    *   If the input grid has more than one row AND more than one column, perform both horizontal and vertical mirroring of the duplicated grid, followed by horizontal and vertical concatenation as in the initial program.
    *   If the input grid has only one row, perform only horizontal mirroring of the duplicated grid, and horizontal concatenation (no vertical mirroring).
    *   If the input grid has only one column, perform only vertical mirroring of the duplicated grid, and vertical concatenation (no horizontal mirroring).
3. **Concatenation**:
    * The duplicated blocks are concatenated with their mirrored counterparts
"""

import numpy as np

def transform(input_grid):
    # Create a numpy array from the input grid
    input_array = np.array(input_grid)

    # Get the dimensions of the input grid
    rows, cols = input_array.shape

    # 1. Duplicate each cell to create a 2x2 block.
    duplicated_array = np.repeat(np.repeat(input_array, 2, axis=0), 2, axis=1)

    # 2. Conditional Mirroring.
    if rows > 1 and cols > 1:
        # Both horizontal and vertical mirroring.
        mirrored_horizontal = np.fliplr(duplicated_array)
        intermediate_result = np.hstack((duplicated_array, mirrored_horizontal))
        mirrored_vertical = np.flipud(intermediate_result)
        output_array = np.vstack((intermediate_result, mirrored_vertical))
    elif rows == 1:
        # Only horizontal mirroring.
        mirrored_horizontal = np.fliplr(duplicated_array)
        output_array = np.hstack((duplicated_array, mirrored_horizontal))
    elif cols == 1:
        # Only vertical mirroring.
        mirrored_vertical = np.flipud(duplicated_array)
        output_array = np.vstack((duplicated_array, mirrored_vertical))

    return output_array.tolist()