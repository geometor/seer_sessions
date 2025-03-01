# cf98881b • 010 • refine_coder

---
```python
"""
The transformation extracts subgrids from the input grid. These subgrids are defined as columns starting with colors 4 (yellow), 0 (white), 1 (blue), or 9 (maroon) and extending down to the height of the output grid for that example.  The extracted subgrids are then combined to form the output grid.
"""

import numpy as np

def get_subgrids_starting_with_colors(grid, colors, output_height):
    """
    Identifies and returns subgrids (columns) that start with specified colors,
    with a height equal to output_height.
    """
    selected_subgrids = []
    for j in range(grid.shape[1]):
        if grid[0, j] in colors:
            subgrid = grid[:output_height, j]
            selected_subgrids.append(subgrid)
    return selected_subgrids

def transform(input_grid, output_grid): # Include output_grid in the signature
    """
    Transforms the input grid by selecting subgrids starting with specified colors
    and arranging them into a new output grid.  The height of the subgrids
    is determined by the height of the corresponding output_grid.
    """
    # Define the target colors
    target_colors = [4, 0, 1, 9]

    # Get the height of the output grid
    output_height = output_grid.shape[0]

    # Get subgrids starting with the target colors and the specified height
    selected_subgrids = get_subgrids_starting_with_colors(input_grid, target_colors, output_height)

    # Initialize the output grid
    output_grid_computed = np.zeros((output_height, len(selected_subgrids)), dtype=int)

    # Fill in output
    for i, subgrid in enumerate(selected_subgrids):
        output_grid_computed[:, i] = subgrid

    return output_grid_computed
```
