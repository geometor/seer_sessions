import math
import numpy as np

"""
Processes a 5x9 input grid to produce a 5x4 output grid.
The transformation operates independently on each row.
For each row, it considers two subgrids: columns 0-3 (left) and columns 5-8 (right),
ignoring the central separator column (index 4).
It compares elements at the same corresponding column index (0-3) within the left and right subgrids.
If exactly one of the two compared elements is 0, the output element at that index is 2.
Otherwise (if both are 0 or both are non-zero), the output element is 0.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on element comparison between left and right subgrids.

    Args:
        input_grid: A list of lists representing the 5x9 input grid.

    Returns:
        A list of lists representing the 5x4 output grid.
    """
    output_grid = [] # Initialize the final output grid

    # Iterate through each row of the input grid
    for row in input_grid:
        # Extract the left subgrid (columns 0-3)
        left_subgrid = row[0:4]
        # Extract the right subgrid (columns 5-8)
        right_subgrid = row[5:9]

        output_row = [] # Initialize the row for the output grid

        # Iterate through the corresponding elements of the left and right subgrids
        for i in range(4): # Corresponds to indices 0, 1, 2, 3
            left_val = left_subgrid[i]
            right_val = right_subgrid[i]

            # Apply the comparison logic
            # Check if exactly one of the values is 0
            if (left_val == 0 and right_val != 0) or \
               (left_val != 0 and right_val == 0):
                output_row.append(2) # Append 2 if the condition is met
            else:
                output_row.append(0) # Append 0 otherwise

        # Add the completed output row to the final output grid
        output_grid.append(output_row)

    return output_grid
