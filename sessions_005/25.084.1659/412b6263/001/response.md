```python
import numpy as np

"""
Transforms the input grid by performing the following steps:
1. Transpose the input grid (swap rows and columns).
2. Flip the transposed grid vertically to create the 'core_grid'.
3. Create an output grid with dimensions calculated based on the core_grid:
   - output_height = 2 * core_grid_height + 3
   - output_width = core_grid_width + 2
4. Construct the output grid:
   - Draw a border frame (1 pixel thick) of blue (1) around the entire output.
   - Draw a horizontal dividing line of blue (1) in the middle.
   - Set the six corner points (outer top-left, top-right, bottom-left, bottom-right, and the ends of the middle dividing line) to orange (7).
   - Place two copies of the core_grid vertically within the frame, separated by the middle dividing line.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list[list[int]]): The input grid.

    Returns:
        list[list[int]]: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)

    # 1. Transpose the input grid
    transposed_grid = np.transpose(input_np)

    # 2. Flip the transposed grid vertically to create the core_grid
    core_grid = np.flipud(transposed_grid)
    core_h, core_w = core_grid.shape

    # 3. Calculate output dimensions
    output_height = 2 * core_h + 3
    output_width = core_w + 2

    # 4. Initialize output grid (fill with a default color, e.g., white (0),
    #    or directly start drawing the border)
    #    Using blue (1) as default simplifies border drawing slightly.
    output_grid = np.full((output_height, output_width), 1, dtype=int) # Default to blue

    # 5. Place the two copies of the core_grid
    # Top copy
    output_grid[1:core_h + 1, 1:core_w + 1] = core_grid
    # Bottom copy
    output_grid[core_h + 2:core_h + 2 + core_h, 1:core_w + 1] = core_grid

    # 6. Set the corner points to orange (7)
    # Outer corners
    output_grid[0, 0] = 7
    output_grid[0, output_width - 1] = 7
    output_grid[output_height - 1, 0] = 7
    output_grid[output_height - 1, output_width - 1] = 7
    # Middle border corners
    output_grid[core_h + 1, 0] = 7
    output_grid[core_h + 1, output_width - 1] = 7

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()

```