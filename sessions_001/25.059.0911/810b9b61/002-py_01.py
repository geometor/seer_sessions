"""
1.  **Identify Blue Regions:** Scan the input grid and identify all connected components (regions) of blue (1) pixels.  A connected component is a group of adjacent blue pixels.
2.  **Measure Region Size:** For each identified blue region, calculate its size (the number of blue pixels it contains).
3.  **Conditional Replacement:** If a blue region is larger than the threshold defined by the size of the original blue element, replace *all* pixels within that region with green (3).
4. **Preserve remaining blue pixels**: Any blue region smaller or equal to the original blue is preserved
5.  **Output:** Create a new grid with the replacements. All other colors and empty spaces remain the same, as do blue elements not meeting the replacement criterion.
"""

import numpy as np
from scipy.ndimage import label

def find_connected_components(grid, color):
    """Finds connected components of a specific color in the grid."""
    colored_grid = (grid == color).astype(int)
    labeled_grid, num_labels = label(colored_grid)
    return labeled_grid, num_labels

def get_component_sizes(labeled_grid, num_labels):
    """Calculates the size of each connected component."""
    sizes = []
    for i in range(1, num_labels + 1):  # Label 0 is background
        sizes.append(np.sum(labeled_grid == i))
    return sizes

def transform(input_grid):
    """Transforms the input grid by replacing large blue regions with green."""
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # Find connected components of blue color (1)
    labeled_grid, num_labels = find_connected_components(input_grid, 1)

    # Get the sizes of all blue components
    component_sizes = get_component_sizes(labeled_grid, num_labels)
      
    # Iterate through each component and replace if it's larger than 1 pixel
    for i in range(1, num_labels + 1):
        if component_sizes[i-1] > 1:
            output_grid[labeled_grid == i] = 3

    return output_grid