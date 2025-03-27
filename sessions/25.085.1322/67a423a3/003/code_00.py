"""
Identifies a horizontal and a vertical line in the input grid, determines their intersection point (r, c), and modifies a 3x3 area centered at this intersection in a copy of the input grid. The 3x3 area is initially filled entirely with yellow (4). Then, only the center pixel (r, c) within this area is restored to its original color from the input grid. All other pixels within the 3x3 area (horizontal neighbors, vertical neighbors, and corners) remain yellow.
"""

import numpy as np

def find_lines(grid):
    """
    Finds the main horizontal and vertical lines and their intersection.
    Handles both continuous lines and specific fragmented lines observed in examples.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: (row_index, col_index, horizontal_color, vertical_color)
               Returns (None, None, None, None) if lines are not found.
    """
    rows, cols = grid.shape
    horizontal_line_info = None
    vertical_line_info = None

    # Find horizontal line: look for the row with the most non-background pixels
    # belonging to a single color, assuming this represents the line.
    max_h_count = 0
    for r in range(rows):
        non_bg_pixels = grid[r, grid[r, :] != 0]
        if len(non_bg_pixels) > 0:
            colors, counts = np.unique(non_bg_pixels, return_counts=True)
            most_common_idx = np.argmax(counts)
            count = counts[most_common_idx]
            color = colors[most_common_idx]
            # Use the row with the maximum count of a single non-bg color
            # Break ties by choosing the first one found (usually lower index)
            # Consider line must span at least 2 cells
            if count > 1 and count > max_h_count:
                 max_h_count = count
                 horizontal_line_info = (r, color)
            elif count == max_h_count and horizontal_line_info is None: # Handle first potential line
                 horizontal_line_info = (r, color)


    # Find vertical line: similar logic for columns.
    max_v_count = 0
    for c in range(cols):
        non_bg_pixels = grid[grid[:, c] != 0, c]
        if len(non_bg_pixels) > 0:
            colors, counts = np.unique(non_bg_pixels, return_counts=True)
            most_common_idx = np.argmax(counts)
            count = counts[most_common_idx]
            color = colors[most_common_idx]
            # Use the column with the maximum count of a single non-bg color
            if count > 1 and count > max_v_count:
                max_v_count = count
                vertical_line_info = (c, color)
            elif count == max_v_count and vertical_line_info is None: # Handle first potential line
                 vertical_line_info = (c, color)

    # Handle Example 2 specifically: If vertical line detection yields green (3)
    # but it's fragmented (count <= 1 in any single column), find the column
    # containing green (3) that intersects the found horizontal line.
    # This is a bit heuristic based on observation.
    if horizontal_line_info and not vertical_line_info:
        r_h, color_h = horizontal_line_info
        # Check if green exists anywhere and could form the vertical 'line'
        green_cols = np.where(np.any(grid == 3, axis=0))[0]
        if len(green_cols) > 0:
             # Find the green column that intersects the horizontal line row
             for c_test in green_cols:
                 if grid[r_h, c_test] != 0: # Intersection exists
                     # Check if this column contains *mostly* green, even if fragmented
                     col_pixels = grid[:, c_test]
                     non_bg_col_pixels = col_pixels[col_pixels != 0]
                     if len(non_bg_col_pixels) > 0:
                         colors, counts = np.unique(non_bg_col_pixels, return_counts=True)
                         if colors[np.argmax(counts)] == 3:
                             vertical_line_info = (c_test, 3)
                             break # Found the fragmented green line intersection

    if horizontal_line_info and vertical_line_info:
        r, color_h = horizontal_line_info
        c, color_v = vertical_line_info
        # Basic check: ensure the determined intersection point isn't background.
        # Although the logic should inherently find non-background intersections.
        if grid[r, c] != 0:
             return r, c, color_h, color_v
        else:
             # If intersection is background, the line finding might be flawed.
             # Try refining search or default to first non-zero?
             # For now, rely on the primary detection logic.
             # Let's try finding the column based on color_v intersecting row r
             potential_cols = np.where(grid[r,:] == color_v)[0]
             if len(potential_cols) > 0 :
                 c = potential_cols[0] # Take the first one
                 return r, c, color_h, color_v
             # And vice versa
             potential_rows = np.where(grid[:,c] == color_h)[0]
             if len(potential_rows) > 0:
                 r = potential_rows[0]
                 return r, c, color_h, color_v

    print(f"Warning: Could not definitively find lines/intersection in grid:\n{grid}")
    return None, None, None, None # Indicate failure


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # 1. & 2. Identify Lines and Find Intersection
    r, c, color_h, color_v = find_lines(input_grid)

    if r is None or c is None:
        # If lines aren't found, return the input unchanged
        print("Error: Lines or intersection not found. Returning original grid.")
        return np.copy(input_grid)

    # 3. Initialize Output
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # 4. Apply Yellow Square
    # Define the 3x3 area boundaries, respecting grid limits
    min_r = max(0, r - 1)
    max_r = min(rows - 1, r + 1)
    min_c = max(0, c - 1)
    max_c = min(cols - 1, c + 1)

    # Fill the 3x3 area with yellow (4)
    output_grid[min_r : max_r + 1, min_c : max_c + 1] = 4

    # 5. Restore Center
    # Ensure the center (r, c) is valid (should be if found by find_lines)
    if 0 <= r < rows and 0 <= c < cols:
        output_grid[r, c] = input_grid[r, c]

    # 6. Final Output (horizontal neighbors, vertical neighbors, corners remain yellow)
    return output_grid