"""
1.  **Identify Azure Regions:** Locate all contiguous regions of azure (8) pixels in the input grid.
2.  **Enclosure and adjacency Check:** for each azure region, perform step 3.
3.  **Fill with green:** find the bounding box of the azure object. Find all white
    pixels inside this bounding box, if any, that are adjacent to any azure
    pixel of the current region, replace these white pixels with green (3).
    Pixels are adjacent side by side or diagonally.
"""

import numpy as np
from scipy.ndimage import label

def get_objects(grid, color):
    """
    Find contiguous regions of a specific color in the grid.
    """
    binary_grid = (grid == color).astype(int)
    labeled_grid, num_objects = label(binary_grid)
    objects = []
    for i in range(1, num_objects + 1):
        objects.append(np.where(labeled_grid == i))
    return objects
    

def get_bounding_box(region):
    """
    Calculate the bounding box of a region.
    """
    min_row = np.min(region[0])
    max_row = np.max(region[0])
    min_col = np.min(region[1])
    max_col = np.max(region[1])
    return min_row, max_row, min_col, max_col

def is_adjacent(pixel, region):
    """
    Check if a pixel is adjacent to any pixel in a region (8-connectivity).
    """
    rows, cols = region
    for r, c in zip(rows, cols):
        if abs(pixel[0] - r) <= 1 and abs(pixel[1] - c) <= 1:
            return True
    return False

def transform(input_grid):
    # initialize output_grid
    output_grid = input_grid.copy()
    
    # Identify Azure Regions
    azure_regions = get_objects(input_grid, 8)

    # Enclosure and adjacency Check & Fill
    for azure_region in azure_regions:
        min_row, max_row, min_col, max_col = get_bounding_box(azure_region)
        
        # Find white pixels within the bounding box
        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                if input_grid[r, c] == 0:  # white pixel
                    # check if the pixel is also adjacent to any of the
                    # current azure region pixels
                    if is_adjacent((r, c), azure_region):
                         output_grid[r, c] = 3  # green
                        
    return output_grid