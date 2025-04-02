"""
Identifies pairs of non-white pixels within each row (treating the input as potentially multi-row, although examples are single-row).
For each row, finds all non-white pixels, groups their column indices into consecutive pairs (first with second, third with fourth, etc.).
For each pair of indices (col1, col2), fills the segment in the corresponding output row from col1 to col2 (inclusive) with the non-white color found at col1.
Pixels outside these filled segments remain white (0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by filling segments between pairs of non-white pixels in each row.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid with the same shape as input, filled with white (0)
    output_grid = np.zeros_like(input_grid)
    height, width = input_grid.shape

    # Process each row independently
    for r in range(height):
        # Get the current row
        row = input_grid[r, :]
        
        # Find the column indices of all non-white pixels in this row
        non_white_indices = np.where(row != 0)[0]
        
        # Iterate through the non-white indices, taking them two at a time
        # The step of 2 ensures we process pairs (0, 1), (2, 3), etc.
        # We iterate up to len - 1 to avoid index errors if the count is odd. 
        # The last index will be ignored if the count is odd, matching the pairing logic.
        for i in range(0, len(non_white_indices) - 1, 2):
            # Get the start and end column indices for the current pair
            col1 = non_white_indices[i]
            col2 = non_white_indices[i+1]
            
            # Get the color to fill with (should be the same for both pixels in the pair)
            fill_color = row[col1] 
            
            # Fill the segment in the output grid's corresponding row
            # The slice includes col1 and goes up to col2 (col2 + 1 is exclusive)
            output_grid[r, col1 : col2 + 1] = fill_color

    # Return the modified output grid
    return output_grid