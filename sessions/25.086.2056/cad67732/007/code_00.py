# -*- coding: utf-8 -*-
"""
Transforms an input grid by creating an enlarged output grid (2x height, 2x width)
and placing two copies of the input grid into specific quadrants based on the
distribution of non-background pixels in the input. Specifically, it compares
the count of non-background pixels on the main diagonal vs. the anti-diagonal
of the input grid. If the main diagonal count is greater than or equal to the
anti-diagonal count, copies are placed on the main diagonal of the output grid
(top-left and bottom-right). Otherwise, copies are placed on the anti-diagonal
of the output grid (top-right and bottom-left).
"""

import numpy as np

def count_diagonal_pixels(grid):
    """
    Counts non-white (non-zero) pixels on the main and anti-diagonals of a grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: A tuple containing (main_diagonal_count, anti_diagonal_count).
    """
    height, width = grid.shape
    main_diag_count = 0
    anti_diag_count = 0

    # Iterate through rows to check diagonal elements
    for r in range(height):
        # Main diagonal check: element at (r, r)
        # Check bounds: r must be less than width
        if r < width and grid[r, r] != 0:
            main_diag_count += 1

        # Anti-diagonal check: element at (r, width - 1 - r)
        c = width - 1 - r
        # Check bounds: c must be non-negative and less than width
        if 0 <= c < width and grid[r, c] != 0:
            anti_diag_count += 1

    return main_diag_count, anti_diag_count

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # 1. Determine the height (H) and width (W) of the input grid.
    input_height, input_width = input_grid.shape

    # 2. Create a new output grid with dimensions 2*H x 2*W, initializing all cells to white (0).
    output_height = 2 * input_height
    output_width = 2 * input_width
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # 3. & 4. Count non-white pixels on main and anti-diagonals of the input grid.
    main_count, anti_count = count_diagonal_pixels(input_grid)

    # 5. Compare diagonal counts.
    # 6. If main_count >= anti_count: Place copies on the main diagonal (TL, BR)
    if main_count >= anti_count:
        # 6.a. Copy input to top-left quadrant [0:H, 0:W]
        output_grid[0:input_height, 0:input_width] = input_grid
        # 6.b. Copy input to bottom-right quadrant [H:2H, W:2W]
        output_grid[input_height:output_height, input_width:output_width] = input_grid
    # 7. Else (main_count < anti_count): Place copies on the anti-diagonal (TR, BL)
    else:
        # 7.a. Copy input to top-right quadrant [0:H, W:2W]
        output_grid[0:input_height, input_width:output_width] = input_grid
        # 7.b. Copy input to bottom-left quadrant [H:2H, 0:W]
        output_grid[input_height:output_height, 0:input_width] = input_grid

    # 8. Return the completed output grid.
    return output_grid