```python
import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by creating a larger output grid (double the height and width) 
    composed of four quadrants derived from the input grid:
    - Top-left: Original input grid.
    - Top-right: Horizontally flipped input grid.
    - Bottom-left: Vertically flipped input grid.
    - Bottom-right: Input grid flipped both horizontally and vertically.
    """

    # Convert input list of lists to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)

    # Get the dimensions of the input grid
    input_height, input_width = input_array.shape

    # Calculate the dimensions of the output grid
    output_height = 2 * input_height
    output_width = 2 * input_width

    # Initialize the output grid with zeros (or any default value)
    # Using the same dtype as the input array
    output_grid = np.zeros((output_height, output_width), dtype=input_array.dtype)

    # 1. Top-left quadrant: Copy the original input grid
    output_grid[0:input_height, 0:input_width] = input_array

    # 2. Top-right quadrant: Create horizontally flipped version and copy
    flipped_horizontal = np.fliplr(input_array)
    output_grid[0:input_height, input_width:output_width] = flipped_horizontal

    # 3. Bottom-left quadrant: Create vertically flipped version and copy
    flipped_vertical = np.flipud(input_array)
    output_grid[input_height:output_height, 0:input_width] = flipped_vertical

    # 4. Bottom-right quadrant: Create version flipped both ways and copy
    # Can flip the vertically flipped version horizontally, or vice-versa
    flipped_both = np.fliplr(flipped_vertical) 
    # Alternatively: flipped_both = np.flipud(flipped_horizontal)
    output_grid[input_height:output_height, input_width:output_width] = flipped_both

    # Convert the final numpy array back to a list of lists for the expected output format
    return output_grid.tolist()
```