import numpy as np

def _find_borders(grid):
    """
    Identifies the two border lines (top/bottom or left/right) and their colors.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: (border_type, color1, edge1, color2, edge2) or None if no valid borders found.
               border_type is 'horizontal' or 'vertical'.
               color1, color2 are the border colors.
               edge1, edge2 are the row/column indices of the borders.
    """
    height, width = grid.shape

    # Check horizontal borders (top and bottom rows)
    top_row = grid[0, :]
    bottom_row = grid[height - 1, :]
    if len(np.unique(top_row)) == 1 and top_row[0] != 0 and \
       len(np.unique(bottom_row)) == 1 and bottom_row[0] != 0:
        return 'horizontal', top_row[0], 0, bottom_row[0], height - 1

    # Check vertical borders (left and right columns)
    left_col = grid[:, 0]
    right_col = grid[:, width - 1]
    if len(np.unique(left_col)) == 1 and left_col[0] != 0 and \
       len(np.unique(right_col)) == 1 and right_col[0] != 0:
        return 'vertical', left_col[0], 0, right_col[0], width - 1

    return None # Should not happen based on examples

def _get_neighbors(r, c, height, width):
    """ Gets orthogonal neighbor coordinates within grid bounds. """
    neighbors = []
    if r > 0: neighbors.append((r - 1, c))
    if r < height - 1: neighbors.append((r + 1, c))
    if c > 0: neighbors.append((r, c - 1))
    if c < width - 1: neighbors.append((r, c + 1))
    return neighbors

def transform(input_grid):
    """
    Transforms the input grid based on the proximity of blue pixels (1) to borders.

    1. Identifies two single-color borders (either top/bottom rows or left/right columns).
    2. For each blue pixel (1) not on a border:
        a. Determines which of the two borders it is closer to (based on row/col index).
        b. Finds the orthogonally adjacent white neighbor (0) that is closest to that same border.
        c. Recolors that specific white neighbor with the color of the closer border.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape
    output_grid = np.copy(input_grid_np)

    # 1. Identify borders
    border_info = _find_borders(input_grid_np)
    if not border_info:
        # Fallback or error handling if borders aren't as expected
        return output_grid.tolist() 
    border_type, color1, edge1, color2, edge2 = border_info

    # Define border ranges to exclude blue pixels on borders
    border_rows = set()
    border_cols = set()
    if border_type == 'horizontal':
        border_rows.add(edge1)
        border_rows.add(edge2)
    else: # vertical
        border_cols.add(edge1)
        border_cols.add(edge2)

    # 2. Find and process each blue pixel
    blue_pixels = []
    for r in range(height):
        for c in range(width):
            # Exclude pixels on the border lines themselves
            if r in border_rows or c in border_cols:
                continue
            if input_grid_np[r, c] == 1:
                blue_pixels.append((r, c))

    for r_blue, c_blue in blue_pixels:
        # 2a. Determine closer border
        closer_border_color = -1
        closer_border_edge = -1
        min_dist_to_border = float('inf')

        if border_type == 'horizontal':
            dist1 = abs(r_blue - edge1)
            dist2 = abs(r_blue - edge2)
            if dist1 < dist2:
                closer_border_color = color1
                closer_border_edge = edge1
                min_dist_to_border = dist1
            elif dist2 < dist1:
                closer_border_color = color2
                closer_border_edge = edge2
                min_dist_to_border = dist2
            # else: equal distance, do nothing based on implicit rule from examples
        else: # vertical
            dist1 = abs(c_blue - edge1)
            dist2 = abs(c_blue - edge2)
            if dist1 < dist2:
                closer_border_color = color1
                closer_border_edge = edge1
                min_dist_to_border = dist1
            elif dist2 < dist1:
                closer_border_color = color2
                closer_border_edge = edge2
                min_dist_to_border = dist2
            # else: equal distance, do nothing

        # If a closer border was identified (not equidistant)
        if closer_border_color != -1:
            
            # 2b. Find orthogonal white neighbors
            potential_targets = []
            neighbors = _get_neighbors(r_blue, c_blue, height, width)
            for nr, nc in neighbors:
                if input_grid_np[nr, nc] == 0: # Must be white in the input
                    potential_targets.append((nr, nc))

            # 2c. Find the neighbor closest to the closer border
            target_neighbor = None
            min_neighbor_dist = float('inf')

            for tr, tc in potential_targets:
                if border_type == 'horizontal':
                    dist = abs(tr - closer_border_edge)
                else: # vertical
                    dist = abs(tc - closer_border_edge)

                # Check if this neighbor is strictly closer than the current best
                # Using <= allows picking one if multiple are equally close, 
                # favoring the one encountered first (or based on iteration order).
                # Examples suggest a unique closest neighbor exists. Let's assume strict minimum for now.
                # If strict '<' fails tests, change to '<='
                if dist < min_neighbor_dist:
                     min_neighbor_dist = dist
                     target_neighbor = (tr, tc)
                # Handle ties explicitly if needed later based on testing

            # 2d. Recolor the target neighbor
            if target_neighbor:
                tr, tc = target_neighbor
                # Check if the target is not already colored by another blue pixel's rule in this pass
                # Although the logic seems deterministic, this prevents accidental overwrites if logic gets complex
                # For this specific task, it might be redundant if each blue influences at most one white.
                if output_grid[tr, tc] == 0: # Ensure we only color originally white pixels
                   output_grid[tr, tc] = closer_border_color


    return output_grid.tolist()