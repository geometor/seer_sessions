import numpy as np

"""
Transforms the input grid based on pixel color and grid dimensions.
The transformation rule depends on whether the grid is "small" (both height and width < 14) or "large" (height >= 14 or width >= 14).

Rule Breakdown:
1.  Determine grid dimensions (Height H, Width W).
2.  Check if the grid is small: `is_small = (H < 14 and W < 14)`
3.  Iterate through each pixel:
    - If the pixel is White (0): Always change it to Blue (1), regardless of grid size.
    - If the grid is small (`is_small` is True):
        - If the pixel is Red (2): Change it to White (0).
        - Other colors remain unchanged.
    - If the grid is large (`is_small` is False):
        - If the pixel is Blue (1): Change it to White (0).
        - Other colors (including Red (2)) remain unchanged.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid based on its size.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    # 1. Determine grid dimensions (Height H, Width W).
    H, W = input_grid.shape

    # 2. Check if the grid is small.
    is_small_grid = H < 14 and W < 14

    # Initialize output_grid as a copy of the input grid.
    # This handles cases where pixels remain unchanged.
    output_grid = np.copy(input_grid)

    # 3. Iterate through each pixel.
    for r in range(H):
        for c in range(W):
            pixel_color = input_grid[r, c]

            # Rule: White (0) always becomes Blue (1).
            if pixel_color == 0:
                output_grid[r, c] = 1
            # Rules specific to small grids.
            elif is_small_grid:
                # Rule: Red (2) becomes White (0) in small grids.
                if pixel_color == 2:
                    output_grid[r, c] = 0
                # Other colors (1, 3-9) remain unchanged (handled by copy).
            # Rules specific to large grids.
            else: # not is_small_grid (i.e., large grid)
                # Rule: Blue (1) becomes White (0) in large grids.
                if pixel_color == 1:
                    output_grid[r, c] = 0
                # Other colors (2-9, excluding 0 which was handled above) remain unchanged (handled by copy).

    return output_grid