```python
import numpy as np

def transform(input_grid):
    """
    Upscales the input grid by a factor of 3x3. Each pixel in the 
    input grid maps to a 3x3 block in the output grid. 
    If the input pixel is white (0) or azure (8), the corresponding 
    3x3 output block is filled with white (0). 
    If the input pixel is any other color (not 0 or 8), the corresponding 
    3x3 output block forms a plus sign (+) pattern of that color against 
    a white background.
    """

    # Get input grid dimensions
    input_height, input_width = input_grid.shape

    # Calculate output grid dimensions (3x scaling)
    output_height = input_height * 3
    output_width = input_width * 3

    # Initialize output grid with white (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each pixel in the input grid
    for r in range(input_height):
        for c in range(input_width):
            # Get the color of the input pixel
            color = input_grid[r, c]

            # Calculate the top-left coordinates for the 3x3 block in the output grid
            output_r = r * 3
            output_c = c * 3

            # Check the color and apply the appropriate transformation
            # If the color is white (0) or azure (8), the block remains white (already initialized)
            # If the color is any other color (not 0 or 8), apply the plus sign pattern
            if color != 0 and color != 8:
                # Apply the plus sign pattern to the output grid's 3x3 block
                # Check bounds implicitly handled by numpy indexing but explicit checks are safer
                # if writing pixel by pixel, as done here.
                
                # Center pixel
                if 0 <= output_r + 1 < output_height and 0 <= output_c + 1 < output_width:
                    output_grid[output_r + 1, output_c + 1] = color
                # Top center
                if 0 <= output_r < output_height and 0 <= output_c + 1 < output_width:
                     output_grid[output_r, output_c + 1] = color
                # Bottom center
                if 0 <= output_r + 2 < output_height and 0 <= output_c + 1 < output_width:
                    output_grid[output_r + 2, output_c + 1] = color
                # Middle left
                if 0 <= output_r + 1 < output_height and 0 <= output_c < output_width:
                    output_grid[output_r + 1, output_c] = color
                # Middle right
                if 0 <= output_r + 1 < output_height and 0 <= output_c + 2 < output_width:
                     output_grid[output_r + 1, output_c + 2] = color

    return output_grid
```