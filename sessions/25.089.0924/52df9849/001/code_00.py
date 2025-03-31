import numpy as np
from collections import Counter

"""
Identify the two distinct non-background colors (Color A and Color B) present in the input grid, assuming the background color is orange (7). Calculate the bounding box for all pixels of Color A and the bounding box for all pixels of Color B. Determine the intersection region of these two bounding boxes. Iterate through each pixel within this intersection region. If a pixel in the input grid within this region has Color A, change its color to Color B in the output grid. If it has Color B, change its color to Color A. Pixels outside the intersection region, or background-colored pixels within the intersection, remain unchanged.
"""

def get_pixel_coordinates_by_color(grid):
    """Finds coordinates of all pixels for each color."""
    color_coords = {}
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color not in color_coords:
                color_coords[color] = []
            color_coords[color].append((r, c))
    return color_coords

def get_bounding_box(coords):
    """Calculates the bounding box for a list of coordinates."""
    if not coords:
        return None # Or handle appropriately, maybe return (0,0,0,0) or raise error
    min_r = min(r for r, c in coords)
    max_r = max(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_c = max(c for r, c in coords)
    # Return format: (min_row, max_row, min_col, max_col) inclusive
    return min_r, max_r, min_c, max_c

def transform(input_grid):
    """
    Swaps the colors of the two non-background objects within their bounding box intersection.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    
    # Define background color
    background_color = 7 

    # Find coordinates for each color
    color_coordinates = get_pixel_coordinates_by_color(input_grid)

    # Identify non-background colors
    non_background_colors = [color for color in color_coordinates if color != background_color]

    # Ensure there are exactly two non-background colors
    if len(non_background_colors) != 2:
        # If not exactly two non-background colors, return the original grid unchanged
        # This handles edge cases or grids not matching the pattern
        return output_grid 

    color_a = non_background_colors[0]
    color_b = non_background_colors[1]

    # Get coordinates for each non-background color
    coords_a = color_coordinates[color_a]
    coords_b = color_coordinates[color_b]

    # Calculate bounding boxes
    bbox_a = get_bounding_box(coords_a)
    bbox_b = get_bounding_box(coords_b)
    
    if not bbox_a or not bbox_b:
        # Handle case where one object might be empty if logic allows
        return output_grid

    min_r_a, max_r_a, min_c_a, max_c_a = bbox_a
    min_r_b, max_r_b, min_c_b, max_c_b = bbox_b

    # Calculate the intersection of the bounding boxes
    intersect_min_r = max(min_r_a, min_r_b)
    intersect_max_r = min(max_r_a, max_r_b)
    intersect_min_c = max(min_c_a, min_c_b)
    intersect_max_c = min(max_c_a, max_c_b)

    # Check if there is a valid intersection area
    if intersect_min_r > intersect_max_r or intersect_min_c > intersect_max_c:
        # No overlap in bounding boxes, return original grid
        return output_grid

    # Iterate through the intersection region
    for r in range(intersect_min_r, intersect_max_r + 1):
        for c in range(intersect_min_c, intersect_max_c + 1):
            # Get the color of the pixel from the input grid
            input_color = input_grid[r, c]
            
            # Swap colors if they match one of the non-background colors
            if input_color == color_a:
                output_grid[r, c] = color_b
            elif input_color == color_b:
                output_grid[r, c] = color_a
            # Pixels with background color or other colors remain unchanged (already copied)

    return output_grid