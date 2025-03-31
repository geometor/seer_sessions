import numpy as np
from scipy.ndimage import label, find_objects

"""
Transformation Rule:

1. Identify the largest contiguous non-background (white, 0) object in the input grid. Determine its color (`filter_color`) and create a mask (`largest_obj_mask`) indicating its pixels.
2. Identify all pixels in the input grid that are non-background AND are *not* part of the largest object. These are the `key_grid_pixels`.
3. Calculate the minimum bounding box enclosing all `key_grid_pixels`.
4. Extract the subgrid within this bounding box from the original input grid. This is the `key_grid`.
5. Define a set of 'target colors' to be replaced with white (0) based on the `filter_color`:
    - If `filter_color` is blue (1), target colors are {blue (1), red (2), yellow (4), maroon (9)}.
    - If `filter_color` is green (3), target colors are {blue (1), azure (8), maroon (9)}.
    - If `filter_color` is azure (8), target colors are {blue (1), green (3), gray (5), orange (7)}.
    - Otherwise, the target color set is empty.
6. Create an output grid by copying the `key_grid`.
7. Iterate through the output grid. If a cell's color is in the 'target colors' set, change its color to white (0).
8. Return the modified output grid as a list of lists.
"""

def find_largest_non_background_object(grid):
    """
    Finds the color and mask of the largest contiguous non-background object.

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: (object_color, object_mask) or (None, None) if no object found.
               object_color (int): The color of the largest object.
               object_mask (np.array): Boolean mask, True for pixels of the largest object.
    """
    background_color = 0
    non_background_mask = grid != background_color
    
    # Label connected components
    labeled_array, num_features = label(non_background_mask)
    
    if num_features == 0:
        return None, None # No non-background objects found

    # Find the size of each component (excluding background label 0)
    component_sizes = np.bincount(labeled_array.ravel())
    if len(component_sizes) <= 1: # Only background found
         return None, None
         
    # Find the label of the largest component (ignore background at index 0)
    largest_component_label = np.argmax(component_sizes[1:]) + 1
    
    # Get coordinates of the largest object to find its color
    coords = np.argwhere(labeled_array == largest_component_label)
    if coords.size == 0: # Should not happen if component exists
        return None, None
        
    # Get the color from the original grid using the first coordinate
    object_color = grid[coords[0, 0], coords[0, 1]]
    
    # Create the mask for the largest object
    object_mask = labeled_array == largest_component_label
    
    return object_color, object_mask

def find_key_grid(grid, largest_obj_mask):
    """
    Finds the subgrid corresponding to the key grid.
    The key grid is the bounding box of non-background pixels
    that are NOT part of the largest object mask.

    Args:
        grid (np.array): The input grid.
        largest_obj_mask (np.array): Boolean mask for the largest object.

    Returns:
        np.array: The extracted key grid, or None if not found.
    """
    background_color = 0
    
    # Default to an empty mask if none provided (e.g., no largest object found)
    if largest_obj_mask is None:
        largest_obj_mask = np.zeros_like(grid, dtype=bool)

    # Identify potential key pixels: non-background AND not in the largest object
    potential_key_pixels_mask = (grid != background_color) & (~largest_obj_mask)
    
    # Get coordinates of these pixels
    coords = np.argwhere(potential_key_pixels_mask)
    
    if coords.shape[0] == 0:
        return None # No key grid pixels found

    # Find the bounding box (min/max row and column)
    min_row, min_col = coords.min(axis=0)
    max_row, max_col = coords.max(axis=0)
    
    # Extract the subgrid using the bounding box slice
    key_grid_slice = (slice(min_row, max_row + 1), slice(min_col, max_col + 1))
    key_grid = grid[key_grid_slice]
    
    return key_grid

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    grid = np.array(input_grid, dtype=int)
    background_color = 0

    # 1. Find the largest non-background object and its color/mask
    filter_color, largest_obj_mask = find_largest_non_background_object(grid)

    # 2. & 3. & 4. Find the key grid (bounding box of other non-background pixels)
    key_grid = find_key_grid(grid, largest_obj_mask)

    if key_grid is None:
        # Handle case where no key grid is found (e.g., return empty or specific error grid)
        # Based on examples, a key grid should always exist if input is valid.
        # Returning an empty list of lists might be a reasonable default.
        return [[]] 
        
    # 5. Determine the set of target colors based on the filter_color
    target_colors = set()
    if filter_color == 1: # Blue
        target_colors = {1, 2, 4, 9}
    elif filter_color == 3: # Green
        target_colors = {1, 8, 9}
    elif filter_color == 8: # Azure
        target_colors = {1, 3, 5, 7}
    # Note: If filter_color is None (no large object found), target_colors remains empty,
    # so the key_grid would be returned unmodified (if found).

    # 6. Create the output grid (start as a copy of the key grid)
    output_grid = key_grid.copy()

    # 7. Iterate and replace target colors with background color
    rows, cols = output_grid.shape
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] in target_colors:
                output_grid[r, c] = background_color

    # 8. Return the result as a list of lists
    return output_grid.tolist()