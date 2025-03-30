```python
"""
Fill specific columns with red (2), preserving gray (5) pixels.

1. Initialize the output grid as a copy of the input grid.
2. Identify the column indices where the pixel value in the last row of the input grid is red (2).
3. For each identified column index:
    a. Iterate through each row index from the top (row 0) to the bottom (last row).
    b. For the cell at the current (row, column):
        i. Check the value of the corresponding cell (row, column) in the *input* grid.
        ii. If the input cell value is *not* gray (5), change the value of the cell (row, column) in the *output* grid to red (2).
        iii. If the input cell value *is* gray (5), the value of the cell (row, column) in the *output* grid remains unchanged (it's already a copy).
4. Return the modified output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Fills columns marked by a red pixel (2) in the last row with red,
    unless the original pixel in that column was gray (5).

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert input list of lists to a numpy array for efficient operations
    input_array = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input_grid
    output_array = np.copy(input_array)
    
    # Get the dimensions of the grid
    height, width = input_array.shape
    
    # Define the colors we are working with
    marker_color = 2  # red
    blocker_color = 5 # gray
    fill_color = 2    # red

    # Identify the columns that have the marker_color in the last row
    # The last row index is height - 1
    marker_columns = np.where(input_array[height - 1, :] == marker_color)[0]

    # Iterate through each column identified by the marker color
    for col_idx in marker_columns:
        # Iterate through each row in that column
        for row_idx in range(height):
            # Check the value of the cell in the original input grid
            original_pixel_value = input_array[row_idx, col_idx]
            
            # If the original pixel is NOT the blocker color, fill it with the fill color
            if original_pixel_value != blocker_color:
                output_array[row_idx, col_idx] = fill_color
                
    # Convert the output numpy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
```