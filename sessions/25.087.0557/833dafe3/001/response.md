```python
"""
Construct a larger grid by reflecting the input grid into four quadrants.
The output grid's dimensions are twice the input grid's dimensions (2H x 2W).
The bottom-right quadrant is the original input grid.
The bottom-left quadrant is the input grid reflected horizontally.
The top-right quadrant is the input grid reflected vertically.
The top-left quadrant is the input grid reflected both horizontally and vertically.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by creating a 2x2 arrangement of reflections.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Convert input list of lists to numpy array if it isn't already
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid, dtype=int)

    # Determine the height (H) and width (W) of the input grid.
    H, W = input_grid.shape

    # Create a new output grid with dimensions 2H x 2W, initialized with zeros.
    output_grid = np.zeros((2 * H, 2 * W), dtype=int)

    # Create the reflected versions of the input grid
    original = input_grid
    h_reflected = np.fliplr(original) # Flip left-to-right
    v_reflected = np.flipud(original) # Flip top-to-bottom
    hv_reflected = np.flipud(h_reflected) # Flip both ways (or np.rot90(original, 2))

    # Place the original and reflected grids into the corresponding quadrants
    # Top-left quadrant: reflected horizontally and vertically
    output_grid[0:H, 0:W] = hv_reflected

    # Top-right quadrant: reflected vertically
    output_grid[0:H, W:2*W] = v_reflected

    # Bottom-left quadrant: reflected horizontally
    output_grid[H:2*H, 0:W] = h_reflected

    # Bottom-right quadrant: original input grid
    output_grid[H:2*H, W:2*W] = original

    # Return the completed output grid
    return output_grid

```