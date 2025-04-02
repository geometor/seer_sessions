```python
"""
Processes the input grid row by row. 
For each row:
1. Finds all non-white pixels (color > 0).
2. If a row contains two or more non-white pixels:
   a. Determines their color (assuming a single non-white color per row, uses the color of the first non-white pixel found).
   b. Finds the leftmost (minimum column index) and rightmost (maximum column index) non-white pixel in that row.
   c. Fills the horizontal segment between the leftmost and rightmost pixel (inclusive) with that color in the corresponding row of the output grid. Pixels outside this range retain their original color from the input.
3. If a row contains fewer than two non-white pixels (zero or one), the row is copied directly from the input to the output grid without modification.
The output grid has the same dimensions as the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the fill-horizontal-span transformation to the input grid.

    Args:
        input_grid (list of lists): A 2D list representing the input grid.

    Returns:
        list of lists: A 2D list representing the transformed output grid.
    """
    # Convert input list of lists to a NumPy array for easier processing
    input_array = np.array(input_grid, dtype=int)
    
    # Initialize the output array as a copy of the input. This handles rows
    # with < 2 non-white pixels automatically, as they won't be modified later.
    output_array = np.copy(input_array)
    
    # Get the dimensions of the grid
    height, width = input_array.shape

    # Process each row independently
    for r in range(height):
        # Find the column indices of non-white pixels (color > 0) in the current row
        non_white_cols = np.where(input_array[r, :] > 0)[0]

        # Check if there are at least two non-white pixels in this row
        if len(non_white_cols) >= 2:
            # Get the color to fill with. Assume all non-white pixels in a
            # row needing filling have the same color; take the first one found.
            fill_color = input_array[r, non_white_cols[0]]
            
            # Find the minimum (leftmost) column index among non-white pixels
            min_col = np.min(non_white_cols)
            # Find the maximum (rightmost) column index among non-white pixels
            max_col = np.max(non_white_cols)
            
            # Fill the horizontal span from min_col to max_col (inclusive) 
            # in the corresponding output row with the determined fill_color.
            # Only this segment of the output row is modified.
            output_array[r, min_col:max_col+1] = fill_color
            
        # No explicit 'else' needed: if len(non_white_cols) < 2, the row in 
        # output_array remains as it was initially copied from input_array.

    # Convert the output NumPy array back to a standard Python list of lists
    output_grid = output_array.tolist()
    
    return output_grid
```