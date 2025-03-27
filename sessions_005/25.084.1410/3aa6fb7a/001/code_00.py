import numpy as np

"""
Iterate through all 2x2 subgrids in the input grid. If a 2x2 subgrid contains 
exactly three azure (8) pixels and one white (0) pixel, change the color of 
that white pixel to blue (1) in the output grid. All other pixels retain 
their original colors.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Convert input_grid to numpy array if it's not already
    input_grid = np.array(input_grid)
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # Get the dimensions of the grid
    height, width = input_grid.shape

    # Iterate through all possible top-left corners (r, c) of 2x2 subgrids
    # The loops stop at height-1 and width-1 to ensure the 2x2 subgrid fits within the grid boundaries
    for r in range(height - 1):
        for c in range(width - 1):
            # Extract the 2x2 subgrid
            subgrid = input_grid[r:r+2, c:c+2]
            
            # Count the number of azure (8) pixels in the subgrid
            azure_count = np.count_nonzero(subgrid == 8)
            # Count the number of white (0) pixels in the subgrid
            white_count = np.count_nonzero(subgrid == 0)
            
            # Check if the condition is met: 3 azure pixels and 1 white pixel
            if azure_count == 3 and white_count == 1:
                # Find the relative coordinates (wr, wc) of the white pixel within the 2x2 subgrid
                white_indices = np.where(subgrid == 0)
                # There should be exactly one white pixel, so take the first (and only) index
                wr, wc = white_indices[0][0], white_indices[1][0] 
                
                # Calculate the absolute coordinates (tr, tc) in the main grid
                tr, tc = r + wr, c + wc
                
                # Change the color of the white pixel to blue (1) in the output grid
                output_grid[tr, tc] = 1
                
    return output_grid.tolist() # Return as list of lists per ARC standard if needed, np array is also fine
