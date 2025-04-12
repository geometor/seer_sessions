"""
1. Create a copy of the input grid.
2. Find the coordinates (row, column) of all pixels with the color red (2).
3. If no red pixels are found, return the unmodified copy.
4. If red pixels are found, check their alignment:
   a. If all red pixels share the same row index, modify the copy by setting all pixels in the first row (row 0) to red (2).
   b. If all red pixels share the same column index, modify the copy by setting all pixels in the first column (column 0) to red (2).
5. Return the modified grid.
"""

import numpy as np

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the alignment of red (2) pixels.
    If all red pixels are in the same row, the first row becomes red.
    If all red pixels are in the same column, the first column becomes red.
    Otherwise, the grid remains unchanged.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Create a copy to modify and return
    output_np = np.copy(input_np)
    
    # Find the coordinates of all red pixels (value 2)
    red_pixels_coords = np.argwhere(input_np == 2)

    # Check if any red pixels were found
    if red_pixels_coords.size == 0:
        # No red pixels, return the unmodified copy
        return output_np.tolist()

    # Extract row and column indices
    rows = red_pixels_coords[:, 0]
    cols = red_pixels_coords[:, 1]

    # Check if all red pixels share the same row index
    # Use set to find unique row indices. If the set has only one element, all rows are the same.
    if len(set(rows)) == 1:
        # All red pixels are in the same row, set the first row (row 0) to red (2)
        output_np[0, :] = 2
    # Check if all red pixels share the same column index
    elif len(set(cols)) == 1:
        # All red pixels are in the same column, set the first column (column 0) to red (2)
        output_np[:, 0] = 2
        
    # If neither condition is met (red pixels are not aligned horizontally or vertically),
    # the output_np remains the initial copy of input_np.

    # Convert the result back to a list of lists before returning
    return output_np.tolist()