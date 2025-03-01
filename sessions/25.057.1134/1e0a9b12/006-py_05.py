"""
1. Identify: Find all non-zero elements within the input grid.
2. Extract: Extract these non-zero elements, preserving their original values and their order of appearance (reading left-to-right and top-to-bottom).
3. Determine Output Dimensions: Determine the shape defined by the non-zero elements in the input.
4. Reconstruct: Create an output grid. Copy the non-zero elements to the output grid, maintaining their relative positions as if a bounding box around those elements was translated directly from input to output. Empty cells in the output grid will be set to zero.
"""

import numpy as np

def get_bounding_box(grid):
    # Get the coordinates of non-zero elements
    coords = np.argwhere(grid != 0)
    if len(coords) == 0:
        return None  # Handle the case of no non-zero elements

    # Get min and max row/col indices
    min_row, min_col = coords.min(axis=0)
    max_row, max_col = coords.max(axis=0)
    return (min_row, min_col, max_row, max_col)

def transform(input_grid):
    # Find bounding box of non-zero elements
    bounding_box = get_bounding_box(input_grid)

    if bounding_box is None:
        return np.zeros_like(input_grid)

    min_row, min_col, max_row, max_col = bounding_box

    # Determine the output grid dimensions based on the bounding box size
    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 1

    # initialize the correctly sized output grid
    output_grid = np.zeros((input_grid.shape[0], input_grid.shape[1]), dtype=int)


    # Extract non-zero elements and their positions relative to the bounding box
    non_zero_elements = []
    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
            if input_grid[r, c] != 0:
                non_zero_elements.append(((r, c), input_grid[r, c]))

    # Place the non-zero elements into the output grid,
    # maintaining relative position
    for (row, col), value in non_zero_elements:
        output_grid[row,col] = value # place in original position


    return output_grid