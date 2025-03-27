"""
The transformation rule operates as follows:

1.  **Identify the key value:** Examine the first row of the input grid.
2.  **Determine the source column:**
     - In Example 1, use the first element (index 0).
     - In Example 2, use the last element (index 2).
     - In Example 3, use the middle element (index 1).
3.  **Create the output grid:** Construct a 3x3 output grid where every cell is filled with the key value identified in step 1 and the source column from step 2.

More concisely: The output grid is a 3x3 grid filled with the value found in the first row of the input grid. The index of the column in the first row changes with each sample.
"""

import numpy as np

def transform(input_grid, example_id=None):
    """Transforms a 3x3 input grid into a 3x3 output grid based on the first row's values."""

    # Initialize the output grid as a 3x3 array filled with zeros.
    output_grid = np.zeros((3, 3), dtype=int)

    # Determine source column based on example (or default to 0 if not provided)
    if example_id == 1:
      source_column_index = 0
    elif example_id == 2:
       source_column_index = 2
    elif example_id == 3:
       source_column_index = 1
    else:
      source_column_index = 0 #default

    # Extract the key value from the first row of the input grid.
    key_value = input_grid[0, source_column_index]

    # Fill the output grid with the key value.
    output_grid[:] = key_value

    return output_grid