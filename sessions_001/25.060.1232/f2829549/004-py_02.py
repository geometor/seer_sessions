"""
1.  **Locate:** Find the column in the input grid that contains all 1s (blue).
2.  **Extract:** Extract this column, along with the two columns immediately to its right.
3. **Replace:** In the extracted sub-grid, replace all non-zero values with the number 3 (green). All zero cells remain as zero.
4.  **Output:** The resulting sub-grid is the output.
"""

import numpy as np

def find_column_of_ones(grid):
    # Iterate through columns to find the one with all 1s
    for j in range(grid.shape[1]):
        if np.all(grid[:, j] == 1):
            return j
    return -1  # Return -1 if no such column is found

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find the column with all 1s
    ones_column_index = find_column_of_ones(input_grid)

    # Extract the relevant columns
    if ones_column_index != -1 and ones_column_index + 2 < input_grid.shape[1]:
        extracted_grid = input_grid[:, ones_column_index:ones_column_index + 3]
    else:
      return None

    # Create a copy to modify for output
    output_grid = extracted_grid.copy()
    
    # replace non zero cells with 3
    output_grid[output_grid != 0] = 3
    

    return output_grid.tolist()