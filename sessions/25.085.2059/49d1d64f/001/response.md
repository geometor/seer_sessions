```python
"""
Transforms an input grid by adding a border around it.
The output grid is two rows taller and two columns wider than the input.
The central part of the output grid is a copy of the input grid.
The new border pixels (excluding corners) are populated by copying the corresponding edge pixels from the input grid.
The four corner pixels of the new border are set to white (0).
"""

import numpy as np

def transform(input_grid):
    """
    Applies a border padding transformation to the input grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Convert input list of lists to numpy array if necessary
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid, dtype=int)

    # 1. Determine the height (H) and width (W) of the input grid.
    H, W = input_grid.shape

    # 2. Create a new output grid with dimensions (H+2) x (W+2), initially filled with white (0).
    output_grid = np.zeros((H + 2, W + 2), dtype=int)

    # 3. Copy the entire input grid into the center of the output grid.
    #    The input grid's top-left (0,0) maps to output grid's (1,1).
    output_grid[1:H+1, 1:W+1] = input_grid

    # 4. Copy the first row of the input grid into the output grid's first row (excluding corners).
    output_grid[0, 1:W+1] = input_grid[0, :]

    # 5. Copy the last row of the input grid into the output grid's last row (excluding corners).
    output_grid[H+1, 1:W+1] = input_grid[H-1, :]

    # 6. Copy the first column of the input grid into the output grid's first column (excluding corners).
    output_grid[1:H+1, 0] = input_grid[:, 0]

    # 7. Copy the last column of the input grid into the output grid's last column (excluding corners).
    output_grid[1:H+1, W+1] = input_grid[:, W-1]

    # 8. The corner cells (0,0), (0, W+1), (H+1, 0), (H+1, W+1) remain 0 as initialized.

    # 9. Return the completed output grid.
    return output_grid.tolist() # Return as list of lists per ARC standard

```