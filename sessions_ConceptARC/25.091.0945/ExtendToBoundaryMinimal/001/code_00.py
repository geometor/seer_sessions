import numpy as np

"""
1. Find the location (row R, column C) and color (Value) of the single non-white pixel in the input grid.
2. Create an output grid of the same dimensions as the input, initially filled with the background color (white, 0).
3. Check if the column index C of the non-white pixel is 0.
4. If C is 0, fill the entire row R of the output grid with the color Value.
5. If C is not 0, fill the entire column C of the output grid with the color Value.
6. Return the output grid.
"""

def find_single_non_background_pixel(grid, background_color=0):
    """Finds the row, column, and color of the single non-background pixel."""
    non_background_coords = np.argwhere(grid != background_color)
    if non_background_coords.shape[0] != 1:
        # This handles cases where there might be zero or more than one non-background pixel,
        # although the problem description implies exactly one.
        # Returning None signals an unexpected input state based on the observed pattern.
        return None, None, None 
        
    row, col = non_background_coords[0]
    color = grid[row, col]
    return row, col, color

def transform(input_grid):
    """
    Transforms the input grid by finding the single non-white pixel and extending
    it horizontally if it's in the first column, or vertically otherwise.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    
    # Find the non-white pixel's location and color
    row, col, color = find_single_non_background_pixel(input_array, background_color=0)

    # Handle cases where the non-background pixel wasn't found as expected
    if row is None:
        # Return a copy of the input or an empty grid? 
        # Based on examples, it assumes a valid input, let's return a copy for now.
        # Or perhaps better, return an empty grid of the same size.
        return np.zeros_like(input_array).tolist() 

    # Initialize the output grid with the background color (white, 0)
    output_grid = np.zeros_like(input_array, dtype=int)
    
    # Get grid dimensions
    # height, width = input_array.shape # Not strictly needed for this logic, but good practice

    # Apply the transformation rule
    if col == 0:
        # If the pixel is in the first column (index 0), fill the entire row
        output_grid[row, :] = color
    else:
        # Otherwise, fill the entire column
        output_grid[:, col] = color

    # Convert the numpy array back to a list of lists for the expected output format
    return output_grid.tolist()
