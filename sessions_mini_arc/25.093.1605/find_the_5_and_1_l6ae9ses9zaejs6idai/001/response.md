```python
import numpy as np

"""
Transforms a 5x5 grid based on the following rule:
1. Find a column where all cells have the value 5.
2. If such a column exists:
   a. Change all cells in that column to 1.
   b. Change the cell in the last row of that column to 2.
3. Keep all other cells the same as the input.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): A 5x5 grid of integers.

    Returns:
        list of lists: The transformed 5x5 grid.
    """
    # Convert input grid to a NumPy array for easier column operations
    grid = np.array(input_grid)
    # Initialize output_grid as a copy of the input grid
    output_grid = grid.copy()
    
    # Get the dimensions of the grid
    rows, cols = grid.shape

    # Iterate through each column index
    for j in range(cols):
        # Extract the current column
        column = grid[:, j]
        
        # Check if all elements in the column are 5
        if np.all(column == 5):
            # If the condition is met, transform this column in the output grid
            # Change all cells in this column to 1
            output_grid[:, j] = 1
            # Change the cell in the last row of this column to 2
            output_grid[rows - 1, j] = 2
            # Assuming only one such column exists per input, stop searching
            break 
            
    # Convert the NumPy array back to a list of lists before returning
    return output_grid.tolist()

```