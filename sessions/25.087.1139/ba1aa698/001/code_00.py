import numpy as np
from collections import Counter

"""
The transformation rule identifies repeating vertical subgrids separated by a border color (BC) within a larger grid framed by the same BC. Each subgrid contains a background color (BGC) and a marker object (MO) of a specific marker color (MC). The marker object maintains its shape across subgrids but shifts vertically by a constant amount (Diff) from one subgrid to the next. The output is a single subgrid structure (using the dimensions, BC, and BGC of the first input subgrid) where the marker object is placed at a new vertical position. This new position is calculated by taking the vertical position of the marker in the *last* input subgrid (P_last) and adding the constant vertical step (Diff). An adjustment is made: if the marker color (MC) is the same as the border color (BC), the calculated position is incremented by 1 before placing the marker.
"""

def find_colors(grid):
    """Identifies border, background, and marker colors."""
    # Border color is typically the frame color
    bc = grid[0, 0]

    # Find colors that are not the border color
    non_border_colors = Counter(grid[grid != bc].flatten())

    # Background color is usually the most frequent non-border color inside
    if not non_border_colors:
        # Handle cases where grid might be only border color or has unique internal structure
        # Let's assume the second most frequent overall color if available, or fallback needed
        all_counts = Counter(grid.flatten())
        if len(all_counts) > 1:
             bgc = all_counts.most_common(2)[1][0]
        else: # Only one color in grid
            bgc = bc # Or handle as error? Assume BGC can be BC.
    else:
        bgc = non_border_colors.most_common(1)[0][0]


    # Marker color is the remaining color (or potentially same as BC or BGC if complex)
    mc = bc # Default assumption if only BC and BGC found
    unique_colors = np.unique(grid)
    potential_mc = [c for c in unique_colors if c != bc and c != bgc]
    if len(potential_mc) == 1:
        mc = potential_mc[0]
    elif len(potential_mc) > 1:
        # More complex case - need a better way to identify marker
        # Maybe check which color forms small connected components inside subgrids
        # For now, let's look for the color with the smallest count among non-BC/non-BGC
        min_count = float('inf')
        best_mc = mc
        for color, count in non_border_colors.items():
             if color != bgc and count < min_count:
                 min_count = count
                 best_mc = color
        mc = best_mc

    # Special case check: If the marker object pixels are the same color as the border
    # We need to find the object later to confirm its color.
    # Let's refine MC detection after finding the object.

    return bc, bgc, mc # Initial guess for MC

def find_separators(grid, bc):
    """Finds the column indices of vertical separators."""
    cols = grid.shape[1]
    separators = []
    for c in range(cols):
        if np.all(grid[:, c] == bc):
            separators.append(c)
    return separators

def find_marker_in_subgrid(subgrid_content, bgc, bc):
    """Finds the marker object, its color, shape (relative coords), and top-left pos within content."""
    marker_pixels = np.argwhere((subgrid_content != bgc) & (subgrid_content != bc))
    if marker_pixels.size == 0:
         # Check if marker might be BC color
         marker_pixels = np.argwhere(subgrid_content != bgc) # Look for anything not BGC
         if marker_pixels.size == 0:
             return None, None, -1, -1, -1 # No marker found

    # Assume marker is a single connected component
    # Find the top-left point of the marker area
    min_r, min_c = marker_pixels.min(axis=0)

    # Determine marker color from the first found pixel
    mc = subgrid_content[min_r, min_c]

    # Extract relative coordinates and shape
    marker_shape_coords = marker_pixels - np.array([min_r, min_c])
    
    # Create a minimal bounding box representation of the shape if needed, or just use coords
    # For now, relative coords are sufficient

    return mc, marker_shape_coords, min_r, min_c

def transform(input_grid):
    """
    Applies the transformation rule based on subgrid repetition and marker movement.
    """
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape

    # 1. Analyze the input grid
    bc, bgc, initial_mc_guess = find_colors(grid) # MC guess might be refined
    separators = find_separators(grid, bc)

    if not separators or len(separators) < 2:
        # Cannot determine subgrids
        print("Error: Could not determine subgrid structure.")
        return input_grid # Or raise error

    # 2. Determine subgrid structure
    subgrid_width = separators[1] - separators[0] # Includes borders
    num_subgrids = len(separators) - 1
    subgrid_height = height

    # 3. Extract marker info from each subgrid
    marker_positions = [] # Stores (absolute_top_row, relative_left_col, marker_shape_coords, actual_mc)
    last_marker_shape = None
    last_relative_c = -1
    actual_mc = -1 # Final determined marker color

    for i in range(num_subgrids):
        start_col = separators[i] + 1
        end_col = separators[i+1]
        if start_col >= end_col: continue # Handle adjacent separators

        subgrid_content = grid[:, start_col:end_col]

        mc_found, shape_coords, rel_r, rel_c = find_marker_in_subgrid(subgrid_content, bgc, bc)

        if shape_coords is not None:
            abs_top_row = rel_r
            # Refine MC based on actual found object
            if actual_mc == -1:
                 actual_mc = mc_found
            elif mc_found != actual_mc:
                 print(f"Warning: Inconsistent marker color found in subgrid {i}. Using {actual_mc}")

            marker_positions.append((abs_top_row, rel_c, shape_coords, actual_mc))
            last_marker_shape = shape_coords
            last_relative_c = rel_c
        # else: No marker found in this subgrid, might indicate an issue or pattern break

    if len(marker_positions) < 2:
         print("Error: Need at least two markers to determine movement.")
         # Fallback: Maybe return the first subgrid as is?
         output_grid_skel = grid[:, separators[0]:separators[1]+1].copy()
         return output_grid_skel.tolist()


    # 4. Calculate vertical step (Diff)
    p1 = marker_positions[0][0]
    p2 = marker_positions[1][0]
    diff = p2 - p1

    # 5. Get last marker position (P_last)
    p_last = marker_positions[-1][0]

    # 6. Calculate target output row
    output_row = p_last + diff

    # 7. Apply adjustment if MC == BC
    if actual_mc == bc:
        output_row += 1
        
    # Ensure calculated row is within bounds (optional, based on ARC rules)
    # output_row = max(0, min(output_row, subgrid_height - max_marker_height)) 
    # Need marker height for precise boundary check. Let's assume it fits for now.


    # 8. Create the output grid structure (copy first subgrid frame/bg)
    output_grid = grid[:, separators[0]:separators[1]].copy() # Copy content area + left border
    output_grid = np.insert(output_grid, output_grid.shape[1], grid[:, separators[1]], axis=1) # Add right border
    
    # Ensure the interior is filled with BGC (might be needed if first subgrid had marker overlapping default BGC)
    output_grid[:, 1:-1] = bgc # Fill content area between borders with BGC

    # 9. Place the marker object in the output grid
    if last_marker_shape is not None and actual_mc != -1:
        marker_abs_col_start = 1 + last_relative_c # 1 for left border offset

        for dr, dc in last_marker_shape:
            r_out = output_row + dr
            c_out = marker_abs_col_start + dc

            # Check bounds before placing pixel
            if 0 <= r_out < output_grid.shape[0] and 0 <= c_out < output_grid.shape[1]:
                # Ensure we don't overwrite the border unless MC == BC
                is_border_col = (c_out == 0 or c_out == output_grid.shape[1] - 1)
                if not is_border_col or actual_mc == bc:
                     output_grid[r_out, c_out] = actual_mc
                # else: Don't draw marker over border if MC != BC (though this case seems less likely by problem design)

    return output_grid.tolist()