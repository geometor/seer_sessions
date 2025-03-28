import numpy as np
from collections import Counter, deque

"""
Transformation Rule:

1.  Get Input Dimensions: Determine the height (`H`) and width (`W`) of the input grid.
2.  Identify Input Frame Color: Read the color value at `input_grid[1, 0]`. Store this as `Input Frame Color`. Handle cases where H < 2.
3.  Define Content Area: Specify the boundaries for the content area: rows 2 to `H-2` (inclusive) and columns 1 to `W-2` (inclusive). Handle cases where H < 3 or W < 3.
4.  Count Content Colors: Iterate through each pixel within the input grid's `Content Area`. Count the occurrences of each color, *excluding* white (0) and the `Input Frame Color`.
5.  Determine Output Fill Color: Find the color with the highest frequency count from Step 4. If no applicable colors are found, default to white (0). Store this as `Output Fill Color`.
6.  Initialize Output Grid: Create a new grid of the same dimensions (`H` x `W`) as the input grid, filled entirely with white (0).
7.  Copy Top Row: If `H > 0`, copy the first row (index 0) from the input grid to the output grid.
8.  Construct Output Frame: If `H >= 2` and `W >= 2`:
    *   Fill the entire second row (index 1) of the output grid with the `Output Fill Color`.
    *   Fill the first column (index 0) from row 1 down (rows 1 to `H-1`) with the `Output Fill Color`.
    *   Fill the last column (index `W-1`) from row 1 down (rows 1 to `H-1`) with the `Output Fill Color`.
    *   Fill the last row (index `H-1`) from column 1 to `W-2` (inclusive) with the `Output Fill Color`.
9.  Identify Seed Points: If `H >= 3` and `W >= 3`, find all coordinates `(r, c)` within the input grid's `Content Area` (rows 2 to `H-2`, cols 1 to `W-2`) where the pixel color `input_grid[r, c]` equals the `Output Fill Color`. Store these as `Seed Points`.
10. Place Seeds in Output: For each `(r, c)` in `Seed Points`, set the corresponding pixel `output_grid[r, c]` to the `Output Fill Color`.
11. Perform Constrained Flood Fill: If `H >= 3` and `W >= 3`:
    *   Initialize a queue with all `Seed Points`.
    *   Initialize a set `visited` with all `Seed Points`.
    *   While the queue is not empty:
        *   Dequeue a coordinate `(r, c)`.
        *   For each 4-way adjacent neighbor `(nr, nc)` of `(r, c)`:
            *   Check if `(nr, nc)` is within the `Content Area` boundaries (rows 2 to `H-2`, cols 1 to `W-2`).
            *   Check if `(nr, nc)` has not been visited.
            *   Check if the target pixel in the output grid `output_grid[nr, nc]` is currently white (0).
            *   Check if the corresponding pixel in the *input* grid `input_grid[nr, nc]` is either white (0) OR the `Output Fill Color`.
            *   If *all* conditions are true:
                *   Set `output_grid[nr, nc]` to the `Output Fill Color`.
                *   Mark `(nr, nc)` as visited.
                *   Enqueue `(nr, nc)`.
12. Handle Small Grids: If `H < 3` or `W < 3`, skip steps 9-11. The grid after step 8 is the result (or a simplified version if H/W are very small). A specific rule applied fills rows > 0 with the output_fill_color if H < 3 or W < 3.
13. Return Output Grid: The final `output_grid` is the result.
"""


def _find_most_frequent_inner_color(input_grid, frame_color, inner_bounds):
    """
    Counts colors in the defined inner area, excluding white (0)
    and the frame_color, and returns the most frequent one.

    Args:
        input_grid (np.ndarray): The input grid.
        frame_color (int): The color of the input frame (row 1).
        inner_bounds (dict): Dictionary with 'row_start', 'row_end', 'col_start', 'col_end'.

    Returns:
        int: The most frequent color, or 0 if none found or area invalid.
    """
    r_start, r_end = inner_bounds['row_start'], inner_bounds['row_end']
    c_start, c_end = inner_bounds['col_start'], inner_bounds['col_end']

    # Check if the inner area is valid dimension-wise
    if r_start > r_end or c_start > c_end or r_start < 0 or c_start < 0 or r_end >= input_grid.shape[0] or c_end >= input_grid.shape[1]:
        return 0 # No valid inner area

    inner_area = input_grid[r_start : r_end + 1, c_start : c_end + 1]

    color_counts = Counter()
    for r in range(inner_area.shape[0]):
        for c in range(inner_area.shape[1]):
            color = inner_area[r, c]
            if color != 0 and color != frame_color:
                color_counts[color] += 1

    if not color_counts:
        return 0 # Return 0 if no applicable colors found

    # Find the color with the maximum count.
    # If there's a tie, max() returns the first one encountered with the max value based on dict iteration order.
    # To make it deterministic (e.g., lowest color index wins tie), we could sort:
    # max_count = max(color_counts.values())
    # tied_colors = sorted([color for color, count in color_counts.items() if count == max_count])
    # most_frequent_color = tied_colors[0]
    # However, let's stick with the simpler max() for now.
    most_frequent_color = max(color_counts, key=color_counts.get)
    return most_frequent_color

def _flood_fill(output_grid, input_grid, start_coords, fill_color, inner_bounds):
    """
    Performs a 4-way flood fill on the output_grid's inner area.
    Starts from start_coords, fills only cells that are white (0) in output_grid
    AND were either white (0) OR the fill_color in the input_grid.
    Modifies the output_grid in place.

    Args:
        output_grid (np.ndarray): The grid to be filled (modified in place).
        input_grid (np.ndarray): The original input grid for checking constraints.
        start_coords (list): A list of (row, col) tuples to start the fill from.
        fill_color (int): The color to fill with.
        inner_bounds (dict): Dictionary with 'row_start', 'row_end', 'col_start', 'col_end'.
    """
    if not start_coords:
        return # No seeds to start from

    q = deque(start_coords)
    # Initialize visited with start_coords ONLY IF they are within bounds
    # (they should be by construction, but safer to check)
    r_start, r_end = inner_bounds['row_start'], inner_bounds['row_end']
    c_start, c_end = inner_bounds['col_start'], inner_bounds['col_end']
    visited = set(coord for coord in start_coords if r_start <= coord[0] <= r_end and c_start <= coord[1] <= c_end)


    while q:
        r, c = q.popleft()

        # Explore neighbours (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check boundaries (inner content area)
            if r_start <= nr <= r_end and c_start <= nc <= c_end:
                # Check if the neighbor hasn't been visited
                if (nr, nc) not in visited:
                    # Check if the neighbor is currently white (0) in the output grid
                    # AND the corresponding cell in the INPUT grid was either white(0) or the fill_color
                    if output_grid[nr, nc] == 0 and (input_grid[nr, nc] == 0 or input_grid[nr, nc] == fill_color):
                        output_grid[nr, nc] = fill_color
                        visited.add((nr, nc))
                        q.append((nr, nc))

def transform(input_grid_list):
    """
    Applies the transformation based on identifying a dominant color in the content area
    and redrawing a frame and filling the content area constrained by other colors.
    """
    input_np = np.array(input_grid_list, dtype=int)
    H, W = input_np.shape

    # 1. Get Input Dimensions (H, W)

    # 2. Identify Input Frame Color (from row index 1)
    input_frame_color = 0 # Default if grid is too small
    if H > 1 and W > 0: # Need at least 2 rows and 1 col to access [1, 0]
        input_frame_color = input_np[1, 0]

    # 3. Define Content Area boundaries (inclusive indices)
    # These are only relevant if H>=3 and W>=3
    inner_bounds = {
        'row_start': 2, 'row_end': H - 2,
        'col_start': 1, 'col_end': W - 2
    }

    # 4. & 5. Analyze inner area and determine Output Fill Color
    # Only calculate if the inner area is potentially valid (H>=3, W>=3)
    output_fill_color = 0
    if H >= 3 and W >= 3:
         output_fill_color = _find_most_frequent_inner_color(input_np, input_frame_color, inner_bounds)
    # If no dominant color found or grid too small, default is 0 (white).
    # However, the frame construction below needs *a* color. If inner area invalid,
    # perhaps output_fill_color should default to input_frame_color or another rule?
    # Let's stick to the most frequent logic for now, it defaults to 0 if empty/invalid.
    # The examples suggest a fill color is always found if H>=3, W>=3.

    # 6. Initialize Output Grid with white (0)
    output_grid = np.zeros_like(input_np)

    # 7. Copy the first row
    if H > 0:
        output_grid[0, :] = input_np[0, :]

    # Handle small grids specifically first
    if H < 3 or W < 3:
        # Simplified behavior for small grids: Copy top row, fill rest with output_fill_color.
        # Note: output_fill_color might be 0 if calculated above, which means fill with white.
        # This seems reasonable as there's no proper content area to analyze.
        if H > 1:
            # Fill rows 1 to H-1. If output_fill_color is 0, this keeps them white.
            output_grid[1:H, :] = output_fill_color
        return output_grid.tolist()

    # Proceed with standard frame/content logic for grids >= 3x3

    # 8. Construct Output Frame using output_fill_color
    if H >= 2 and W >= 2: # Redundant check given H>=3,W>=3 above, but safe
        # Fill row 1
        output_grid[1, :] = output_fill_color
        # Fill col 0 (from row 1 down)
        output_grid[1:H, 0] = output_fill_color
        # Fill col W-1 (from row 1 down)
        output_grid[1:H, W - 1] = output_fill_color
        # Fill row H-1 (between cols 1 and W-2 inclusive)
        if W > 1 : # Ensure we don't try to slice [1:0] if W=1 (though caught by W<3)
             output_grid[H - 1, 1 : W - 1] = output_fill_color

    # 9. Identify Seed Points in the input's inner area
    seed_coords = []
    r_start, r_end = inner_bounds['row_start'], inner_bounds['row_end']
    c_start, c_end = inner_bounds['col_start'], inner_bounds['col_end']
    # Iterate only if bounds are valid (which they are if H>=3, W>=3)
    for r in range(r_start, r_end + 1):
        for c in range(c_start, c_end + 1):
            if input_np[r, c] == output_fill_color:
                seed_coords.append((r, c))

    # 10. Place Seeds in the output grid (within the inner area)
    # Note: Output grid inner area is currently 0 (white)
    for r, c in seed_coords:
         # Check bounds again just in case, though seed_coords generation should be correct
        if r_start <= r <= r_end and c_start <= c <= c_end:
            output_grid[r, c] = output_fill_color

    # 11. Perform constrained flood fill on the output grid's inner area
    _flood_fill(output_grid, input_np, seed_coords, output_fill_color, inner_bounds)

    # 13. Return the completed output grid as a list of lists
    return output_grid.tolist()