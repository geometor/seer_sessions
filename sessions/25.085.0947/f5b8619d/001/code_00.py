import numpy as np

def solve(input_grid):
    """
    Transforms the input grid based on the following rules:
    1. Identify all non-white (non-zero) pixels in the input grid.
    2. Create a 'base grid' initially identical to the input grid.
    3. For each non-white pixel found at location (r_orig, c_orig) in the input:
       - Iterate through all rows `r_new` from 0 to H-1 (where H is the grid height).
       - If `r_new` is different from `r_orig`:
         - Check the pixel at (r_new, c_orig) in the *original* input grid.
         - If the pixel at (r_new, c_orig) in the original input grid is white (0),
           then set the pixel at (r_new, c_orig) in the *base grid* to azure (8).
    4. Create an output grid with dimensions twice the height and twice the width
       of the input grid.
    5. Tile the generated 'base grid' 2x2 onto the output grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Create a copy of the input grid. This copy will be modified to form the 'base grid'.
    base_grid = np.copy(input_np)
    
    # Define the color to use for projected pixels
    azure_color = 8
    white_color = 0
    
    # Find the locations (row, column) of all non-white pixels in the original input grid.
    non_white_locations = []
    for r in range(height):
        for c in range(width):
            if input_np[r, c] != white_color:
                non_white_locations.append((r, c))
                
    # Apply the vertical projection rule to modify the base_grid.
    # For each non-white pixel in the input...
    for r_orig, c_orig in non_white_locations:
        # ...iterate through all rows in the grid.
        for r_new in range(height):
            # We are projecting vertically within the same column (c_orig).
            # The projection only affects rows *other* than the original non-white pixel's row.
            if r_new != r_orig:
                # Check if the cell we are projecting onto was originally white in the input grid.
                if input_np[r_new, c_orig] == white_color:
                    # If it was white, change the corresponding cell in the base_grid to azure.
                    base_grid[r_new, c_orig] = azure_color
                    
    # Create the final output grid, which is twice the height and twice the width of the input grid.
    output_height = 2 * height
    output_width = 2 * width
    # Initialize the output grid with zeros (white). Note: numpy default is float, so specify dtype.
    output_grid = np.zeros((output_height, output_width), dtype=int) 
    
    # Tile the modified base_grid 2x2 onto the output grid.
    # Top-left quadrant
    output_grid[0:height, 0:width] = base_grid
    # Top-right quadrant
    output_grid[0:height, width:output_width] = base_grid
    # Bottom-left quadrant
    output_grid[height:output_height, 0:width] = base_grid
    # Bottom-right quadrant
    output_grid[height:output_height, width:output_width] = base_grid
            
    # Convert the final numpy array back to a list of lists as required.
    return output_grid.tolist()
