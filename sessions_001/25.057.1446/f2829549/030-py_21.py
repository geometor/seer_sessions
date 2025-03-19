"""
1. Iterate through each of the three columns of the input grid individually.
2. Examine each column.
3. Check: If all the pixels in the input column are the same color, AND that
   color is NOT white (0), then the corresponding output column is all green (3).
4. Otherwise, the corresponding output column is all white (0).
5. Combine: The three resulting columns form the output grid.
"""

import numpy as np

def check_all_same_and_not_white(column):
    """
    Checks if all elements in the column are the same and not white (0).
    """
    first_element = column[0]
    if first_element == 0:
        return False  # Not all same and not white
    for element in column:
        if element != first_element:
            return False  # Not all the same
    return True  # All the same and not white


def transform(input_grid):
    """
    Transforms the input grid according to the specified rules.
    """
    input_grid = np.array(input_grid)
    rows = input_grid.shape[0]
    output_grid = np.zeros((rows, 3), dtype=int)

    # Iterate through input grid columns
    for j in range(3):
        column = input_grid[:, j]

        # Check if all pixels are the same color and not white
        if check_all_same_and_not_white(column):
            output_grid[:, j] = 3  # Set corresponding output column to green
        else:
            output_grid[:, j] = 0   # set corresponding output column to white

    return output_grid.tolist()