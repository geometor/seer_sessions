import numpy as np
from scipy.ndimage import label, find_objects, maximum_position

"""
Transformation Rule:

1. Identify the largest contiguous non-background (white, 0) object in the input grid. Determine its color (`filter_color`).
2. Identify the small, isolated rectangular patch of cells containing multiple distinct non-background colors (the `key_grid`).
3. Define a set of 'target colors' to be replaced with white (0) based on the `filter_color`:
    - If `filter_color` is blue (1), target colors are {blue (1), red (2), yellow (4), maroon (9)}.
    - If `filter_color` is green (3), target colors are {blue (1), azure (8), maroon (9)}.
    - If `filter_color` is azure (8), target colors are {blue (1), green (3), gray (5), orange (7)}.
    - Otherwise, the target color set is empty.
4. Create an output grid by copying the `key_grid`.
5. Iterate through the output grid. If a cell's color is in the 'target colors' set, change its color to white (0).
6. Return the modified output grid.
"""

def find_largest_non_background_object(grid):
    """Finds the coordinates and color of the largest contiguous non-background object."""
    background_color = 0
    non_background_mask = grid != background_color
    
    # Label connected components
    labeled_array, num_features = label(non_background_mask)
    
    if num_features == 0:
        return None, None # No non-background objects found

    # Find the size of each component
    component_sizes = np.bincount(labeled_array.ravel())
    # component_sizes[0] is the background size, ignore it
    if len(component_sizes) > 1:
         # Find the label of the largest component (excluding background)
        largest_component_label = np.argmax(component_sizes[1:]) + 1
        
        # Get the coordinates and color of the largest object
        coords = np.argwhere(labeled_array == largest_component_label)
        if coords.size > 0:
            # Get the color from the original grid using the first coordinate
            object_color = grid[coords[0, 0], coords[0, 1]]
            # Get the slice (bounding box) of the largest object
            obj_slice = find_objects(labeled_array == largest_component_label)[0]
            return obj_slice, object_color, labeled_array == largest_component_label # Return slice, color, and mask
    
    return None, None, None # Should not happen if num_features > 0 and components exist

def find_key_grid_location(grid, largest_obj_mask):
    """
    Finds the bounding box of the 'key grid'.
    Assumes the key grid is composed of the non-background pixels
    that are NOT part of the largest object.
    """
    background_color = 0
    
    # Create a mask for potential key grid pixels:
    # Must not be background AND must not be part of the largest object
    potential_key_pixels_mask = (grid != background_color) & (~largest_obj_mask)
    
    coords = np.argwhere(potential_key_pixels_mask)
    
    if coords.shape[0] == 0:
        return None # No key grid pixels found

    # Find the bounding box
    min_row, min_col = coords.min(axis=0)
    max_row, max_col = coords.max(axis=0)
    
    # Return the slice representing the bounding box
    return (slice(min_row, max_row + 1), slice(min_col, max_col + 1))

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    grid = np.array(input_grid, dtype=int)
    background_color = 0

    # 1. Find the largest non-background object and its color
    largest_obj_slice, filter_color, largest_obj_mask = find_largest_non_background_object(grid)

    if largest_obj_slice is None or filter_color is None:
        # Handle cases where no large object is found (return empty or original?)
        # Based on examples, this shouldn't happen. If it did, maybe return an empty grid?
        # For now, let's assume valid inputs as per examples.
        # Returning the input might be safer if unsure.
         print("Warning: Could not find a largest non-background object.")
         # Let's try finding *any* potential key grid even without a large object mask
         largest_obj_mask = np.zeros_like(grid, dtype=bool) # Empty mask


    # 2. Find the location (slice) of the key grid
    key_grid_slice = find_key_grid_location(grid, largest_obj_mask)

    if key_grid_slice is None:
         print("Warning: Could not find key grid location.")
         return np.array([[]]) # Return empty grid if no key grid found


    # Extract the key grid
    key_grid = grid[key_grid_slice]
    
    # 3. Determine the set of target colors based on the filter_color
    target_colors = set()
    if filter_color == 1: # Blue
        target_colors = {1, 2, 4, 9}
    elif filter_color == 3: # Green
        target_colors = {1, 8, 9}
    elif filter_color == 8: # Azure
        target_colors = {1, 3, 5, 7}
    # Add more rules here if other filter colors appear in future examples

    # 4. Create the output grid (start as a copy of the key grid)
    output_grid = key_grid.copy()

    # 5. & 6. Iterate and replace target colors with background color
    rows, cols = output_grid.shape
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] in target_colors:
                output_grid[r, c] = background_color

    return output_grid.tolist() # Return as list of lists as per ARC standard