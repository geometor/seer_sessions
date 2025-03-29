```python
import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by creating an output grid double the size and 
    mapping each non-background pixel from the input to a 4x4 block in the output.

    The transformation follows these steps:
    1. Determine the input grid dimensions (H x W).
    2. Create an output grid with dimensions (2*H x 2*W), initialized with the background color (0).
    3. Iterate through each pixel (r, c) of the input grid.
    4. If the input pixel's color (C) is not the background color (0):
       a. Calculate the top-left coordinate (R, C_out) for the output block using the formula: R = 2*r - 2, C_out = 2*c - 2.
       b. Fill the 4x4 area in the output grid starting at (R, C_out) with the color C.
    5. Return the completed output grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    input_height, input_width = input_grid_np.shape

    # Calculate output dimensions: double the input dimensions
    output_height = input_height * 2
    output_width = input_width * 2

    # Initialize output grid with background color (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each cell of the input grid
    for r in range(input_height):
        for c in range(input_width):
            # Get the color of the current input pixel
            pixel_color = input_grid_np[r, c]

            # Check if the pixel is not the background color (0)
            if pixel_color != 0:
                # Calculate the top-left corner for the 4x4 block in the output grid
                # using the derived formula: (2*r - 2, 2*c - 2)
                output_r_start = 2 * r - 2
                output_c_start = 2 * c - 2

                # Calculate the bottom-right corner (exclusive) for the 4x4 block
                output_r_end = output_r_start + 4
                output_c_end = output_c_start + 4

                # Ensure the block stays within the output grid boundaries.
                # Clip indices if necessary, although based on examples, 
                # r and c seem >= 1, making start coordinates >= 0.
                # And the 2x scaling should ensure end coordinates are within bounds.
                # Adding checks for robustness.
                if 0 <= output_r_start < output_height and 0 <= output_c_start < output_width:
                    # Use min to handle potential edge cases if the block partially exceeds bounds
                    r_end_clipped = min(output_r_end, output_height)
                    c_end_clipped = min(output_c_end, output_width)
                    
                    # Fill the calculated 4x4 (or clipped) area in the output grid
                    output_grid[output_r_start:r_end_clipped, output_c_start:c_end_clipped] = pixel_color

    # Convert the final numpy array back to a list of lists for the expected output format
    return output_grid.tolist() 
```