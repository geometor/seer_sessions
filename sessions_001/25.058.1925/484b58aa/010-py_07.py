"""
Identifies and removes large contiguous regions of white (color 0) pixels from the input grid.
"""

import numpy as np
from scipy.ndimage import label

def get_contiguous_regions(grid):
    """
    Finds contiguous regions (blobs) of the same color in a grid.

    Args:
        grid: A 2D numpy array representing the grid.

    Returns:
        A list of tuples, where each tuple contains:
        - A boolean mask representing the region.
        - The color of the region.
    """
    labeled_grid, num_labels = label(grid)
    regions = []
    for i in range(1, num_labels + 1):  # Label 0 is background
        mask = labeled_grid == i
        color = grid[mask][0]  # Get the color of the region
        regions.append((mask, color))
    return regions

def transform(input_grid):
    """
    Transforms the input grid by removing contiguous white regions.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the output grid.
    """
    # Initialize the output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Get all contiguous regions
    regions = get_contiguous_regions(input_grid)
    
    # Iterate through the regions and remove white regions
    for mask, color in regions:
        if color == 0:  # Check if the region is white
              output_grid[mask] = 0

    return output_grid