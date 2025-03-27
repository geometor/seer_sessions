"""
Identify all distinct objects formed by contiguous gray (5) pixels in the input grid, using 8-way adjacency (including diagonals). Count the total number of these objects (N). Create an output grid as a single column (width 1) with a height equal to N + 1. Fill all pixels in the output grid with the white (0) color.
"""

import numpy as np
from scipy.ndimage import label

def count_gray_objects(grid):
    """
    Counts the number of distinct objects made of gray (5) pixels using 8-way connectivity.

    Args:
        grid (np.array): The input grid.

    Returns:
        int: The number of distinct gray objects.
    """
    # Create a boolean mask for gray pixels (value 5)
    gray_mask = (grid == 5)
    
    # Define the connectivity structure (8-way)
    # [[1,1,1],
    #  [1,1,1],
    #  [1,1,1]] means check all 8 neighbours plus the center
    structure = np.ones((3, 3), dtype=int) 
    
    # Label connected components (objects) in the gray mask
    labeled_array, num_labels = label(gray_mask, structure=structure)
    
    # num_labels is the count of distinct objects
    return num_labels

def transform(input_grid):
    """
    Transforms the input grid based on the count of gray objects.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the output grid (single white column).
    """
    # Count the distinct gray objects in the input grid
    num_objects = count_gray_objects(input_grid)
    
    # Calculate the height of the output grid
    output_height = num_objects + 1
    
    # Create the output grid: width 1, height calculated above, filled with white (0)
    output_grid = np.zeros((output_height, 1), dtype=int)
    
    return output_grid
