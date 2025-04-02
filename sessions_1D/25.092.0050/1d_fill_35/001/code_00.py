import numpy as np

"""
Transforms a 1D input grid by finding the first and last non-white pixels. 
It then fills the segment between these two pixels (inclusive) in the output grid 
with the color of the first non-white pixel found in the input. Pixels outside 
this segment remain white (0).
"""

def find_first_non_white(row):
    """Finds the index and color of the first non-white pixel in a row."""
    for idx, pixel in enumerate(row):
        if pixel != 0:
            return idx, pixel
    return -1, -1 # Return invalid index and color if none found

def find_last_non_white(row):
    """Finds the index of the last non-white pixel in a row."""
    for idx in range(len(row) - 1, -1, -1):
        if row[idx] != 0:
            return idx
    return -1 # Return invalid index if none found

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): A 2D list representing the input grid. 
                                     Expected to be effectively 1D (1 row).

    Returns:
        list of lists: The transformed output grid.
    """
    # Ensure input is treated as a numpy array for easier handling if needed,
    # but primarily work with the first row as a list.
    input_row = input_grid[0]
    height = len(input_grid) # Should be 1
    width = len(input_row)
    
    # Initialize the output grid with the same dimensions, filled with white (0)
    output_grid = [[0 for _ in range(width)] for _ in range(height)] # Or just [[0] * width] for 1D case

    # Find the index and color of the first non-white pixel
    first_idx, fill_color = find_first_non_white(input_row)

    # If no non-white pixel is found, return the all-white grid
    if first_idx == -1:
        return output_grid

    # Find the index of the last non-white pixel
    last_idx = find_last_non_white(input_row)
    
    # Access the output row (there's only one)
    output_row = output_grid[0]

    # Fill the segment in the output row between the first and last non-white indices
    # with the color of the first non-white pixel.
    for i in range(first_idx, last_idx + 1):
        output_row[i] = fill_color
        
    return output_grid
