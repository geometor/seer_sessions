"""
Examine the input grid to determine if any pixel has the color azure (8).
Create the output grid by copying the input grid exactly.
If the color azure (8) was found anywhere in the input grid, modify the output grid by changing all pixels in the topmost row (row 0) to azure (8).
If the color azure (8) was not found anywhere in the input grid, modify the output grid by changing all pixels in the rightmost column to azure (8).
Return the modified output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies a transformation based on the presence of the color azure (8).

    If azure (8) is present in the input grid, the topmost row of the output 
    grid is filled with azure (8). Otherwise, the rightmost column is filled 
    with azure (8). The rest of the grid remains unchanged.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert input grid to a NumPy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input array
    output_array = np.copy(input_array)
    
    # Define the key color (azure)
    key_color = 8
    
    # Get grid dimensions
    height, width = input_array.shape
    
    # Check if the key_color exists anywhere in the input grid
    key_color_present = np.any(input_array == key_color)
    
    # Apply the transformation based on the presence of the key color
    if key_color_present:
        # If key_color (8) is present, fill the topmost row (row 0) with key_color
        output_array[0, :] = key_color
    else:
        # If key_color (8) is not present, fill the rightmost column (last column) with key_color
        output_array[:, width - 1] = key_color
        
    # Convert the NumPy array back to a list of lists for the final output
    output_grid = output_array.tolist()

    return output_grid