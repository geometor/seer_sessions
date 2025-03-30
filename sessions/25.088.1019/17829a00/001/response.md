```python
import numpy as np

"""
Simulates gravity acting on specific pixels within a grid, constrained by top and bottom boundary rows.

1.  Copies the input grid to create the output grid.
2.  Identifies the background color (assumed to be 7 based on examples).
3.  Identifies the top (row 0) and bottom (last row) boundary rows, which remain unchanged.
4.  For each column independently:
    a.  Extracts all pixels between the top and bottom boundary rows.
    b.  Filters out the background-colored pixels, keeping only the 'falling' pixels in their original relative vertical order.
    c.  Clears the corresponding column section (between boundaries) in the output grid by filling it with the background color.
    d.  Places the extracted 'falling' pixels back into the cleared column section of the output grid, stacked towards the bottom (just above the bottom boundary row).
"""

def transform(input_grid):
    """
    Applies gravity to non-background pixels within each column, bounded by fixed top/bottom rows.

    Args:
        input_grid (list[list[int]]): The input grid.

    Returns:
        list[list[int]]: The transformed grid with pixels settled downwards.
    """
    # Convert input to numpy array for efficient slicing and manipulation
    input_arr = np.array(input_grid, dtype=int)
    output_arr = np.copy(input_arr)
    height, width = input_arr.shape

    # Define the background color (assumed to be 7 based on examples)
    background_color = 7

    # Define the rows involved in the gravity simulation (excluding top and bottom boundary rows)
    start_row_idx = 1
    end_row_idx = height - 1  # Index of the row *before* the bottom boundary

    # Process each column independently
    for c in range(width):
        # Extract the vertical slice of the column where gravity applies from the input
        column_slice = input_arr[start_row_idx:end_row_idx, c]

        # Identify the pixels that will 'fall' (non-background)
        falling_pixels = column_slice[column_slice != background_color]
        num_falling = len(falling_pixels)

        # Clear the corresponding column section in the output grid with the background color
        output_arr[start_row_idx:end_row_idx, c] = background_color

        # If there are any falling pixels in this column
        if num_falling > 0:
            # Calculate the starting row index to place the fallen pixels in the output
            # They stack from the bottom up, so the topmost fallen pixel goes here:
            placement_start_row = end_row_idx - num_falling 
            
            # Place the falling pixels into the calculated position in the output grid
            output_arr[placement_start_row:end_row_idx, c] = falling_pixels

    # Convert the result back to a list of lists
    return output_arr.tolist()
```