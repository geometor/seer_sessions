"""
The transformation rule is to identify contiguous regions of red (2) pixels and determine if they fully enclose any green (3) pixels. If a green region is completely enclosed by red pixels, and no other colors (besides 2 and 3) are present within the enclosed area, the green pixels are changed to red.
"""

import numpy as np
from scipy.ndimage import label, measurements

def get_contiguous_regions(grid, color):
    """
    Finds contiguous regions of a specific color in the grid.
    Returns a list of coordinates for each region.
    """
    mask = (grid == color)
    labeled_array, num_features = label(mask)
    regions = []
    for i in range(1, num_features + 1):
        region_coords = np.where(labeled_array == i)
        regions.append(list(zip(region_coords[0], region_coords[1])))
    return regions

def is_enclosed(grid, region_coords, enclosing_color):
    """
    Checks if a region is fully enclosed by pixels of the enclosing_color.
    """
    rows, cols = grid.shape
    # Create a set for faster lookup
    region_set = set(tuple(coord) for coord in region_coords)

    # Check if any pixel in the region is on the border
    for r, c in region_set:
        if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
            return False  # Region touches the border, so it's not enclosed

    # Check if all neighbors of the region are either the enclosing color or part of the region itself
    for r, c in region_set:
        neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
        for nr, nc in neighbors:
            if 0 <= nr < rows and 0 <= nc < cols:  # Check bounds
                if (nr, nc) not in region_set and grid[nr, nc] != enclosing_color:
                    return False  # Neighbor is not enclosing color and not part of the region

    return True

def get_bounding_box(region_coords):
    """Calculates min and max row/col"""
    min_row = min(r for r, _ in region_coords)
    max_row = max(r for r, _ in region_coords)
    min_col = min(c for _, c in region_coords)
    max_col = max(c for _, c in region_coords)
    return min_row, max_row, min_col, max_col

def check_region_colors(grid, region_coords, allowed_colors):
    """
    Check if a region contains any colors *not* present in an allow list.
    """
    min_row, max_row, min_col, max_col = get_bounding_box(region_coords)
    for i in range(min_row, max_row + 1):
        for j in range(min_col, max_col + 1):
            if (i,j) in region_coords:
                if grid[i,j] not in allowed_colors:
                    return False # Disqualifying color
    return True # No disqualifying colors

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Identify Red Regions
    red_regions = get_contiguous_regions(output_grid, 2)

    # Check for enclosured and transform
    for red_region in red_regions:
        #find green regions:
        green_regions = get_contiguous_regions(output_grid, 3)
        for green_region in green_regions:
            if is_enclosed(output_grid, green_region, 2) and check_region_colors(output_grid, red_region, [2, 3]):
                #change all green pixels to red if enclosed:
                for r, c in green_region:
                    output_grid[r, c] = 2  # Change to red

    return output_grid