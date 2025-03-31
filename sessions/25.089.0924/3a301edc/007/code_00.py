import numpy as np

"""
Transforms the input grid based on the following rules:

1.  Identify all non-white (non-zero) pixels in the input grid.
2.  Determine the minimal bounding box that encloses all these non-white pixels.
3.  Identify the distinct non-white colors present within this bounding box: an 'outer' color and an 'inner' color. There should be either one or two such colors.
4.  Determine the 'inner' color (which will be used as the fill_color):
    a. If only one non-white color exists within the bounding box, it is the inner color.
    b. If two non-white colors exist, the inner color is the one whose pixels do *not* touch the absolute edge of the bounding box.
    c. If both colors have pixels touching the bounding box edge (e.g., if the outer frame is only 1 pixel thick), the color with the *fewer* total pixels within the bounding box is considered the 'inner' color.
    d. If ambiguity remains (e.g., >2 colors, neither touches edge, both touch edge with equal counts), the transformation cannot proceed reliably.
5.  Create a copy of the input grid.
6.  Iterate through each pixel location (row, column) *within* the calculated bounding box.
7.  If a pixel at a location within the bounding box has the background color (white, 0) in the *original input grid*, change its color in the *copied output grid* to the determined 'inner' (fill) color.
8.  Pixels outside the bounding box and pixels that were originally non-white remain unchanged in the output grid.
9. Return the modified output grid.
"""


def find_bounding_box(grid):
    """
    Finds the minimum bounding box (min_row, min_col, max_row, max_col) 
    containing all non-zero pixels in the grid.
    Returns None if the grid contains only zeros.
    """
    # Find coordinates (row, col) of all non-zero pixels
    non_zero_coords = np.argwhere(grid != 0)
    # If no non-zero pixels exist, return None
    if non_zero_coords.size == 0:
        return None
    # Determine the minimum and maximum row and column indices
    min_r, min_c = non_zero_coords.min(axis=0)
    max_r, max_c = non_zero_coords.max(axis=0)
    # Return the bounding box coordinates as a tuple
    return (min_r, min_c, max_r, max_c)

def get_inner_color(grid, bbox):
    """
    Determines the 'inner' color within the bounding box based on edge contact
    and pixel count as tie-breaker.
    Returns the integer color value or None if indeterminate.
    """
    min_r, min_c, max_r, max_c = bbox
    
    # Extract the subgrid defined by the bounding box
    subgrid = grid[min_r : max_r + 1, min_c : max_c + 1]
    # Find unique non-zero colors within this subgrid
    unique_colors = np.unique(subgrid[subgrid != 0])

    # Handle cases based on the number of unique non-zero colors found
    if len(unique_colors) == 0:
         # Should not happen if bbox is valid
         return None
    if len(unique_colors) == 1:
         # Rule 4a: Only one non-white color present; it acts as the fill color
         return unique_colors[0]
    if len(unique_colors) != 2:
        # Rule 4d: The pattern observed relies on exactly one or two non-white colors
        return None

    # Rule 4b/4c: We have exactly two colors
    color1, color2 = unique_colors

    # Check which color touches the boundary of the *bounding box*
    color1_touches_boundary = False
    color2_touches_boundary = False

    # Check vertical edges (left: min_c, right: max_c) for rows min_r to max_r
    for r in range(min_r, max_r + 1):
        if grid[r, min_c] == color1 or grid[r, max_c] == color1:
            color1_touches_boundary = True
        if grid[r, min_c] == color2 or grid[r, max_c] == color2:
            color2_touches_boundary = True
        # Optimization: if both found touching, no need to check further rows for vertical edges
        if color1_touches_boundary and color2_touches_boundary:
            break

    # Check horizontal edges (top: min_r, bottom: max_r) for columns min_c to max_c
    # Only check if needed (i.e., if distinction not yet made)
    if not (color1_touches_boundary and color2_touches_boundary):
         for c in range(min_c, max_c + 1): # Check all columns including edges
            if grid[min_r, c] == color1 or grid[max_r, c] == color1:
                color1_touches_boundary = True
            if grid[min_r, c] == color2 or grid[max_r, c] == color2:
                color2_touches_boundary = True
            # Optimization: if both found touching, no need to check further columns
            if color1_touches_boundary and color2_touches_boundary:
                break

    # Determine the inner color based on edge contact
    if color1_touches_boundary and not color2_touches_boundary:
        # Rule 4b: Only color1 touches the edge, so color2 must be inner
        return color2
    elif not color1_touches_boundary and color2_touches_boundary:
        # Rule 4b: Only color2 touches the edge, so color1 must be inner
        return color1
    elif color1_touches_boundary and color2_touches_boundary:
        # Rule 4c: Both colors touch the edge. Use pixel count within the bbox subgrid as a tie-breaker.
        count1 = np.sum(subgrid == color1)
        count2 = np.sum(subgrid == color2)
        if count1 < count2:
            return color1 # Color with fewer pixels is inner
        elif count2 < count1:
            return color2 # Color with fewer pixels is inner
        else:
            # Rule 4d: Counts are equal, and both touch edge - ambiguous
            return None # Indicate failure to determine inner color
    else:
        # Rule 4d: Neither color touches the edge. Unexpected scenario.
        return None # Indicate failure


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    
    # Step 5: Initialize the output grid as a copy of the input grid
    output_grid = np.copy(input_np)
    
    # Step 1 & 2: Find the bounding box containing all non-zero pixels
    bbox = find_bounding_box(input_np)
    
    # If no non-zero pixels (and thus no bbox), return the grid unchanged
    if bbox is None:
        return output_grid.tolist()
        
    # Unpack bounding box coordinates
    min_r, min_c, max_r, max_c = bbox
    
    # Step 3 & 4: Determine the color to use for filling (the 'inner' color)
    fill_color = get_inner_color(input_np, bbox)

    # Step 4d: If a valid fill color could not be determined, return the grid unchanged
    if fill_color is None:
        return output_grid.tolist() # Return the unmodified copy

    # Step 6 & 7: Iterate through each pixel *within* the bounding box
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            # Check if the pixel in the *original* input grid at this location was white (0)
            if input_np[r, c] == 0:
                # If it was white, change its color in the *output* grid to the determined fill_color
                output_grid[r, c] = fill_color
                
    # Step 9: Convert the final NumPy array back to a list of lists format
    return output_grid.tolist()
