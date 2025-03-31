import numpy as np

"""
Transformation Rule:

1. Identify a composite object predominantly made of gray (5) pixels, located adjacent to either the left or right vertical edge of the input grid. This object has a fixed width of 5 columns, but its height can vary.
2. Determine the object's bounding box (top row, bottom row, left column, right column) and extract its pattern.
3. Determine the direction of movement: if the object is on the left edge, it moves right; if on the right edge, it moves left.
4. Calculate the target bounding box for the object on the opposite edge. The vertical position remains unchanged.
5. Create a copy of the input grid to serve as the output grid.
6. Clear the object's original location in the output grid by filling the original bounding box area with the background color (blue, 1).
7. Transform the extracted object pattern: For each row within the object pattern, starting from the 4th row (relative index 3), cyclically shift the pixels in that row to the right by `row_index - 2` positions (where row_index is the 0-based index within the pattern).
8. Draw the *transformed* object pattern onto the output grid at the calculated target bounding box location.
9. Identify the row index immediately below the object's original bottom row (`trail_row = original_bottom_row + 1`).
10. Determine the horizontal range for a 'trail' of maroon (9) pixels to be drawn in the `trail_row`:
    - If moving left: The trail spans from the column immediately to the right of the object's *final* right edge (`final_c2 + 1`) up to the object's *original* right edge (`original_c2`).
    - If moving right: The trail spans from the object's *original* left edge (`original_c1`) up to the object's *final* left edge (`final_c1`).
11. Fill the calculated trail range in the `trail_row` of the output grid with the trail color (maroon, 9), overwriting the existing color (typically magenta, 6).
12. Return the modified output grid.
"""

def find_object_bbox(grid):
    """
    Finds the bounding box of the gray object located at a vertical edge.
    Assumes the object width is 5.
    """
    height, width = grid.shape
    gray_color = 5
    object_width = 5

    coords = np.argwhere(grid == gray_color)
    if coords.size == 0:
        return None # No gray pixels found

    min_r, min_c = np.min(coords, axis=0)
    max_r, max_c = np.max(coords, axis=0)

    # Determine if object is on left or right edge based on gray pixel coords
    if min_c == 0 and max_c < object_width: # Likely on left edge
        c1 = 0
        c2 = object_width - 1
        # Find the actual vertical extent based on gray pixels within these columns
        edge_coords = coords[coords[:, 1] <= c2]
        r1 = np.min(edge_coords[:, 0])
        r2 = np.max(edge_coords[:, 0])
    elif max_c == width - 1 and min_c >= width - object_width : # Likely on right edge
        c2 = width - 1
        c1 = width - object_width
        # Find the actual vertical extent based on gray pixels within these columns
        edge_coords = coords[coords[:, 1] >= c1]
        r1 = np.min(edge_coords[:, 0])
        r2 = np.max(edge_coords[:, 0])
    else:
        # Object not clearly at an edge or doesn't fit width assumption
        return None 

    # Check if calculated width matches expected width
    if c2 - c1 + 1 != object_width:
         # This could happen if gray pixels don't span the full 5 assumed width
         # Might need refinement, but stick to assumption for now.
         print(f"Warning: Detected object width {c2 - c1 + 1} differs from expected {object_width}")

    return (r1, c1, r2, c2)

def transform_pattern(pattern):
    """
    Transforms the object pattern by cyclically shifting rows >= 3.
    """
    transformed = pattern.copy()
    height, width = pattern.shape
    for r in range(height):
        if r >= 3:
            shift = r - 2
            # Apply cyclic shift right using np.roll
            transformed[r, :] = np.roll(pattern[r, :], shift)
    return transformed

def transform(input_grid):
    """
    Applies the described transformation to the input grid.
    """
    # Convert input to numpy array
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    height, width = grid.shape
    
    background_color = 1
    trail_color = 9

    # 1. Find the object's original bounding box
    bbox_orig = find_object_bbox(grid)
    if bbox_orig is None:
        print("Error: Could not find object at edges.")
        return input_grid # Return original if object not found

    r1_orig, c1_orig, r2_orig, c2_orig = bbox_orig
    object_height = r2_orig - r1_orig + 1
    object_width = c2_orig - c1_orig + 1 # Should be 5 based on find_object_bbox logic

    # 2. Extract the original pattern
    pattern_orig = grid[r1_orig:r2_orig+1, c1_orig:c2_orig+1]

    # 3. Determine movement direction and final position
    direction = ''
    if c1_orig == 0:
        direction = 'right'
        c1_final = width - object_width
    elif c2_orig == width - 1:
        direction = 'left'
        c1_final = 0
    else:
        # Should not happen if find_object_bbox works correctly
        print("Error: Object not located at a known edge.")
        return input_grid 

    c2_final = c1_final + object_width - 1
    r1_final, r2_final = r1_orig, r2_orig # Vertical position is constant

    # 4. Clear the original location
    output_grid[r1_orig:r2_orig+1, c1_orig:c2_orig+1] = background_color

    # 5. Transform the pattern
    pattern_transformed = transform_pattern(pattern_orig)

    # 6. Draw the transformed pattern at the final location
    # Check bounds before drawing
    if r1_final + object_height <= height and c1_final + object_width <= width:
        output_grid[r1_final:r2_final+1, c1_final:c2_final+1] = pattern_transformed
    else:
         print("Warning: Final object position exceeds grid bounds.")
         # Handle clipping or return error if needed

    # 7. Determine trail row and draw the trail
    trail_row = r2_orig + 1
    if trail_row < height: # Check if trail row is within grid
        trail_start_col = -1
        trail_end_col = -1
        
        if direction == 'left':
            # Trail from column after final right edge to original right edge
            trail_start_col = c2_final + 1
            trail_end_col = c2_orig 
        elif direction == 'right':
            # Trail from original left edge to final left edge (inclusive)
            trail_start_col = c1_orig
            trail_end_col = c1_final

        # Ensure column indices are valid and in correct order for slicing
        if trail_start_col != -1 and trail_end_col != -1:
             actual_start = max(0, min(trail_start_col, trail_end_col))
             actual_end = min(width - 1, max(trail_start_col, trail_end_col))
             
             if actual_start <= actual_end:
                 output_grid[trail_row, actual_start:actual_end+1] = trail_color

    return output_grid.tolist() # Return as list of lists