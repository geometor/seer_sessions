"""
The output grid consists of the largest connected component of azure (8) and blue (1) pixels,
where "connected" means horizontally or vertically adjacent, but not diagonally. The relative
positions and shapes of these pixels within the component are preserved.
"""

import numpy as np
from scipy.ndimage import label

def find_largest_connected_component(grid):
    """
    Finds the largest connected component of azure (8) and blue (1) pixels in the grid.
    Returns a mask where the largest component is True and everything else is False.
    """
    # Create a mask for azure and blue pixels.
    mask = (grid == 1) | (grid == 8)
    
    # Label connected components.  Use a 4-connected structure (no diagonals).
    labeled_array, num_features = label(mask, structure=[[0,1,0],[1,1,1],[0,1,0]])

    if num_features == 0:
        return np.zeros_like(grid, dtype=bool)

    # Find the size of each component.
    component_sizes = np.bincount(labeled_array.ravel())

    # Remove the background size (first element).
    component_sizes = component_sizes[1:]

    # Find the label of the largest component.
    largest_component_label = np.argmax(component_sizes) + 1

    # Create a mask for the largest component.
    largest_component_mask = (labeled_array == largest_component_label)

    return largest_component_mask

def extract_subgrid_from_mask(grid, mask):
    """
    Extracts the subgrid corresponding to the True values in the mask.
    """
    # Find the bounding box of the mask.
    rows, cols = np.where(mask)
    
    if rows.size > 0 :
        min_row, max_row = np.min(rows), np.max(rows)
        min_col, max_col = np.min(cols), np.max(cols)

        # Extract the subgrid.
        return grid[min_row:max_row+1, min_col:max_col+1]
    
    return np.array([])

def transform(input_grid):
    """
    Extracts the largest connected component of azure (8) and blue (1) pixels.
    """
    # Convert the input grid to a NumPy array.
    input_np = np.array(input_grid)

    # Find the largest connected component of azure and blue pixels.
    largest_component_mask = find_largest_connected_component(input_np)

    # Extract the subgrid corresponding to the largest component.
    output_np = extract_subgrid_from_mask(input_np, largest_component_mask)
    if output_np.size == 0:
        return []
    return output_np.tolist()