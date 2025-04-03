import copy

def transform(input_grid):
    """
    Transforms the input grid (a single row) by finding a single, isolated non-white pixel 
    (a non-zero value surrounded by zeros) and expanding it into a block of three identical 
    pixels, overwriting the original pixel and its immediate left and right neighbors. 
    All other pixels remain unchanged unless overwritten by this expansion.
    """
    
    # Ensure input is a list (single row expected)
    if not isinstance(input_grid, list):
        # Assuming ARC grids might be passed as numpy arrays or lists of lists
        if hasattr(input_grid, 'tolist'):
            # Handle numpy array case
            grid_list = input_grid.tolist()
            if len(grid_list) == 1: # Check if it's a single row nested in a list
                input_grid = grid_list[0]
            else: # Or just a 1D array
                 input_grid = grid_list
        else:
            # Handle list of lists case (take the first row)
            input_grid = input_grid[0]

    # Initialize output_grid as a copy of the input_grid
    output_grid = list(input_grid) # Use list() to ensure it's a mutable copy
    grid_width = len(output_grid)

    # Iterate through the grid to find the isolated pixel
    # Start from index 1 and end at index width-2 to safely check neighbors
    for i in range(1, grid_width - 1):
        # Check if the current pixel is non-white (not 0)
        if output_grid[i] != 0:
            # Check if the neighbors (left and right) are white (0)
            if output_grid[i-1] == 0 and output_grid[i+1] == 0:
                # Found the isolated pixel
                isolated_color = output_grid[i]
                
                # Expand the isolated pixel into a block of three
                # Overwrite the left neighbor, the pixel itself, and the right neighbor
                output_grid[i-1] = isolated_color
                output_grid[i] = isolated_color
                output_grid[i+1] = isolated_color
                
                # Assumption: There is only one such isolated pixel per grid.
                # Stop searching once the transformation is done.
                break 

    # Return the modified grid
    return output_grid
