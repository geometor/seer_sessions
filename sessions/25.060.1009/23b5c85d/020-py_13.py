"""
1.  Identify the Largest Square: Find the largest square (contiguous block of pixels of the same color) within the input grid. It does *not* have to be a solid square.
2.  Determine Bounding Box: Find the minimum and maximum row and column indices occupied by the pixels of this largest square. This defines the smallest rectangular region containing the entire largest square.
3.  Extract Subgrid: Extract the rectangular subgrid from the *input grid* corresponding to the bounding box. This subgrid includes all pixels (of any color) within the bounding box, not just the pixels of the largest square.
4. Return: return the subgrid
"""

import numpy as np
from scipy.ndimage import measurements

def find_largest_square(grid):
    """
    Finds the largest square (contiguous block of same color) in the grid.
    """
    # Label connected regions of the same color.
    labeled_grid, num_features = measurements.label(grid)
    
    # If there are no features, return None.
    if num_features == 0:
        return None

    # Calculate the size of each labeled region.
    sizes = measurements.sum(grid, labeled_grid, range(num_features + 1))

    # Find the largest region
    largest_region_label = np.argmax(sizes)
    
    if largest_region_label == 0: # background
       return None
        
    largest_region_mask = (labeled_grid == largest_region_label)

    # Get coordinates of the largest region.
    coords = np.argwhere(largest_region_mask)
    
    # Check the shape of this.
    min_row = coords[:, 0].min()
    max_row = coords[:, 0].max()
    min_col = coords[:, 1].min()
    max_col = coords[:, 1].max()
    
    width = max_col - min_col + 1
    height = max_row - min_row + 1

    if width != height:
        return None
    
    return largest_region_mask


def transform(input_grid):
    # Convert input grid to a NumPy array.
    input_array = np.array(input_grid)

    # Find the largest square.
    largest_square_mask = find_largest_square(input_array)

    # If no largest square is found, return an empty grid.
    if largest_square_mask is None:
        return []

    # Find the coordinates of all pixels in the largest square.
    square_coords = np.argwhere(largest_square_mask)


    # Determine Bounding Box: Find the min and max row and column indices.
    min_row = square_coords[:, 0].min()
    max_row = square_coords[:, 0].max()
    min_col = square_coords[:, 1].min()
    max_col = square_coords[:, 1].max()

    # Extract Subgrid: Extract the relevant section from the *input* grid.
    output_grid = input_array[min_row:max_row + 1, min_col:max_col + 1]

    return output_grid.tolist()