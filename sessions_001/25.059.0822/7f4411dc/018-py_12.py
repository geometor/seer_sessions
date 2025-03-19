"""
1. Identify Connected Gray Regions: Find all connected regions (objects) of gray (5) pixels in the input grid.  A connected region is a group of gray pixels where each pixel is adjacent (horizontally or vertically, not diagonally) to at least one other pixel in the group.
2. Determine Object to consolidate: In all cases there is one largest mass of grey. The bounding box should be created to fully enclose this region.
3. Create rectangle: Create a solid grey rectangle based on the bounding box of the main gray object.
4. Clear Other Pixels: Set all pixels outside the consolidated gray rectangle to white (0).
"""

import numpy as np
from scipy.ndimage import label

def get_largest_connected_component(grid, color):
    """
    Finds the largest connected component of a given color.
    """
    labeled_grid, num_labels = label(grid == color)
    if num_labels == 0:
        return None  # No components of the specified color

    # Count the size of each component
    component_sizes = np.bincount(labeled_grid.ravel())

    # Remove the background (label 0)
    component_sizes = component_sizes[1:]
    
    # Find the label of the largest component
    largest_component_label = np.argmax(component_sizes) + 1 # +1 because we removed 0

    return labeled_grid == largest_component_label

def get_bounding_box(mask):
    """
    Calculates the bounding box of a boolean mask.
    """
    rows, cols = np.where(mask)
    if len(rows) == 0:
        return None  # No True values in the mask
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, min_col), (max_row, max_col)


def transform(input_grid):
    """
    Transforms the input grid by consolidating the largest gray object into a rectangle.
    """
    # Create a copy to modify
    output_grid = np.copy(input_grid)

    # Find the largest connected gray region
    largest_gray_region = get_largest_connected_component(input_grid, 5)

    if largest_gray_region is not None:
        # Get the bounding box of the largest gray region
        bounding_box = get_bounding_box(largest_gray_region)

        if bounding_box:
            (min_row, min_col), (max_row, max_col) = bounding_box

            # Create the solid gray rectangle
            for i in range(min_row, max_row + 1):
                for j in range(min_col, max_col + 1):
                    output_grid[i, j] = 5

            # Clear other pixels outside the bounding box.
            for i in range(output_grid.shape[0]):
                for j in range(output_grid.shape[1]):
                    if not (min_row <= i <= max_row and min_col <= j <= max_col):
                        output_grid[i,j] = 0

    else:
        # if no grey, set everything to 0
        output_grid[:] = 0


    return output_grid