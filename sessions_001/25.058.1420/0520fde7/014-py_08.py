"""
1.  **Identify Target Columns:** Examine each column in the input grid. A column is a target column if it contains at least one pixel with the value '1' (blue), '2' (red), or '8' (azure).
2.  **Extract Target Columns:** Create a new grid consisting of only the target columns, preserving their original order from the input grid.
3.  **Transform Colors:** Within the extracted columns, apply the following color transformations:
    *   If a pixel is '1' (blue), change it to '2' (red).
    *   If a pixel is '2' (red), change it to '0' (white).
    *   If a pixel is '8' (azure), change it to '2' (red).
    *   If a pixel is '5' (gray), change it to '0' (white)
    *   All other colors remain unchanged.
"""

import numpy as np

def _identify_target_columns(input_array):
    """Identifies target columns based on the presence of 1, 2, or 8."""
    rows, cols = input_array.shape
    target_columns = []
    for j in range(cols):
        if 1 in input_array[:, j] or 2 in input_array[:, j] or 8 in input_array[:, j]:
            target_columns.append(j)
    return target_columns

def _transform_colors(extracted_array):
    """Applies color transformations to the extracted array."""
    output_array = extracted_array.copy()
    for i in range(output_array.shape[0]):
        for j in range(output_array.shape[1]):
            if output_array[i, j] == 1:
                output_array[i, j] = 2
            elif output_array[i, j] == 2:
                output_array[i, j] = 0
            elif output_array[i, j] == 8:
                output_array[i, j] = 2
            elif output_array[i, j] == 5:
                output_array[i, j] = 0
    return output_array

def transform(input_grid):
    """
    Transforms the input grid to the output grid based on the observed rules.
    """
    input_array = np.array(input_grid)

    # 1. Identify Target Columns
    target_columns = _identify_target_columns(input_array)

    # 2. Extract Target Columns
    extracted_array = input_array[:, target_columns]

    # 3. Transform Colors
    output_array = _transform_colors(extracted_array)

    return output_array.tolist()