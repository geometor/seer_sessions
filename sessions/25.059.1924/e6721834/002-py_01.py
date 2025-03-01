"""
1. **Identify the Background:** Determine the most frequent color in the input grid. This color represents the background.
2. **Remove the Background:** Eliminate all pixels of the background color from the input grid.
3. **Crop/Extract remaining parts:** Isolate remaining parts of the grid that have other colors, removing empty rows and columns.
4. Keep relative position of the foreground objects.
"""

import numpy as np
from collections import Counter

def get_background_color(grid):
    # Flatten the grid and count color occurrences
    color_counts = Counter(grid.flatten())
    # Return the most common color (background)
    return color_counts.most_common(1)[0][0]

def remove_background(grid, background_color):
    # Create a mask where True indicates foreground pixels
    mask = grid != background_color
    return mask

def crop_grid(grid, mask):
    # Find rows and cols that contain True values in mask
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)
    
    # get the min/max row
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]

    # use the mask to crop
    return grid[rmin:rmax+1, cmin:cmax+1]

def transform(input_grid):
    """
    Transforms the input grid by removing the background and cropping to the remaining content.
    """
    # Convert input grid to a NumPy array for easier manipulation
    input_grid = np.array(input_grid)

    # 1. Identify the background color
    background_color = get_background_color(input_grid)

    # 2. Remove the background
    foreground_mask = remove_background(input_grid, background_color)

    # 3. Crop the grid to the foreground
    cropped_grid = crop_grid(input_grid, foreground_mask)
    
    return cropped_grid.tolist()