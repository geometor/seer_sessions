import numpy as np

"""
Identify all non-white (non-zero) pixels in the input grid.
Calculate the bounding box that encompasses all these non-white pixels.
Create an output grid by copying the input grid.
Iterate through each cell within the calculated bounding box in the input grid.
If a cell within the bounding box in the input grid is white (0), change the corresponding cell in the output grid to yellow (4).
Leave all original non-white pixels and all pixels outside the bounding box unchanged.
"""

def transform(input_grid):
    """
    Fills the background within the bounding box of all non-background 
    objects with yellow, preserving the original objects.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    
    # Find the coordinates of all non-white pixels
    non_white_coords = np.argwhere(input_grid > 0)

    # If there are no non-white pixels, return the input grid unchanged
    if non_white_coords.size == 0:
        return input_grid.copy()

    # Calculate the bounding box
    min_row = np.min(non_white_coords[:, 0])
    max_row = np.max(non_white_coords[:, 0])
    min_col = np.min(non_white_coords[:, 1])
    max_col = np.max(non_white_coords[:, 1])

    # Initialize the output grid as a copy of the input grid
    output_grid = input_grid.copy()
    
    # Define the fill color
    fill_color = 4 # yellow

    # Iterate through the cells within the bounding box
    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
            # Check if the corresponding cell in the *input* grid is white (0)
            if input_grid[r, c] == 0:
                # If it is white, change the cell in the *output* grid to the fill color
                output_grid[r, c] = fill_color

    return output_grid