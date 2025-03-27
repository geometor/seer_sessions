```python
import numpy as np

def transform(input_grid):
    """
    Scales the input grid by a factor of 3x3. Each non-white pixel 
    in the input is transformed into a 3x3 plus sign (+) pattern of 
    the same color in the output grid, centered within the 3x3 block 
    corresponding to the input pixel's position. White pixels in the 
    input map to 3x3 blocks of white pixels in the output.
    """

    # Get input grid dimensions
    input_height, input_width = input_grid.shape

    # Calculate output grid dimensions
    output_height = input_height * 3
    output_width = input_width * 3

    # Initialize output grid with white (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each pixel in the input grid
    for r in range(input_height):
        for c in range(input_width):
            # Get the color of the input pixel
            color = input_grid[r, c]

            # If the color is not white (0)
            if color != 0:
                # Calculate the top-left coordinates for the 3x3 block in the output grid
                output_r = r * 3
                output_c = c * 3

                # Apply the plus sign pattern to the output grid
                # Center pixel of the 3x3 block
                output_grid[output_r + 1, output_c + 1] = color
                # Top center
                output_grid[output_r, output_c + 1] = color
                # Bottom center
                output_grid[output_r + 2, output_c + 1] = color
                # Middle left
                output_grid[output_r + 1, output_c] = color
                # Middle right
                output_grid[output_r + 1, output_c + 2] = color

    return output_grid
```