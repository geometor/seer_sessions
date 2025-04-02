```python
import numpy as np

def transform(input_grid):
    """
    Processes a 2D grid row by row.
    For each row containing non-white pixels:
    1. Identify the color (C) and the leftmost (min_col) and rightmost (max_col)
       indices of these non-white pixels.
    2. Determine the end column (end_col) for filling:
        - If C is green (3), end_col is the last column index of the grid.
        - Otherwise, end_col is max_col.
    3. In the output grid's corresponding row, fill the pixels from min_col to
       end_col (inclusive) with color C.
    Rows containing only white pixels remain unchanged.
    """

    # Convert input list of lists to a NumPy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    # Initialize the output grid as a copy of the input
    output_array = np.copy(input_array)
    height, width = input_array.shape

    # Iterate through each row of the grid
    for r in range(height):
        # Get the current row
        row = input_array[r, :]
        
        # Find the column indices of non-white (non-zero) pixels
        non_white_cols = np.where(row != 0)[0]

        # If there are no non-white pixels in this row, continue to the next row
        if len(non_white_cols) == 0:
            continue

        # Identify the color (assuming all non-white pixels in a row are the same color)
        # Get the color from the first non-white pixel found
        pixel_color = row[non_white_cols[0]]
        
        # Find the minimum (leftmost) column index
        min_col = np.min(non_white_cols)
        # Find the maximum (rightmost) column index
        max_col = np.max(non_white_cols)

        # Determine the end column for filling based on the color
        if pixel_color == 3:  # Green
            end_col = width - 1
        else: # Other colors (Red, Blue in examples)
            end_col = max_col

        # Fill the segment in the output grid's corresponding row
        output_array[r, min_col:end_col + 1] = pixel_color

    # Convert the output NumPy array back to a list of lists
    output_grid = output_array.tolist()
    return output_grid

```