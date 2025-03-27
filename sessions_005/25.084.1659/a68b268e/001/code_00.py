"""
The transformation identifies four 4x4 quadrants in the 9x9 input grid, separated by a central row (index 4) and a central column (index 4). It then creates a 4x4 output grid by combining the colors from the corresponding cells of the four quadrants based on a priority order.

1.  Identify the four 4x4 quadrants:
    *   Quadrant 1 (Q1): Top-Left (rows 0-3, columns 0-3).
    *   Quadrant 2 (Q2): Top-Right (rows 0-3, columns 5-8).
    *   Quadrant 3 (Q3): Bottom-Left (rows 5-8, columns 0-3).
    *   Quadrant 4 (Q4): Bottom-Right (rows 5-8, columns 5-8).
2.  Create a new 4x4 output grid.
3.  For each position (r, c) in the 4x4 output grid:
    *   If Q1[r, c] is not white (0), use the color from Q1[r, c].
    *   Else if Q2[r, c] is not white (0), use the color from Q2[r, c].
    *   Else if Q3[r, c] is not white (0), use the color from Q3[r, c].
    *   Else, use the color from Q4[r, c].
"""

import numpy as np

def transform(input_grid):
    """
    Combines four quadrants of a 9x9 input grid into a 4x4 output grid based on color priority.

    Args:
        input_grid (list of lists or numpy array): The 9x9 input grid.

    Returns:
        numpy array: The 4x4 transformed output grid.
    """
    # Convert input to numpy array for easier slicing
    input_array = np.array(input_grid, dtype=int)

    # Define the dimensions
    output_rows, output_cols = 4, 4
    input_rows, input_cols = input_array.shape

    # Ensure input is 9x9 as expected
    if input_rows != 9 or input_cols != 9:
        # Handle potential errors or unexpected input sizes if needed
        # For now, assume input is always 9x9 based on examples
        pass 

    # Extract the four quadrants
    q1 = input_array[0:output_rows, 0:output_cols]            # Top-Left
    q2 = input_array[0:output_rows, output_cols + 1:input_cols] # Top-Right
    q3 = input_array[output_rows + 1:input_rows, 0:output_cols] # Bottom-Left
    q4 = input_array[output_rows + 1:input_rows, output_cols + 1:input_cols] # Bottom-Right

    # Initialize the output grid (4x4) with zeros (white)
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Iterate through each cell of the output grid
    for r in range(output_rows):
        for c in range(output_cols):
            # Apply the priority logic
            if q1[r, c] != 0:
                output_grid[r, c] = q1[r, c]
            elif q2[r, c] != 0:
                output_grid[r, c] = q2[r, c]
            elif q3[r, c] != 0:
                output_grid[r, c] = q3[r, c]
            else:
                output_grid[r, c] = q4[r, c]

    return output_grid.tolist() # Return as list of lists if required by ARC format