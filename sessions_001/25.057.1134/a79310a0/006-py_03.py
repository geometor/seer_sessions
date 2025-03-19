"""
1.  **Identify:** Find all 2x2 squares in the input grid. Ignore any squares of color White (0).
2.  **Select:** If a 2x2 square of a non-white color is present, select it. There will be at most one such square in these tasks, any others should be ignored.
3. **Remove**: Change the color of the selected 2x2 square to White (0).
4.  **Create:** Create a 2x2 square of Red (2) pixels.
5.  **Position:** The position of the new Red square is determined by adding one row, element-wise, to the top-left coordinates of the removed square.
6. **Preserve**: Ensure no other changes.
"""

import numpy as np

def find_square(grid, size):
    """Finds the top-left coordinates of a square of given size, ignoring white squares."""
    rows, cols = grid.shape
    for i in range(rows - size + 1):
        for j in range(cols - size + 1):
            if np.all(grid[i:i+size, j:j+size] != 0) and np.all(grid[i:i+size, j:j+size] == grid[i,j]): # added check to ensure all elements of the square are same
                return (i, j)
    return None

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    
    # Define the size of the square to search for
    size = 2
    
    # Find the top-left corner of the non-white square
    square_pos = find_square(input_grid, size)
    
    if square_pos:
        # Calculate new position (move one row down)
        new_row = square_pos[0] + 1
        new_col = square_pos[1]

        # Remove the original square by setting it to white (0)
        output_grid[square_pos[0]:square_pos[0]+size, square_pos[1]:square_pos[1]+size] = 0

        # Check boundaries before creating the red square
        if new_row + size <= output_grid.shape[0]:
            # Create the 2x2 red square at the new position
            output_grid[new_row:new_row+size, new_col:new_col+size] = 2
    
    return output_grid