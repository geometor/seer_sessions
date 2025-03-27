```python
import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by scaling it by a factor of 2 in both height and width.
    Each white (0) pixel in the input grid maps to a 2x2 block of white (0) pixels in the output grid.
    Each gray (5) pixel in the input grid maps to a 2x2 block with the pattern [[1, 2], [2, 1]] (blue, red; red, blue) in the output grid.
    """

    # Convert input_grid to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Get input dimensions
    input_height, input_width = input_np.shape
    
    # Calculate output dimensions
    output_height = input_height * 2
    output_width = input_width * 2
    
    # Initialize the output grid with white (0) pixels
    output_grid = np.zeros((output_height, output_width), dtype=int)
    
    # Iterate through each pixel of the input grid
    for r in range(input_height):
        for c in range(input_width):
            # Get the color of the current input pixel
            pixel_color = input_np[r, c]
            
            # Calculate the top-left coordinates for the corresponding 2x2 block in the output grid
            out_r = r * 2
            out_c = c * 2
            
            # Apply the transformation rules based on the input pixel color
            if pixel_color == 5:  # Gray pixel
                # Fill the 2x2 block with the pattern [[1, 2], [2, 1]]
                output_grid[out_r, out_c] = 1     # blue
                output_grid[out_r, out_c + 1] = 2 # red
                output_grid[out_r + 1, out_c] = 2 # red
                output_grid[out_r + 1, out_c + 1] = 1 # blue
            elif pixel_color == 0: # White pixel
                # The 2x2 block is already filled with white (0) due to initialization
                # Explicitly setting them (optional but clear):
                # output_grid[out_r, out_c] = 0
                # output_grid[out_r, out_c + 1] = 0
                # output_grid[out_r + 1, out_c] = 0
                # output_grid[out_r + 1, out_c + 1] = 0
                pass # No change needed as the grid is initialized with 0
            # Add conditions for other colors if necessary, though not present in examples

    # Return the transformed output grid
    return output_grid.tolist() # Convert back to list of lists if required by the environment

```