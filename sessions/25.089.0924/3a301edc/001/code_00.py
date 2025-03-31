import numpy as np

"""
Transforms the input grid based on the following rules:

1. Identify all non-white (non-zero) pixels in the input grid.
2. Determine the minimal bounding box that encloses all these non-white pixels.
3. Identify the two distinct non-white colors present within this bounding box.
4. Determine which of these two colors corresponds to the 'inner' object. This can be identified as the non-white color whose pixels do not touch the edge of the minimal bounding box. This color becomes the 'fill_color'.
5. Iterate through each pixel within the calculated bounding box.
6. If a pixel inside the bounding box has the background color (white, 0) in the input grid, change its color in the output grid to the 'fill_color'.
7. Pixels outside the bounding box and pixels that were originally non-white remain unchanged.
"""

def find_bounding_box(grid):
    """Finds the minimum bounding box containing all non-zero pixels."""
    non_zero_coords = np.argwhere(grid != 0)
    if non_zero_coords.size == 0:
        return None  # No non-zero pixels found
    min_r, min_c = non_zero_coords.min(axis=0)
    max_r, max_c = non_zero_coords.max(axis=0)
    return (min_r, min_c, max_r, max_c)

def get_inner_color(grid, bbox):
    """Determines the inner color within the bounding box."""
    min_r, min_c, max_r, max_c = bbox
    
    # Extract the subgrid defined by the bounding box
    subgrid = grid[min_r:max_r+1, min_c:max_c+1]
    
    # Find unique non-zero colors within the subgrid
    unique_colors = np.unique(subgrid[subgrid != 0])
    
    if len(unique_colors) != 2:
        # Handle edge cases or unexpected inputs if necessary
        # For this specific problem structure, we expect exactly two colors.
        # If only one color, maybe return that color? Or raise error?
        # Let's assume the problem guarantees two colors.
        # If only one color, maybe it acts as both inner and outer? 
        # Example 4 has inner=red, outer=blue. Fills with red.
        # If input was just the blue frame, what would happen? Undefined by examples.
        # If input was just the red center, what would happen? Undefined.
        # Let's stick to the 2-color assumption derived from examples.
        # If it fails on a test case, we'll revisit.
         if len(unique_colors) == 1:
             return unique_colors[0] # Or handle differently if required by future tests
         else: # 0 or >2 colors
             return None # Cannot determine based on observed pattern

    color1, color2 = unique_colors
    
    # Check which color touches the boundary of the *bounding box*
    color1_touches_boundary = False
    color2_touches_boundary = False

    for r in range(min_r, max_r + 1):
        if grid[r, min_c] == color1 or grid[r, max_c] == color1:
            color1_touches_boundary = True
        if grid[r, min_c] == color2 or grid[r, max_c] == color2:
            color2_touches_boundary = True
        if color1_touches_boundary and color2_touches_boundary:
            break # No need to check further rows if both already touch

    if not (color1_touches_boundary and color2_touches_boundary): # Only check cols if necessary
         for c in range(min_c, max_c + 1):
            if grid[min_r, c] == color1 or grid[max_r, c] == color1:
                color1_touches_boundary = True
            if grid[min_r, c] == color2 or grid[max_r, c] == color2:
                color2_touches_boundary = True
            if color1_touches_boundary and color2_touches_boundary:
                break # No need to check further columns

    # The inner color is the one that DOES NOT touch the boundary
    if color1_touches_boundary and not color2_touches_boundary:
        return color2
    elif not color1_touches_boundary and color2_touches_boundary:
        return color1
    else:
        # This case (both touch or neither touch) shouldn't happen based on examples
        # Or could happen if the inner object touches the bounding box edge too.
        # Let's reconsider the definition - the fill color is the color of the object
        # *fully contained* within the other.
        # Find all coordinates for each color within the bbox
        coords1 = np.argwhere(grid[min_r:max_r+1, min_c:max_c+1] == color1) + [min_r, min_c]
        coords2 = np.argwhere(grid[min_r:max_r+1, min_c:max_c+1] == color2) + [min_r, min_c]

        # Check if any coord lies on the bbox edge
        c1_on_edge = any(r == min_r or r == max_r or c == min_c or c == max_c for r, c in coords1)
        c2_on_edge = any(r == min_r or r == max_r or c == min_c or c == max_c for r, c in coords2)

        if c1_on_edge and not c2_on_edge:
             return color2 # Color 2 is inner
        elif not c1_on_edge and c2_on_edge:
             return color1 # Color 1 is inner
        else:
             # If both touch or neither touch (e.g., single pixel object?), this logic fails.
             # Based on examples, one color forms the outer frame touching the bbox edge.
             # Let's default to assuming the one *not* on the edge is inner. If both are,
             # this might need refinement based on other properties (e.g., smaller area?).
             # For now, returning None or raising error might be safer if ambiguity arises.
             print(f"Ambiguous inner/outer color: C1 on edge: {c1_on_edge}, C2 on edge: {c2_on_edge}. Colors: {color1}, {color2}")
             # Perhaps count pixels? The inner object usually has fewer pixels.
             if len(coords1) < len(coords2):
                 return color1
             elif len(coords2) < len(coords1):
                 return color2
             else:
                # If counts are equal and both/neither touch edge, truly ambiguous from rules derived so far.
                 return None # Or raise an error


def transform(input_grid):
    """
    Transforms the input grid by finding the bounding box of non-white pixels,
    identifying the inner color, and filling the white space within the 
    bounding box with the inner color.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)
    
    # Find the bounding box of all non-white shapes
    bbox = find_bounding_box(output_grid)
    
    # If no non-white pixels or bounding box not found, return the original grid
    if bbox is None:
        return output_grid.tolist()
        
    min_r, min_c, max_r, max_c = bbox
    
    # Determine the color to fill with (the 'inner' color)
    fill_color = get_inner_color(output_grid, bbox)

    # If we couldn't determine a fill color (e.g., not exactly 2 colors, ambiguity)
    # return the grid unchanged, or handle as appropriate for the ambiguity.
    if fill_color is None:
        print("Warning: Could not determine unique inner fill color.")
        return output_grid.tolist() # Return unchanged

    # Iterate through the pixels within the bounding box
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            # If the pixel in the *original* input was white (0)
            if input_np[r, c] == 0:
                # Change the corresponding pixel in the output grid to the fill_color
                output_grid[r, c] = fill_color
                
    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
