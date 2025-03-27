"""
1.  **Extract Subgrid:** From the input grid, extract a subgrid comprising the first three columns (columns 0, 1, and 2).
2.  **Transform Pixels:** Within this subgrid, replace all orange pixels (value 7) with green pixels (value 3). Set all other pixels within the subgrid to white (value 0).
3.  **Reverse Rows:** Reverse the order of the rows of the transformed subgrid. The result is the output grid.
"""

import numpy as np

def _extract_subgrid(input_grid):
    # Extract the first three columns
    return input_grid[:, :3]

def _transform_pixels(subgrid):
    # Replace 7 with 3, and everything else within the subgrid with 0
    transformed_subgrid = np.where(subgrid == 7, 3, 0)
    return transformed_subgrid

def _reverse_rows(grid):
    # Reverse the order of rows
    return np.flipud(grid)

def transform(input_grid):
    # Extract subgrid (first 3 columns)
    subgrid = _extract_subgrid(input_grid)

    # Transform pixels (7 -> 3, others -> 0 within the subgrid)
    transformed_subgrid = _transform_pixels(subgrid)

    # Reverse the rows of the transformed subgrid
    output_grid = _reverse_rows(transformed_subgrid)

    return output_grid