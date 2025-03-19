"""
Identify the largest contiguous object in the input, create an output grid of the same dimensions, and reproduce the object within it.
"""

import numpy as np
from skimage.measure import label, regionprops

def get_largest_object(grid):
    """
    Finds the largest connected component (excluding white) and its metrics.
    """
    grid_np = np.array(grid)
    labeled_grid = label(grid_np != 0, connectivity=1)  # Consider only non-white pixels, 4-connectivity
    regions = regionprops(labeled_grid)

    if not regions:  # handle empty case (all white)
        return {
            'area': 0,
            'bbox': (0, 0, 0, 0),
            'coords': [],
            'label': 0,
        }
    
    largest_region = max(regions, key=lambda region: region.area)
    
    return {
            'area': largest_region.area,
            'bbox': largest_region.bbox, # (min_row, min_col, max_row, max_col)
            'coords': largest_region.coords,
            'label' : largest_region.label
            }

def transform(input_grid):
    # 1. Identify the Largest Object
    largest_object_metrics = get_largest_object(input_grid)
    
    # 2. Determine Output Dimensions
    min_row, min_col, max_row, max_col = largest_object_metrics['bbox']
    height = max_row - min_row
    width = max_col - min_col

    # Handle the case where the input is all white (no largest object)
    if largest_object_metrics['area'] == 0:
        return [[0]]

    # 3. Create and Fill Output Grid
    output_grid = [[0] * width for _ in range(height)] # initialize to white
    for coord in largest_object_metrics['coords']:
      r, c = coord
      output_grid[r - min_row][c - min_col] = input_grid[r][c]

    return output_grid