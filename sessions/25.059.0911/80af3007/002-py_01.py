"""
Extracts gray (5) pixels from the input grid, and creates a new grid where
the extracted pixels are placed in an alternating pattern with background
(0) pixels, effectively downsampling and creating a striped representation.
"""

import numpy as np

def get_bounding_box(grid):
    """Find the bounding box of all gray pixels."""
    gray_pixels = np.argwhere(grid == 5)
    if gray_pixels.size == 0:
        return (0, 0, 0, 0)
    min_row = np.min(gray_pixels[:, 0])
    max_row = np.max(gray_pixels[:, 0])
    min_col = np.min(gray_pixels[:, 1])
    max_col = np.max(gray_pixels[:, 1])
    return (min_row, max_row, min_col, max_col)

def transform(input_grid):
    """Transforms the input grid by extracting gray pixels and arranging them
    in an alternating pattern with background pixels."""
    input_grid = np.array(input_grid)
    min_row, max_row, min_col, max_col = get_bounding_box(input_grid)

    # Extract the bounding box
    extracted_grid = input_grid[min_row:max_row+1, min_col:max_col+1]
    
    rows, cols = extracted_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # Alternate placement in new output
    output_row, output_col = 0, 0
    for r in range(rows):
       for c in range(cols):
          if (extracted_grid[r,c] == 5):
             output_grid[r,c]=5

    output_rows, output_cols = output_grid.shape
    final_output = np.zeros((2*output_rows-1 if output_rows> 1 else output_rows, 2*output_cols -1 if output_cols > 1 else output_cols), dtype=int)
    for r in range(output_rows):
       for c in range(output_cols):
            if output_grid[r,c] == 5:
                final_output[r*2 if output_rows > 1 else r, c * 2 if output_cols > 1 else c] = 5
    return final_output.tolist()