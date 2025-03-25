"""
Transforms an input 3x3 grid (containing 0s and 1s) to an output 3x3 grid (containing 0s and 2s)
based on the following rule:
1. Iterate through the rows of the input grid.
2. For each input row:
   - If the row contains one or more 1s, create a new output row of all 2s of length 3.
   - If a row does not contain any 1s, create a new output row of all 0s of length 3.
3. The final output grid maintains a fixed 3x3 shape.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""

    # Initialize an empty list to hold the new rows.
    output_rows = []

    # Iterate through each row of the input grid.
    for row in input_grid:
        # Check if the row contains any 1s.
        if 1 in row:
            # If it does, append a row of all 2s.
            output_rows.append([2, 2, 2])
        else:
            # If it doesn't, append a row of all 0s.
            output_rows.append([0, 0, 0])

    # Convert the list of rows to a NumPy array.
    output_grid = np.array(output_rows)
    return output_grid