```python
"""
Identifies the contiguous red (2) object and the contiguous azure (8) object.
Calculates the horizontal and vertical gaps (number of background pixels) between their bounding boxes.
Determines the axis (horizontal or vertical) with the larger gap. If gaps are equal, chooses the vertical axis.
Translates the red object along the chosen axis towards the azure object.
The translation distance is equal to the calculated gap along that axis, resulting in a 1-pixel gap between the objects along that axis in the output.
The azure object remains stationary.
The output grid contains the translated red object and the original azure object on a white background.
"""

import numpy as np

def get_object_pixels_and_bbox(grid, color):
    """
    Finds all pixels of a given color and calculates their bounding box.

    Args:
        grid (np.array): The input grid.
        color (int): The color value to search for.

    Returns:
        tuple: A tuple containing:
            - list: A list of (row, col) tuples for each pixel of the specified color.
            - tuple: The bounding box (min_row, max_row, min_col, max_col),
                     or None if no pixels of the color are found.
            Returns (None, None) if no pixels are found.
    """
    pixels = np.argwhere(grid == color)
    if pixels.size == 0:
        return None, None
    
    min_row = np.min(pixels[:, 0])
    max_row = np.max(pixels[:, 0])
    min_col = np.min(pixels[:, 1])
    max_col = np.max(pixels[:, 1])
    
    # Convert numpy array rows to tuples for consistency
    pixel_list = [tuple(p) for p in pixels]
    
    return pixel_list, (min_row, max_row, min_col, max_col)

def transform(input_grid):
    """
    Transforms the input grid by moving the red object towards the azure object
    along the axis of greatest separation, leaving a 1-pixel gap.

    Args:
        input_grid (list[list[int]]): The input grid as a list of lists.

    Returns:
        list[list[int]]: The transformed grid.
    """
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape
    
    # --- Find objects and their bounding boxes ---
    red_pixels, red_bbox = get_object_pixels_and_bbox(grid, 2)
    azure_pixels, azure_bbox = get_object_pixels_and_bbox(grid, 8)

    # Handle cases where one or both objects might be missing (though unlikely in valid ARC tasks)
    if not red_pixels or not azure_pixels:
        return input_grid # Return original grid if objects aren't found

    r1_min, r1_max, c1_min, c1_max = red_bbox
    r2_min, r2_max, c2_min, c2_max = azure_bbox

    # --- Calculate horizontal and vertical gaps ---
    h_gap = 0
    if c1_max < c2_min: # Red is strictly left of azure
        h_gap = c2_min - c1_max - 1
    elif c2_max < c1_min: # Red is strictly right of azure
        h_gap = c1_min - c2_max - 1

    v_gap = 0
    if r1_max < r2_min: # Red is strictly above azure
        v_gap = r2_min - r1_max - 1
    elif r2_max < r1_min: # Red is strictly below azure
        v_gap = r1_min - r2_max - 1
        
    # Ensure gaps are non-negative (already handled by max(0, ...) logic implicitly)
    h_gap = max(0, h_gap)
    v_gap = max(0, v_gap)

    # --- Determine translation direction and distance ---
    dx = 0
    dy = 0

    if h_gap > v_gap:
        # Move horizontally
        if c1_max < c2_min: # Red left of azure -> move right
            dx = h_gap
        elif c2_max < c1_min: # Red right of azure -> move left
            dx = -h_gap
    elif v_gap >= h_gap : # v_gap >= h_gap (includes equality preference for vertical)
        # Move vertically
        if r1_max < r2_min: # Red above azure -> move down
            dy = v_gap
        elif r2_max < r1_min: # Red below azure -> move up
            dy = -v_gap
            
    # If both gaps are 0 and objects don't touch/overlap, something is wrong,
    # but current logic handles dx=0, dy=0 correctly (no move).

    # --- Construct the output grid ---
    output_grid = np.zeros_like(grid) # Initialize with background color (white=0)

    # Place the static azure object
    for r, c in azure_pixels:
        # Check bounds just in case, though azure doesn't move
        if 0 <= r < height and 0 <= c < width:
            output_grid[r, c] = 8

    # Place the translated red object
    for r, c in red_pixels:
        new_r, new_c = r + dy, c + dx
        # Check bounds for the new position
        if 0 <= new_r < height and 0 <= new_c < width:
            output_grid[new_r, new_c] = 2
        # else: pixel moves off-grid, ignore it.

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
```