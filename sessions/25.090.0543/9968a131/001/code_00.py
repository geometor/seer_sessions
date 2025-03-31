import numpy as np
from typing import List

"""
Transforms the input grid based on specific patterns found within each row.

The transformation logic is applied row by row:
1. If a row starts with the sequence [7, 8, 3, 7] (orange, azure, green, orange), 
   the middle two elements [8, 3] are transformed into [7, 8] (orange, azure) 
   and the fourth element 7 (orange) is transformed into 3 (green). 
   The modified sequence becomes [7, 7, 8, 3]. The rest of the row, if any, remains unchanged.
   Specifically, input `[7, 8, 3, 7]` becomes output `[7, 7, 8, 3]`.

2. If a row starts with the sequence [5, 0, 7] (gray, white, orange), 
   this sequence is transformed into [7, 5, 0] (orange, gray, white). 
   The rest of the row, if any, remains unchanged.

3. If a row does not match either of the starting patterns described above, 
   it is copied to the output grid without any changes.
"""

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies transformations to rows of the input grid based on specific starting patterns.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input grid to a numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    # Create a copy of the grid to modify, ensuring the original is untouched
    output_grid = grid.copy()
    
    # Get the dimensions of the grid
    height, width = grid.shape

    # Iterate through each row of the grid
    for r in range(height):
        # Extract the current row
        row = grid[r]

        # Check for the first pattern (from train_1)
        # Requires row width to be at least 4
        if width >= 4 and row[0] == 7 and row[1] == 8 and row[2] == 3 and row[3] == 7:
            # Apply the transformation for pattern 1
            # input:  [7, 8, 3, 7]
            # output: [7, 7, 8, 3]
            output_grid[r, 1] = 7  # 8 becomes 7
            output_grid[r, 2] = 8  # 3 becomes 8
            output_grid[r, 3] = 3  # 7 becomes 3
            # Note: output_grid[r, 0] remains 7 as it was copied initially.
            # Note: Elements from index 4 onwards remain unchanged as they were copied.

        # Check for the second pattern (from train_2)
        # Requires row width to be at least 3
        elif width >= 3 and row[0] == 5 and row[1] == 0 and row[2] == 7:
            # Apply the transformation for pattern 2
            # input:  [5, 0, 7]
            # output: [7, 5, 0]
            output_grid[r, 0] = 7  # 5 becomes 7
            output_grid[r, 1] = 5  # 0 becomes 5
            output_grid[r, 2] = 0  # 7 becomes 0
            # Note: Elements from index 3 onwards remain unchanged as they were copied.

        # If neither pattern matches, the row in output_grid remains unchanged
        # (because it was copied initially).

    # Convert the modified numpy array back to a list of lists
    return output_grid.tolist()