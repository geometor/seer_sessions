```python
"""
Iterate through each row in the input grid. If a row contains any blue (1) pixels, first create a copy of the row, replacing all blue pixels with red (2) pixels, and add this modified row to the output grid. Then, create a new row with the same width as the input, filled initially with white (0) pixels. For each position in this new row, check the corresponding position in the *original* input row. If the original row had a blue (1) pixel at that position, place a red (2) pixel in the new row at that position. Append this conditionally created row to the output grid. If a row does not contains any blue pixels, simply skip it.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a NumPy array with the same data type as the input
    output_grid = []

    # Iterate through each row of the input grid
    for row in input_grid:
        # Check if the row contains any blue pixels
        if 1 in row:
            # Create a new row for the output, replacing 1s with 2s
            new_row = [2 if cell == 1 else cell for cell in row]
            output_grid.append(new_row)

            # Create a row of 0s, with a 2 where 1s were in the input row
            zero_row = [2 if cell == 1 else 0 for cell in row]
            output_grid.append(zero_row)

    return output_grid
```