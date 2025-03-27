```python
"""
Expands the input grid by adding a border of width 1. The border cells, excluding the corners, are filled by copying the corresponding edge pixels from the input grid outwards. The four corner cells of the output grid are set to white (0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by adding a border copied from the edges,
    with white corners.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # 1. Determine the height (H) and width (W) of the input grid.
    H, W = input_grid.shape

    # 2. Create a new output grid with height H+2 and width W+2.
    # Initialize with a placeholder value like -1, or directly with 0 (white)
    # since corners will be white anyway. Let's use 0.
    output_grid = np.zeros((H + 2, W + 2), dtype=input_grid.dtype)

    # 3. Copy the input grid into the center of the output grid.
    output_grid[1:H+1, 1:W+1] = input_grid

    # 4. Fill the border of the output grid:
    # a. Copy the first row of the input grid to the top border (excluding corners).
    if H > 0: # Check if input grid is not empty
        output_grid[0, 1:W+1] = input_grid[0, :]
    # b. Copy the last row of the input grid to the bottom border (excluding corners).
    if H > 0:
        output_grid[H+1, 1:W+1] = input_grid[H-1, :]
    # c. Copy the first column of the input grid to the left border (excluding corners).
    if W > 0: # Check if input grid is not empty
        output_grid[1:H+1, 0] = input_grid[:, 0]
    # d. Copy the last column of the input grid to the right border (excluding corners).
    if W > 0:
        output_grid[1:H+1, W+1] = input_grid[:, W-1]

    # 5. Set the four corner cells of the output grid to white (0).
    # Note: Since we initialized with zeros, this step is technically redundant
    # if the placeholder was 0. However, explicitly setting them makes the logic clearer.
    output_grid[0, 0] = 0      # Top-left
    output_grid[0, W+1] = 0    # Top-right
    output_grid[H+1, 0] = 0    # Bottom-left
    output_grid[H+1, W+1] = 0  # Bottom-right

    # 6. Return the completed output grid.
    return output_grid
```