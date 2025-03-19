"""
1.  **Azure Replication:** The first four columns of the output grid are always azure (8), regardless of the input. This fills the entire height of the output.

2.  **Input Echo (First Row):** Copy the last two pixels of the input row to the first row of the last two columns of the output grid.

3.  **Conditional Modification (Second Row):**
    *   The fifth column's cell is set to azure (8).
    *   The sixth column cell will match the value of the last element of the input.

4. **Azure Fill (Third Row):**
  - The 5th column will be azure.
  - the 6th column will be azure.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_grid = np.zeros((3, input_width), dtype=int)

    # Azure Replication (first four columns)
    for i in range(3):
        for j in range(min(4, input_width)):  # Ensure we don't go out of bounds
            output_grid[i, j] = 8

    # Input Echo (First Row)
    if input_width >= 2:  # Ensure input has at least two elements
       output_grid[0, -2] = input_grid[0, -2]
       output_grid[0, -1] = input_grid[0, -1]


    # Conditional Modification (Second Row)
    if input_width >= 2:
      output_grid[1, -2] = 8  # Fifth column to azure
      output_grid[1, -1] = input_grid[0,-1]  # sixth matches input

    # Azure Fill (Third Row)
    if input_width >=2:
        output_grid[2, -2] = 8
        output_grid[2, -1] = 8

    return output_grid