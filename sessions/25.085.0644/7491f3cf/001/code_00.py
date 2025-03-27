"""
The transformation identifies four zones within a bordered grid. It copies the pattern
(non-background, non-border pixels) from either Zone 2 or Zone 3 into Zone 4,
overwriting Zone 4's original pattern but preserving its background.

The source zone selection logic is:
1. If Zone 3 contains any non-background pattern pixel that is NOT green (3),
   Zone 3 is the source.
2. Otherwise, Zone 2 is the primary source.
3. If Zone 2 is the source AND Zone 3's pattern consists solely of green (3) pixels
   forming a single horizontal line spanning the zone's width, then Zone 3 acts as
   a modifier, and its green pattern is overlaid onto Zone 4 after copying
   Zone 2's pattern.
"""

import numpy as np
from collections import Counter

# Define constants
ZONE_WIDTH = 5
ZONE_SEPARATOR_WIDTH = 1
NUM_ZONES = 4
MODIFIER_COLOR = 3  # green

ZONE_COLUMNS = {
    1: list(range(1, 1 + ZONE_WIDTH)),
    2: list(range(1 + ZONE_WIDTH + ZONE_SEPARATOR_WIDTH, 1 + ZONE_WIDTH + ZONE_SEPARATOR_WIDTH + ZONE_WIDTH)),
    3: list(range(1 + 2 * (ZONE_WIDTH + ZONE_SEPARATOR_WIDTH), 1 + 2 * (ZONE_WIDTH + ZONE_SEPARATOR_WIDTH) + ZONE_WIDTH)),
    4: list(range(1 + 3 * (ZONE_WIDTH + ZONE_SEPARATOR_WIDTH), 1 + 3 * (ZONE_WIDTH + ZONE_SEPARATOR_WIDTH) + ZONE_WIDTH)),
}

def _get_border_color(grid):
    """Finds the most frequent color in the grid, assuming it's the border color."""
    counts = Counter(grid.flatten())
    return counts.most_common(1)[0][0]

def _get_zone_subgrid(grid, zone_index):
    """Extracts the inner part (excluding borders) of a specified zone."""
    rows, _ = grid.shape
    cols = ZONE_COLUMNS[zone_index]
    return grid[1:rows-1, min(cols):max(cols)+1]

def _get_zone_background(grid, zone_index, border_color):
    """Finds the most frequent color within a zone, excluding the border color."""
    zone_subgrid = _get_zone_subgrid(grid, zone_index)
    if zone_subgrid.size == 0:
        # Handle empty inner zone case, maybe default? Or assume valid input.
        # Let's assume valid input means non-empty inner zones for Z2/Z3/Z4
        # If the zone only contains border color, there's no distinct background.
        # This might need adjustment based on edge cases.
        # For now, return a value unlikely to be a pattern, like border_color itself
        # or -1 if we need to signal this. Let's return border_color for now.
         unique_colors = np.unique(zone_subgrid)
         if len(unique_colors) == 1 and unique_colors[0] == border_color:
             # If the zone *only* has border color, this is tricky.
             # Let's return the border color, assuming patterns won't match it.
             return border_color
         elif len(unique_colors) == 0:
             # Empty subgrid? Shouldn't happen with ARC constraints (min 1x1)
             # but being safe.
             return border_color # or raise error


    counts = Counter(zone_subgrid.flatten())
    # Remove border color count if present
    if border_color in counts:
        del counts[border_color]
    
    if not counts:
         # This means the zone only contained the border color
         # Return the border color itself, assuming patterns won't match it.
         return border_color

    # Return the most frequent remaining color
    return counts.most_common(1)[0][0]


def _get_pattern_pixels(grid, zone_index, bg_color, border_color):
    """Finds coordinates and colors of pattern pixels in a zone."""
    pattern_pixels = []
    rows, _ = grid.shape
    cols = ZONE_COLUMNS[zone_index]
    min_col, max_col = min(cols), max(cols)

    for r in range(1, rows - 1):
        for c in range(min_col, max_col + 1):
            color = grid[r, c]
            if color != bg_color and color != border_color:
                pattern_pixels.append(((r, c), color))
    return pattern_pixels

def _is_horizontal_line(pattern_pixels, zone_index):
    """Checks if pattern pixels form a single horizontal line across the zone."""
    if not pattern_pixels:
        return False

    cols = ZONE_COLUMNS[zone_index]
    min_col, max_col = min(cols), max(cols)
    expected_width = max_col - min_col + 1 # Should be ZONE_WIDTH

    first_row = pattern_pixels[0][0][0]
    pixel_cols = set()

    for (r, c), color in pattern_pixels:
        if r != first_row: # Must all be on the same row
            return False
        if color != MODIFIER_COLOR: # Must all be the modifier color (green)
            return False
        if not (min_col <= c <= max_col): # Must be within zone columns
             return False
        pixel_cols.add(c)

    # Check if all columns in the zone range are present exactly once
    return len(pixel_cols) == expected_width and min(pixel_cols) == min_col and max(pixel_cols) == max_col


def transform(input_grid):
    """
    Applies the transformation rule based on zone analysis and copying/modifying Zone 4.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify border color
    border_color = _get_border_color(input_grid)

    # 2. Get background colors for relevant zones
    bg_z2 = _get_zone_background(input_grid, 2, border_color)
    bg_z3 = _get_zone_background(input_grid, 3, border_color)
    # bg_z4 is not explicitly needed for the logic, but good for clarity if copying
    # bg_z4 = _get_zone_background(input_grid, 4, border_color) # We preserve Z4 bg

    # 3. Analyze Zone 3 to determine source and modifier
    source_zone_index = 2 # Default source
    modifier_zone_index = None # Default no modifier

    z3_pattern_pixels = _get_pattern_pixels(input_grid, 3, bg_z3, border_color)

    has_non_green_pattern_z3 = any(color != MODIFIER_COLOR for _, color in z3_pattern_pixels)

    if has_non_green_pattern_z3:
        source_zone_index = 3
        modifier_zone_index = None
    else:
        # All pattern pixels in Z3 (if any) are green
        if _is_horizontal_line(z3_pattern_pixels, 3):
            source_zone_index = 2
            modifier_zone_index = 3
        else:
            source_zone_index = 2
            modifier_zone_index = None

    # 4. Perform the copy operation
    source_cols = ZONE_COLUMNS[source_zone_index]
    target_cols = ZONE_COLUMNS[4]
    col_offset = min(target_cols) - min(source_cols)
    source_bg = bg_z2 if source_zone_index == 2 else bg_z3

    source_pattern_pixels = _get_pattern_pixels(input_grid, source_zone_index, source_bg, border_color)

    for (r, c_src), color in source_pattern_pixels:
        c_tgt = c_src + col_offset
        # Ensure target is within bounds (should be by logic, but safety)
        if 1 <= r < rows - 1 and min(target_cols) <= c_tgt <= max(target_cols):
             # Check if target pixel is NOT part of the original Z4 background
             # Actually, the rule seems to be overwrite regardless, preserving only Z4 bg *implicitly*
             # by only copying non-bg pixels from source. Let's stick to that.
             output_grid[r, c_tgt] = color


    # 5. Perform the modification operation (if applicable)
    if modifier_zone_index == 3:
        modifier_cols = ZONE_COLUMNS[modifier_zone_index]
        target_cols = ZONE_COLUMNS[4] # Target is still Zone 4
        col_offset_mod = min(target_cols) - min(modifier_cols)
        modifier_bg = bg_z3 # Modifier is Zone 3

        # We already have z3_pattern_pixels
        # modifier_pattern_pixels = _get_pattern_pixels(input_grid, modifier_zone_index, modifier_bg, border_color)

        for (r, c_mod), color in z3_pattern_pixels: # Use the already computed Z3 pattern
             c_tgt = c_mod + col_offset_mod
             # Ensure target is within bounds
             if 1 <= r < rows - 1 and min(target_cols) <= c_tgt <= max(target_cols):
                  # Overwrite with the modifier color (which must be green)
                  output_grid[r, c_tgt] = color # color here must be MODIFIER_COLOR

    # Return the modified grid
    return output_grid