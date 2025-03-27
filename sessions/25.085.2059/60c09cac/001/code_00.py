import numpy as np

def transform(input_grid):
    """
    Transforms an input grid by scaling it up by a factor of 2 in both height and width.
    Each pixel in the input grid is expanded into a 2x2 block of the same color 
    in the output grid.

    Args:
        input_grid (list of lists or numpy array): The input grid representing colors.

    Returns:
        numpy array: The transformed output grid, scaled 2x.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Get input dimensions
    input_height, input_width = input_np.shape
    
    # Calculate output dimensions
    output_height = input_height * 2
    output_width = input_width * 2
    
    # Initialize the output grid with zeros (white)
    output_grid = np.zeros((output_height, output_width), dtype=int)
    
    # Iterate through each pixel of the input grid
    for r in range(input_height):
        for c in range(input_width):
            # Get the color of the current input pixel
            color = input_np[r, c]
            
            # Determine the top-left coordinates of the 2x2 block in the output grid
            output_r_start = r * 2
            output_c_start = c * 2
            
            # Fill the corresponding 2x2 block in the output grid with the input pixel's color
            output_grid[output_r_start,     output_c_start]     = color  # Top-left
            output_grid[output_r_start + 1, output_c_start]     = color  # Bottom-left
            output_grid[output_r_start,     output_c_start + 1] = color  # Top-right
            output_grid[output_r_start + 1, output_c_start + 1] = color  # Bottom-right
            
    return output_grid
