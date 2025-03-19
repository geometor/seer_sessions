"""
The program takes all the largest connected area of color white(0) inside a frame of colors red(2) and azure(8), and changes their color into green(3). Everything else remains unchanged.
"""

import numpy as np
from scipy.ndimage import label

def find_contiguous_region(grid, color):
    # Create a boolean mask for the specified color
    mask = (grid == color)
    # Label connected regions
    labeled_mask, num_labels = label(mask)
    return labeled_mask, num_labels

def get_largest_region(labeled_mask, num_labels):
     # Find the size of each region
    region_sizes = np.bincount(labeled_mask.ravel())
     # Exclude the background (region 0) when finding the largest region
    largest_region_label = np.argmax(region_sizes[1:]) + 1
    return largest_region_label
    

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # Find the contiguous regions of white (0)
    labeled_mask, num_labels = find_contiguous_region(input_grid, 0)

    # Get largest region of white(0)
    largest_region_label = get_largest_region(labeled_mask, num_labels)

    # Change color of the largest region to green
    output_grid[labeled_mask == largest_region_label] = 3
    
    return output_grid