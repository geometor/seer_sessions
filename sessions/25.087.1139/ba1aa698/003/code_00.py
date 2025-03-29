import numpy as np
from collections import Counter

"""
The transformation identifies repeating vertical subgrids separated by a border color (BC) within a larger grid framed by the same BC. Each subgrid contains a background color (BGC) and a marker object (MO) of a specific marker color (MC). The marker object maintains its shape across subgrids but its top-left position shifts vertically by a constant amount (Diff) from one subgrid to the next, while maintaining its relative horizontal position within the subgrid's content area. 

The transformation rule is to:
1. Isolate the first subgrid (including its borders) as a template for the output.
2. Identify the BC, BGC, MC, marker shape, and marker positions (P_row) in each input subgrid.
3. Calculate the vertical step difference (Diff = P_row_i+1 - P_row_i).
4. Determine the last marker's row position (P_last).
5. Calculate the target output row (Target_Row = P_last + Diff).
6. Apply an adjustment: If MC is the same as BC, increment Target_Row by 1.
7. Create the output grid by copying the template.
8. Fill the content area of the output grid (inside the borders) with BGC.
9. Place the marker object (using its shape and MC) onto the output grid, starting at the calculated Target_Row and its original relative horizontal column position within the content area. Ensure marker pixels only overwrite border pixels if MC equals BC.
"""

def find_colors(grid):
    """Identifies border, background, and potential marker colors."""
    # Border color (BC) is assumed to be the color of the top-left pixel (frame).
    bc = grid[0, 0]

    # Create a mask for the content area (excluding the frame/border)
    content_mask = np.ones(grid.shape, dtype=bool)
    content_mask[0, :] = False
    content_mask[-1, :] = False
    content_mask[:, 0] = False
    content_mask[:, -1] = False

    # Find colors within the general content area (might include markers)
    # Exclude border columns as well for BGC calculation
    inner_content_mask = content_mask.copy()
    for c in range(grid.shape[1]):
         if np.all(grid[:, c] == bc):
              inner_content_mask[:,c] = False

    # Count colors in the inner content that are not the border color
    non_border_content_colors = Counter(grid[inner_content_mask & (grid != bc)].flatten())

    # Background color (BGC) is the most frequent non-border color in the content.
    if not non_border_content_colors:
        # If no non-border colors, BGC might be same as BC or need fallback.
        # Count all non-border colors across the whole grid as a fallback.
        all_non_border = Counter(grid[grid != bc].flatten())
        if not all_non_border:
            bgc = bc # Grid is only border color
        else:
             bgc = all_non_border.most_common(1)[0][0] # Use most common non-border overall
    else:
        bgc = non_border_content_colors.most_common(1)[0][0]

    # Marker color (MC) is likely the least frequent color that isn't BC or BGC.
    # This is an initial guess; it will be confirmed by finding the marker object.
    mc_guess = bc # Default assumption
    unique_colors = np.unique(grid)
    potential_mc = [c for c in unique_colors if c != bc and c != bgc]

    if len(potential_mc) == 1:
        mc_guess = potential_mc[0]
    elif len(potential_mc) > 1:
        # If multiple candidates, use counts from the non-border content area
        min_count = float('inf')
        best_mc = mc_guess
        for color, count in non_border_content_colors.items():
            if color != bgc and count < min_count:
                min_count = count
                best_mc = color
        mc_guess = best_mc

    return bc, bgc, mc_guess

def find_separators(grid, bc):
    """Finds the column indices of vertical separators (full columns of BC)."""
    cols = grid.shape[1]
    separators = []
    for c in range(cols):
        if np.all(grid[:, c] == bc):
            separators.append(c)
    # Ensure the first and last columns are included if they are borders
    if 0 not in separators and np.all(grid[:, 0] == bc):
        separators.insert(0, 0)
    if cols - 1 not in separators and np.all(grid[:, cols - 1] == bc):
         separators.append(cols-1)
    # Sort just in case insertion messed order, and remove duplicates
    separators = sorted(list(set(separators)))
    return separators


def find_marker_in_subgrid_content(subgrid_content, bgc, bc):
    """
    Finds the marker object within a subgrid's content area.
    Returns: (marker_shape_coords, marker_color, rel_row, rel_col)
    rel_row, rel_col are relative to the top-left of the subgrid_content.
    Returns (None, -1, -1, -1) if no marker found.
    """
    # Marker pixels are those not matching BGC or BC (unless MC == BC)
    marker_pixels = np.argwhere((subgrid_content != bgc) & (subgrid_content != bc))

    mc = -1
    # If nothing found, check if the marker could be the same color as BC
    if marker_pixels.size == 0:
        marker_pixels = np.argwhere(subgrid_content != bgc) # Look for anything not BGC
        if marker_pixels.size > 0:
             # Potential marker found, check its color - it must be BC
             temp_mc = subgrid_content[marker_pixels[0,0], marker_pixels[0,1]]
             if temp_mc == bc:
                  mc = bc # Confirmed: marker color is border color
             else: # Found something else, not matching expected pattern
                  marker_pixels = np.array([]) # Reset

    if marker_pixels.size == 0:
        return None, -1, -1, -1 # No marker found

    # Determine marker color if not already set (i.e., if MC != BC)
    if mc == -1:
        mc = subgrid_content[marker_pixels[0, 0], marker_pixels[0, 1]]

    # Find the top-left point of the marker relative to the subgrid_content
    min_r, min_c = marker_pixels.min(axis=0)

    # Extract relative coordinates defining the shape
    marker_shape_coords = marker_pixels - np.array([min_r, min_c])

    return marker_shape_coords, mc, min_r, min_c

def transform(input_grid):
    """
    Applies the transformation rule based on subgrid repetition and marker movement extrapolation.
    """
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape

    # 1. Identify colors
    bc, bgc, mc_guess = find_colors(grid)

    # 2. Locate vertical separators
    separators = find_separators(grid, bc)

    if not separators or len(separators) < 2:
        # Cannot determine subgrids - return input or handle error
        # Based on problem structure, likely indicates an issue
        # For robustness, maybe return input or a default grid? Let's return input.
        # print("Error: Could not determine subgrid structure.")
        return input_grid # Return original if structure unclear

    # 3. Define the output template (first subgrid including borders)
    # Ensure separators define a valid first subgrid
    if separators[1] <= separators[0]:
         # print("Error: Invalid separator definition for first subgrid.")
         return input_grid # Invalid structure
    output_template = grid[:, separators[0]:separators[1]+1]
    template_h, template_w = output_template.shape

    # 4. Analyze subgrids to find markers and movement
    marker_positions = [] # Stores (absolute_row, relative_col_in_content, shape_coords, actual_mc)
    last_marker_shape = None
    last_relative_c = -1
    actual_mc = -1 # Final determined marker color

    num_subgrids = len(separators) - 1
    for i in range(num_subgrids):
        start_col = separators[i] + 1
        end_col = separators[i+1]

        # Check for valid content area dimensions
        if start_col >= end_col or 1 >= height - 1:
            # print(f"Warning: Skipping subgrid {i} due to invalid dimensions.")
            continue # Skip if content area is zero width or height

        # Extract the content area (excluding borders)
        subgrid_content = grid[1:height-1, start_col:end_col]

        # Find marker within this content area
        shape_coords, mc_found, rel_r, rel_c = find_marker_in_subgrid_content(subgrid_content, bgc, bc)

        if shape_coords is not None:
            # Calculate absolute row position relative to the *full* subgrid height
            abs_top_row = rel_r + 1 # Add 1 because content starts at row index 1

            # Determine/confirm actual marker color
            if actual_mc == -1:
                 actual_mc = mc_found
            elif mc_found != actual_mc:
                 # Handle inconsistency if needed, e.g., raise error or use first found
                 # print(f"Warning: Inconsistent marker color found ({mc_found} vs {actual_mc}). Using {actual_mc}.")
                 pass # Keep using the first MC found

            # Store marker info: absolute row, relative col *within content*, shape, color
            marker_positions.append((abs_top_row, rel_c, shape_coords, actual_mc))
            last_marker_shape = shape_coords
            last_relative_c = rel_c # Store relative col within content
        # else: Marker not found in this subgrid, could be intentional or an error

    # If MC wasn't found via objects, use the initial guess (might occur if grid has no markers)
    if actual_mc == -1:
        actual_mc = mc_guess

    # 5. Calculate movement if possible
    if len(marker_positions) < 2:
        # Cannot determine movement, return the template grid as is (or handle error)
        # print("Error: Need at least two markers to determine movement. Returning template.")
        # Create a clean template grid (filled with BGC)
        output_grid = output_template.copy()
        output_grid[1:template_h-1, 1:template_w-1] = bgc
        # Attempt to place the single marker found, if any
        if len(marker_positions) == 1 and last_marker_shape is not None:
             p_row, p_rel_c, _, _ = marker_positions[0]
             abs_marker_col_start = 1 + p_rel_c
             for dr, dc in last_marker_shape:
                 r_out, c_out = p_row + dr, abs_marker_col_start + dc
                 if 0 <= r_out < template_h and 0 <= c_out < template_w:
                     is_border = (r_out == 0 or r_out == template_h - 1 or
                                  c_out == 0 or c_out == template_w - 1)
                     if not is_border or actual_mc == bc:
                         output_grid[r_out, c_out] = actual_mc
        return output_grid.tolist()


    # 6. Calculate vertical step (Diff)
    p1_row = marker_positions[0][0]
    p2_row = marker_positions[1][0]
    diff = p2_row - p1_row

    # 7. Get last marker position (P_last_row)
    p_last_row = marker_positions[-1][0]

    # 8. Calculate target output row
    output_row = p_last_row + diff

    # 9. Apply adjustment if MC == BC
    if actual_mc == bc:
        output_row += 1

    # 10. Create the output grid (copy of template)
    output_grid = output_template.copy()

    # 11. Fill the content area with BGC
    # Ensure indices are valid before slicing
    if template_h > 2 and template_w > 2:
        output_grid[1:template_h-1, 1:template_w-1] = bgc

    # 12. Place the marker object in the output grid
    if last_marker_shape is not None and last_relative_c != -1:
        # Calculate absolute column start based on relative col in content
        abs_marker_col_start = 1 + last_relative_c # Add 1 for the left border column

        for dr, dc in last_marker_shape:
            # Calculate target coordinates in the output grid
            r_out = output_row + dr
            c_out = abs_marker_col_start + dc

            # Check bounds before placing pixel
            if 0 <= r_out < template_h and 0 <= c_out < template_w:
                # Check if the target location is a border pixel
                is_border_pixel = (r_out == 0 or r_out == template_h - 1 or
                                   c_out == 0 or c_out == template_w - 1)

                # Place the marker pixel if:
                # - It's not a border pixel OR
                # - It is a border pixel AND the marker color matches the border color
                if not is_border_pixel or actual_mc == bc:
                     output_grid[r_out, c_out] = actual_mc
                # Otherwise, do not overwrite a border pixel with a non-border marker color

    # Convert final grid to list format for ARC standard
    return output_grid.tolist()