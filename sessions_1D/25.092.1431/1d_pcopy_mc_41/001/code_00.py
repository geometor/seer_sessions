import numpy as np

def is_single_dot(grid, row, col):
    """
    Checks if a non-white pixel at (row, col) is a single dot,
    meaning its horizontal neighbors (within bounds) are background (0).
    Assumes grid is 1D or checks only horizontal neighbors.
    """
    height, width = grid.shape
    
    # Check if the pixel itself is non-white
    if grid[row, col] == 0:
        return False

    # Check left neighbor
    left_is_background = (col == 0) or (grid[row, col - 1] == 0)
    
    # Check right neighbor
    right_is_background = (col == width - 1) or (grid[row, col + 1] == 0)

    # It's a single dot if both neighbors are background
    return left_is_background and right_is_background

def transform(input_grid):
    """
    Transforms the input grid according to the following rule:
    1. Initialize the output grid as a copy of the input grid.
    2. Iterate through each pixel in the input grid's row.
    3. If a pixel is non-white (not 0) and is a single dot (i.e., its horizontal 
       neighbors within the grid boundaries are white), then:
       a. Identify the color of the dot.
       b. Identify the column index of the dot.
       c. In the output grid, change the pixel at the column index `c` and its 
          horizontal neighbors (column `c-1` and `c+1`, if within grid bounds) 
          to the color of the original dot.
    4. Leave all other pixels (background white pixels and pixels belonging to 
       existing horizontal lines of length 3) unchanged.
    5. Return the modified output grid.
    """
    # Convert input list of lists to a NumPy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize the output grid as a copy of the input grid
    # Changes will be made to this copy based on analysis of the input
    output_np = np.copy(input_np)
    
    # Get grid dimensions (assuming 1 row based on examples)
    height, width = input_np.shape
    
    # Process the single row (index 0)
    row = 0 
    
    # Iterate through each column of the row
    for col in range(width):
        # Check if the pixel at (row, col) in the *original input grid* is a single dot
        if is_single_dot(input_np, row, col):
            # Get the color of the dot from the input grid
            dot_color = input_np[row, col]
            
            # Apply the transformation to the *output grid*
            # Color the center pixel (where the dot was)
            # Note: output_np[row, col] is already dot_color due to the initial copy,
            # but setting it explicitly can improve clarity.
            output_np[row, col] = dot_color
            
            # Color the left neighbor, if it exists
            if col > 0:
                output_np[row, col - 1] = dot_color
                
            # Color the right neighbor, if it exists
            if col < width - 1:
                output_np[row, col + 1] = dot_color
                
    # Convert the modified NumPy array back to a list of lists
    return output_np.tolist()
