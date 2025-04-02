"""
Transforms an input grid by processing each row independently.
For each row in the input grid:
1. Find the column indices of all non-white pixels (value > 0).
2. If there are two or more non-white pixels in the row:
   a. Identify the color of the first non-white pixel found.
   b. Find the column index of the first (leftmost) non-white pixel.
   c. Find the column index of the second non-white pixel from the left.
   d. In the corresponding row of the output grid, draw a horizontal line segment 
      using the identified color, starting from the first non-white pixel's column 
      and ending at the second non-white pixel's column (inclusive). Pixels outside
      this segment remain unchanged from the input.
3. If a row contains fewer than two non-white pixels, the corresponding row in 
   the output grid is identical to the input row.
The output grid has the same dimensions as the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the row-based horizontal line drawing transformation based on the 
    first two non-white pixels.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Initialize the output grid as a copy of the input grid.
    # This handles rows with 0 or 1 non-white pixels correctly, as they
    # remain unchanged. It also preserves pixels outside the drawn segment
    # in rows that are modified.
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Iterate through each row of the input grid
    for r in range(height):
        # Get the current row from the input grid
        row = input_grid[r, :]
        
        # Find the column indices of non-white pixels in the current row
        # np.where returns indices sorted in ascending order automatically
        non_white_indices = np.where(row > 0)[0]

        # Check if there are at least two non-white pixels in this row
        if non_white_indices.size >= 2:
            # Determine the color (use the color of the first non-white pixel)
            color = row[non_white_indices[0]]
            
            # Get the column index of the first non-white pixel (leftmost)
            start_col = non_white_indices[0]
            
            # Get the column index of the second non-white pixel
            end_col = non_white_indices[1]
            
            # Fill the corresponding row segment in the output grid with the color 
            # between start_col and end_col (inclusive).
            # NumPy slicing is exclusive of the end index, so use end_col + 1.
            output_grid[r, start_col : end_col + 1] = color
        # else: 
            # If the row has fewer than 2 non-white pixels, the output_grid row 
            # (copied from input) is already correct. No action needed.

    # Return the modified grid
    return output_grid