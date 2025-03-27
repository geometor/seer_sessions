import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by scaling it by a factor of 2 and modifying
    the resulting 2x2 blocks based on the original pixel color.
    
    1. Double the dimensions of the input grid for the output grid.
    2. Initialize the output grid with white (0) pixels.
    3. For each non-white (non-zero) pixel in the input grid at (r, c) with color C,
       fill the corresponding 2x2 block in the output grid starting at (2*r, 2*c)
       with color C.
    4. For each white (zero) pixel in the input grid at (r, c), set the top-left
       (2*r, 2*c) and bottom-right (2*r + 1, 2*c + 1) corners of the
       corresponding 2x2 block in the output grid to blue (1). The other two
       pixels in the block remain white (0).
    """
    # Convert input grid (list of lists) to a numpy array for efficient operations
    input_grid_np = np.array(input_grid, dtype=int)
    
    # Get the dimensions of the input grid
    input_height, input_width = input_grid_np.shape

    # Calculate the dimensions of the output grid (double the input dimensions)
    output_height = input_height * 2
    output_width = input_width * 2

    # Initialize the output grid with zeros (representing white color)
    output_grid_np = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each pixel of the input grid
    for r in range(input_height):
        for c in range(input_width):
            # Get the color of the current input pixel
            input_color = input_grid_np[r, c]
            
            # Calculate the top-left coordinates of the 2x2 block in the output grid
            output_r_start = r * 2
            output_c_start = c * 2
            
            # Apply transformation based on the input pixel color
            if input_color != 0:
                # If the input color is not white, fill the 2x2 block with that color
                output_grid_np[output_r_start : output_r_start + 2, output_c_start : output_c_start + 2] = input_color
            else:
                # If the input color is white (0), set the top-left and bottom-right
                # corners of the 2x2 block to blue (1).
                # The output grid is already initialized to 0 (white), so we only need to set the blue pixels.
                output_grid_np[output_r_start, output_c_start] = 1  # Top-left corner
                output_grid_np[output_r_start + 1, output_c_start + 1] = 1  # Bottom-right corner

    # Convert the final numpy array back to a list of lists format before returning
    output_grid = output_grid_np.tolist()

    return output_grid