import numpy as np

"""
Transforms the input grid based on the following rules:

1.  Identify all non-white (non-zero) pixels in the input grid.
2.  Determine the minimal bounding box that encloses all these non-white pixels.
3.  Identify the two distinct non-white colors present within this bounding box: an 'outer' color and an 'inner' color.
4.  Determine the 'inner' color. This is the non-white color within the bounding box whose pixels do *not* touch the absolute edge of the bounding box.
5.  If both colors have pixels touching the bounding box edge (e.g., if the outer frame is only 1 pixel thick), the color with the *fewer* pixels within the bounding box is considered the 'inner' color.
6.  If only one non-white color exists, it is used as the 'inner' color.
7.  Iterate through each pixel location (row, column) *within* the calculated bounding box.
8.  If a pixel at a location within the bounding box has the background color (white, 0) in the *original input grid*, change its color in the *output grid* to the determined 'inner' color.
9.  Pixels outside the bounding box and pixels that were originally non-white remain unchanged.
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
    Determines the 'inner' color within the bounding box.
    It prioritizes the color not touching the bbox edge. If ambiguous,
    it uses pixel count within the bbox as a tie-breaker.
    Returns the integer color value or None if indeterminate.
    """
    min_r, min_c, max_r, max_c = bbox
    
    # Extract the subgrid defined by the bounding box
    subgrid = grid[min_r : max_r + 1, min_c : max_c + 1]
    # Find unique non-zero colors within this subgrid
    unique_colors = np.unique(subgrid[subgrid != 0])

    # Handle cases based on the number of unique non-zero colors found
    if len(unique_colors) == 0:
         # Should not happen if bbox is valid, but handle defensively
         # print("Warning: No non-zero colors found within the bounding box.") # Optional logging
         return None
    if len(unique_colors) == 1:
         # Only one non-white color present; it acts as the fill color
         return unique_colors[0]
    if len(unique_colors) != 2:
        # The pattern observed relies on exactly two non-white colors (inner/outer)
        # print(f"Warning: Expected 1 or 2 non-zero colors in bbox, found {len(unique_colors)}: {unique_colors}. Cannot determine inner color.") # Optional logging
        return None

    # We have exactly two colors
    color1, color2 = unique_colors

    # Check which color touches the boundary of the *bounding box*
    color1_touches_boundary = False
    color2_touches_boundary = False

    # Check vertical edges (min_c, max_c) for rows min_r to max_r
    for r in range(min_r, max_r + 1):
        if grid[r, min_c] == color1 or grid[r, max_c] == color1:
            color1_touches_boundary = True
        if grid[r, min_c] == color2 or grid[r, max_c] == color2:
            color2_touches_boundary = True
        # Optimization: if both found touching, no need to check further rows for vertical edges
        if color1_touches_boundary and color2_touches_boundary:
            break

    # Only check horizontal edges if needed (i.e., if distinction not yet made)
    # and avoid double-checking corners already covered by the row checks
    if not (color1_touches_boundary and color2_touches_boundary):
         for c in range(min_c + 1, max_c): # Check columns between the edges
            if grid[min_r, c] == color1 or grid[max_r, c] == color1:
                color1_touches_boundary = True
            if grid[min_r, c] == color2 or grid[max_r, c] == color2:
                color2_touches_boundary = True
            # Optimization: if both found touching, no need to check further columns
            if color1_touches_boundary and color2_touches_boundary:
                break

    # Determine the inner color based on edge contact
    if color1_touches_boundary and not color2_touches_boundary:
        # Only color1 touches the edge, so color2 must be inner
        return color2
    elif not color1_touches_boundary and color2_touches_boundary:
        # Only color2 touches the edge, so color1 must be inner
        return color1
    elif color1_touches_boundary and color2_touches_boundary:
        # Both colors touch the edge. Use pixel count within the bbox as a tie-breaker.
        # The 'inner' object typically has fewer pixels than the 'outer' frame.
        # print(f"Info: Both colors ({color1}, {color2}) touch the bbox edge. Using pixel count within bbox as tie-breaker.") # Optional logging
        count1 = np.sum(subgrid == color1)
        count2 = np.sum(subgrid == color2)
        if count1 < count2:
            return color1
        elif count2 < count1:
            return color2
        else:
            # Counts are equal, and both touch edge - truly ambiguous based on derived rules.
            # print(f"Error: Ambiguous inner color. Both colors touch edge and have equal pixel count ({count1}) within bbox.") # Optional logging
            return None # Indicate failure to determine inner color
    else:
        # Neither color touches the edge. This scenario is unexpected given the problem structure.
        # print(f"Error: Neither color ({color1}, {color2}) touches the bbox edge. Bbox: {bbox}. Cannot determine inner color.") # Optional logging
        return None # Indicate failure


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize the output grid as a copy of the input grid
    output_grid = np.copy(input_np)
    
    # Step 1 & 2: Find the bounding box containing all non-zero pixels
    bbox = find_bounding_box(input_np)
    
    # If no non-zero pixels (and thus no bbox), return the grid unchanged
    if bbox is None:
        return output_grid.tolist()
        
    # Unpack bounding box coordinates
    min_r, min_c, max_r, max_c = bbox
    
    # Step 3, 4, 5, 6: Determine the color to use for filling (the 'inner' color)
    fill_color = get_inner_color(input_np, bbox)

    # If a valid fill color could not be determined (e.g., >2 colors, ambiguity),
    # return the grid unchanged to avoid incorrect modifications.
    if fill_color is None:
        # print("Warning: Could not determine a valid fill color. Returning original grid.") # Optional logging
        return output_grid.tolist() # Return the unmodified copy

    # Step 7 & 8: Iterate through each pixel *within* the bounding box
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            # Check if the pixel in the *original* input grid at this location was white (0)
            if input_np[r, c] == 0:
                # If it was white, change its color in the *output* grid to the determined fill_color
                output_grid[r, c] = fill_color
                
    # Step 9: Convert the final NumPy array back to a list of lists format
    return output_grid.tolist()