import numpy as np
from collections import Counter, deque

"""
Transforms the input grid by finding specific 3x3 patterns ("stamps") and using them to "paint" adjacent areas that are either the background color or the same color as the stamp's center.

1.  **Analyze Input:**
    *   Determine the background color (C_bg) by finding the most frequent color in the input grid.

2.  **Find Stamps:**
    *   Scan the input grid for 3x3 subgrids.
    *   A valid "stamp" is a 3x3 subgrid with:
        *   A uniform border color (C_frame).
        *   A single center pixel color (C_center).
        *   The border color C_frame must *not* be the background color C_bg.
    *   Store each found stamp's 3x3 grid, its center color (C_center), and its top-left position (r_stamp, c_stamp).

3.  **Identify Target Pixels for Each Stamp:**
    *   Initialize the output grid as a copy of the input grid.
    *   Keep track of pixels that have been modified using a set `modified_pixels`.
    *   For each identified stamp S located at (r_stamp, c_stamp) with center color C_center:
        *   Define the 3x3 bounding box coordinates of the stamp: `stamp_coords = {(r, c) for r in range(r_stamp, r_stamp+3) for c in range(c_stamp, c_stamp+3)}`.
        *   Find all adjacent pixel coordinates (8-connectivity, including diagonals) to any pixel within `stamp_coords`.
        *   Filter these adjacent coordinates to find the `target_pixels` for this stamp:
            *   A pixel (r, c) is a target if it's adjacent to the stamp AND its color in the *input* grid is either the background color (C_bg) OR the stamp's center color (C_center).

4.  **Apply Stamp Pattern (Tiling):**
    *   For each stamp S and its corresponding `target_pixels`:
        *   Iterate through each target pixel coordinate (r, c) in `target_pixels`.
        *   Check if (r, c) is already in the `modified_pixels` set. If yes, skip to the next target pixel (first modification wins).
        *   Calculate the corresponding indices within the stamp's 3x3 grid using modulo arithmetic relative to the *stamp's* top-left corner:
            *   `stamp_r_idx = (r - r_stamp) % 3`
            *   `stamp_c_idx = (c - c_stamp) % 3`
        *   Update the `output_grid` at position (r, c) with the color from the stamp's grid: `output_grid[r, c] = stamp_grid[stamp_r_idx, stamp_c_idx]`.
        *   Add the coordinate (r, c) to the `modified_pixels` set.

5.  **Finalize:**
    *   Return the `output_grid`. Pixels that were not target pixels for any stamp remain unchanged from their original input color.
"""

def find_background_color(grid):
    """Finds the most frequent color in the grid."""
    counts = Counter(grid.flatten())
    # Handle empty grid or single color case
    if not counts:
        return 0 # Default to black/white if grid is empty
    # If multiple colors have the same max count, the specific choice might matter,
    # but usually, the background is overwhelmingly dominant. np.unique handles ties arbitrarily.
    colors, freqs = np.unique(grid, return_counts=True)
    return colors[np.argmax(freqs)]

def find_stamps(grid, background_color):
    """
    Finds 3x3 stamp patterns with a uniform border color different from the background
    and a single center color.
    """
    stamps_info = []
    height, width = grid.shape
    for r in range(height - 2):
        for c in range(width - 2):
            subgrid = grid[r:r+3, c:c+3]

            # Check for uniform border
            frame_color = subgrid[0, 0]
            is_uniform_border = True
            # Check top and bottom rows
            if not (np.all(subgrid[0, :] == frame_color) and np.all(subgrid[2, :] == frame_color)):
                is_uniform_border = False
            # Check middle row sides
            if not (subgrid[1, 0] == frame_color and subgrid[1, 2] == frame_color):
                is_uniform_border = False

            if is_uniform_border:
                # Check if frame color is not the background color
                if frame_color != background_color:
                    center_color = subgrid[1, 1]
                    stamps_info.append({
                        'grid': subgrid.copy(),
                        'frame_color': frame_color,
                        'center_color': center_color,
                        'row': r,
                        'col': c
                    })
    return stamps_info

def get_adjacent_pixels(grid_shape, coords_set):
    """
    Finds all unique pixels adjacent (8-connectivity) to any pixel in coords_set,
    excluding pixels within coords_set itself.
    """
    height, width = grid_shape
    adjacent = set()
    for r_orig, c_orig in coords_set:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r_orig + dr, c_orig + dc
                # Check bounds
                if 0 <= nr < height and 0 <= nc < width:
                    neighbor_coord = (nr, nc)
                    # Add if not part of the original set
                    if neighbor_coord not in coords_set:
                        adjacent.add(neighbor_coord)
    return adjacent


def transform(input_grid):
    """
    Applies the stamp tiling transformation based on adjacency and color rules.
    """
    height, width = input_grid.shape

    # 1. Analyze Input: Find background color
    background_color = find_background_color(input_grid)

    # 2. Find Stamps: Identify relevant 3x3 patterns
    stamps = find_stamps(input_grid, background_color)

    # Initialize output grid and track modified pixels
    output_grid = np.copy(input_grid)
    modified_pixels = set()

    # 3 & 4. Identify Targets & Apply Tiling for each stamp
    for stamp in stamps:
        stamp_grid = stamp['grid']
        stamp_center_color = stamp['center_color']
        r_stamp, c_stamp = stamp['row'], stamp['col']

        # Define the stamp's own coordinates
        stamp_coords = set()
        for r_offset in range(3):
            for c_offset in range(3):
                 # Ensure stamp coords are within grid bounds (redundant check if find_stamps is correct)
                 curr_r, curr_c = r_stamp + r_offset, c_stamp + c_offset
                 if 0 <= curr_r < height and 0 <= curr_c < width:
                    stamp_coords.add((curr_r, curr_c))


        # Find pixels adjacent to the stamp
        pixels_near_stamp = get_adjacent_pixels((height, width), stamp_coords)

        # Filter adjacent pixels to find target pixels
        target_pixels = set()
        for r, c in pixels_near_stamp:
             pixel_color = input_grid[r, c]
             # Check color condition: pixel is background OR matches stamp center
             if pixel_color == background_color or pixel_color == stamp_center_color:
                 target_pixels.add((r,c))

        # Apply tiling to target pixels
        for r, c in target_pixels:
            # Apply modification only if pixel hasn't been modified yet
            if (r, c) not in modified_pixels:
                # Calculate stamp indices using modulo relative to stamp's top-left
                stamp_r_idx = (r - r_stamp) % 3
                stamp_c_idx = (c - c_stamp) % 3

                # Update the output grid
                output_grid[r, c] = stamp_grid[stamp_r_idx, stamp_c_idx]
                modified_pixels.add((r, c)) # Mark pixel as modified

    # 5. Finalize
    return output_grid