```python
import numpy as np

"""
Transforms the input grid by processing each row independently.
If a row contains exactly two non-white pixels of the same color,
it fills the horizontal span between and including these two pixels with their color.
Otherwise, the row remains unchanged.
"""

def find_non_white_pixels(row):
    """Finds the indices and colors of non-white pixels in a row."""
    indices = np.where(row != 0)[0]
    colors = row[indices]
    return indices, colors

def transform(input_grid):
    """
    Applies the row-based filling transformation to the input grid.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert input to a numpy array for easier processing and row slicing
    input_np = np.array(input_grid, dtype=int)
    # Create a copy to modify, ensuring unchanged rows are preserved
    output_np = np.copy(input_np)
    # Get the number of rows (height)
    height = input_np.shape[0]

    # Iterate through each row of the grid by index
    for r in range(height):
        # Get the current row from the input
        row = input_np[r, :]
        
        # Find non-white pixels in the current row
        non_white_indices, non_white_colors = find_non_white_pixels(row)

        # Check if the condition is met: exactly two non-white pixels
        if len(non_white_indices) == 2:
            # Get the two colors
            color1 = non_white_colors[0]
            color2 = non_white_colors[1]

            # Check if the colors are the same
            if color1 == color2:
                # The condition is fully met, proceed with filling
                fill_color = color1
                
                # Get the column indices of the two pixels
                col1 = non_white_indices[0]
                col2 = non_white_indices[1]
                
                # Determine the start and end columns for the fill (inclusive)
                col_start = min(col1, col2)
                col_end = max(col1, col2) 

                # Modify the corresponding row in the output numpy array
                # Fill the segment from col_start to col_end (inclusive)
                # Numpy slicing is exclusive at the end, so use col_end + 1
                output_np[r, col_start : col_end + 1] = fill_color
                
        # If the conditions (exactly 2 non-white pixels AND same color) are not met,
        # the corresponding row in output_np remains as the original input row (due to the initial copy).

    # Convert the final numpy array back to a standard list of lists for the return value
    return output_np.tolist()
```