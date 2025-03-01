"""
Extracts non-yellow pixels from the input grid and arranges them into a smaller output grid, preserving their relative positions.
"""

import numpy as np

def get_non_yellow_pixels(grid):
    """
    Identifies and returns a list of non-yellow pixels with their positions.
    """
    non_yellow_pixels = []
    for row_index, row in enumerate(grid):
        for col_index, pixel in enumerate(row):
            if pixel != 4:
                non_yellow_pixels.append({
                    'color': pixel,
                    'original_row': row_index,
                    'original_col': col_index
                })
    return non_yellow_pixels

def transform(input_grid):
    # Convert input_grid to numpy array
    input_grid = np.array(input_grid)

    # 1. Identify and Extract Target Pixels
    target_pixels = get_non_yellow_pixels(input_grid)

    if not target_pixels:  # Handle cases with no non-yellow pixels
        return [[]]

    # 2. Determine Output Grid Dimensions and relative positions
    
    rows = [pixel['original_row'] for pixel in target_pixels]
    cols = [pixel['original_col'] for pixel in target_pixels]
    
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)

    
    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 1

    # 3. Create Output Grid
    output_grid = np.full((output_height, output_width), 4) #initialise with yellow background

    # 4. Populate Output Grid
    for pixel in target_pixels:
        new_row = pixel['original_row'] - min_row
        new_col = pixel['original_col'] - min_col
        output_grid[new_row, new_col] = pixel['color']

    return output_grid.tolist()