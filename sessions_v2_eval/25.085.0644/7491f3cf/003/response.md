```python
import numpy as np
from collections import Counter

"""
The transformation operates on a grid divided into four zones (1-4) separated by
vertical borders, all enclosed within a main border. The zones are assumed to be
of equal width (5 pixels) and the separators are 1 pixel wide.

1. **Identify Borders and Backgrounds**:
   - Determine the grid's overall border color (most frequent color).
   - Determine the background color for Zone 2, Zone 3, and Zone 4 independently.
     The background is the most frequent color within the zone's inner area
     (excluding the main border), ignoring the border color itself.

2. **Clear Zone 4**:
   - Set all pixels within the inner area of Zone 4 (excluding the main border)
     to the background color determined for Zone 4.

3. **Copy Pattern from Zone 2 to Zone 4**:
   - Identify "pattern" pixels in Zone 2: these are pixels within the inner
     area that are neither the border color nor Zone 2's background color.
   - Copy these pattern pixels to the corresponding relative positions within
     Zone 4.

4. **Check for Zone 3 Modifier**:
   - Identify pattern pixels in Zone 3 (pixels within the inner area that are
     neither the border color nor Zone 3's background color).
   - Check if these pattern pixels meet two conditions:
     a) All pattern pixels are green (color 3).
     b) They form a single, continuous horizontal line spanning the entire
        width of Zone 3's inner area.

5. **Apply Zone 3 Modifier (if applicable)**:
   - If the conditions in step 4 are met, overlay the green horizontal line
     pattern from Zone 3 onto Zone 4 at the corresponding relative positions.
     These green pixels overwrite any pixels previously copied from Zone 2
     at the same locations.

6. **Output**:
   - The resulting grid after these operations is the output.
"""

# Define constants based on observed structure
ZONE_WIDTH = 5
ZONE_SEPARATOR_WIDTH = 1
MODIFIER_COLOR = 3  # green

# Pre-calculate zone column indices for efficiency
ZONE_COLUMNS = {
    # Zone index: list of column indices (0-based)
    1: list(range(1, 1 + ZONE_WIDTH)),
    2: list(range(1 + ZONE_WIDTH + ZONE_SEPARATOR_WIDTH, 1 + ZONE_WIDTH + ZONE_SEPARATOR_WIDTH + ZONE_WIDTH)),
    3: list(range(1 + 2 * (ZONE_WIDTH + ZONE_SEPARATOR_WIDTH), 1 + 2 * (ZONE_WIDTH + ZONE_SEPARATOR_WIDTH) + ZONE_WIDTH)),
    4: list(range(1 + 3 * (ZONE_WIDTH + ZONE_SEPARATOR_WIDTH), 1 + 3 * (ZONE_WIDTH + ZONE_SEPARATOR_WIDTH) + ZONE_WIDTH)),
}

def _get_border_color(grid):
    """Finds the most frequent color in the grid, assuming it's the border color."""
    # Ensure grid is numpy array
    grid_np = np.array(grid)
    counts = Counter(grid_np.flatten())
    # If grid is empty or has no colors, handle appropriately (e.g., return default or raise error)
    if not counts:
        # Fallback or error, depends on expected input constraints.
        # Assuming valid ARC grid, this shouldn't happen.
        # Let's default to 0 (black) if truly empty, though unlikely.
        return 0 
    return counts.most_common(1)[0][0]

def _get_zone_subgrid(grid, zone_index):
    """Extracts the inner part (excluding borders) of a specified zone."""
    grid_np = np.array(grid)
    rows, _ = grid_np.shape
    # Check if grid is too small to have an 'inner' part
    if rows <= 2:
        return np.array([[]], dtype=grid_np.dtype) # Return empty array matching dtype

    cols = ZONE_COLUMNS.get(zone_index)
    if not cols:
         raise ValueError(f"Invalid zone index: {zone_index}")
    min_col, max_col = min(cols), max(cols)

    # Ensure column indices are within grid bounds
    if max_col >= grid_np.shape[1] -1 : # Needs to be less than last col index
         # This suggests grid structure doesn't match expected zone layout
         # Handle gracefully, perhaps return empty or raise error depending on strictness
         # Let's return empty for robustness
         return np.array([[]], dtype=grid_np.dtype)


    return grid_np[1:rows-1, min_col:max_col+1]

def _get_zone_background(grid, zone_index, border_color):
    """Finds the most frequent color within a zone's inner area, excluding the border color."""
    zone_subgrid = _get_zone_subgrid(grid, zone_index)
    
    # Handle case where subgrid is empty (e.g., grid height <= 2)
    if zone_subgrid.size == 0:
        # No inner area to analyze. Return a value that won't interfere.
        # Returning border_color might be problematic if a pattern could be border_color.
        # Returning -1 might be safer to indicate 'no background'.
        # Let's reconsider: If the zone is JUST border, maybe the 'background'
        # concept doesn't apply or should default? ARC usually uses 0 (black/white)
        # as a common background. Let's default to 0 if no other color exists.
        grid_np = np.array(grid)
        if grid_np.size > 0: # If original grid wasn't empty
            unique_colors = np.unique(grid_np)
            if len(unique_colors) == 1 and unique_colors[0] == border_color:
                return border_color # The whole grid is border color
            else:
                return 0 # Default to black/white if unsure
        else:
            return 0 # Default if original grid was empty

    counts = Counter(zone_subgrid.flatten())
    
    # Remove border color count if present
    if border_color in counts:
        del counts[border_color]

    if not counts:
         # This means the zone's inner area only contained the border color (or was empty after removing border color)
         # What should be the background? Often it's 0 in ARC.
         # Let's check if 0 exists elsewhere in the subgrid *before* removing border
         original_counts = Counter(zone_subgrid.flatten())
         if 0 in original_counts:
             return 0
         else:
             # If 0 wasn't present, and only border was, this is ambiguous.
             # Maybe return the border color, assuming pattern won't match it.
             # Or stick to 0 as a general default background. Let's stick to 0.
             return 0
             # Alternative: return border_color

    # Return the most frequent *remaining* color
    return counts.most_common(1)[0][0]


def _get_pattern_pixels(grid, zone_index, bg_color, border_color):
    """Finds relative coordinates (within zone) and colors of pattern pixels."""
    pattern_pixels = []
    grid_np = np.array(grid)
    rows, cols_total = grid_np.shape
    zone_cols = ZONE_COLUMNS.get(zone_index)

    if not zone_cols or rows <= 2: # No zone or no inner rows
        return []

    min_col, max_col = min(zone_cols), max(zone_cols)

    # Check bounds to prevent errors
    if max_col >= cols_total -1:
        return [] # Zone definition exceeds grid boundary

    for r in range(1, rows - 1):
        for c_abs in range(min_col, max_col + 1):
            color = grid_np[r, c_abs]
            if color != bg_color and color != border_color:
                # Store relative coordinates (r_rel, c_rel) and color
                r_rel = r - 1 # Relative row index within the inner area
                c_rel = c_abs - min_col # Relative col index within the inner area
                pattern_pixels.append(((r_rel, c_rel), color))
    return pattern_pixels

def _is_horizontal_line(pattern_pixels, zone_index, grid_shape):
    """Checks if pattern pixels form a single horizontal green line across the zone."""
    if not pattern_pixels:
        return False

    inner_height = grid_shape[0] - 2
    inner_width = ZONE_WIDTH # Expected width of the inner zone area

    if inner_height <= 0 or inner_width <= 0:
        return False # Not a valid inner area

    first_rel_row = pattern_pixels[0][0][0]
    pixel_rel_cols = set()

    for (r_rel, c_rel), color in pattern_pixels:
        # Check row consistency
        if r_rel != first_rel_row:
            return False # Must all be on the same relative row
        # Check color
        if color != MODIFIER_COLOR: # Must all be the modifier color (green)
            return False
        # Check relative column is within expected zone width
        if not (0 <= c_rel < inner_width):
             return False # Outside zone bounds
        pixel_rel_cols.add(c_rel)

    # Check if all relative columns (0 to inner_width-1) are present exactly once
    return len(pixel_rel_cols) == inner_width


def transform(input_grid):
    """
    Applies the transformation rule: clears Zone 4, copies Zone 2 pattern,
    and potentially overlays Zone 3's green line pattern.
    """
    grid_np = np.array(input_grid)
    output_grid = np.copy(grid_np)
    rows, cols = grid_np.shape

    # --- 1. Identify Borders and Backgrounds ---
    border_color = _get_border_color(grid_np)
    # Need backgrounds for Z2, Z3 (pattern detection) and Z4 (clearing)
    bg_z2 = _get_zone_background(grid_np, 2, border_color)
    bg_z3 = _get_zone_background(grid_np, 3, border_color)
    bg_z4 = _get_zone_background(grid_np, 4, border_color)

    # --- 2. Clear Zone 4 ---
    zone4_cols = ZONE_COLUMNS.get(4)
    if zone4_cols and rows > 2: # Check if zone exists and has inner area
        min_col4, max_col4 = min(zone4_cols), max(zone4_cols)
        # Ensure indices are within actual grid bounds before slicing
        if max_col4 < cols -1:
             for r in range(1, rows - 1):
                 for c in range(min_col4, max_col4 + 1):
                     # Only clear if it's not already the background OR if we need to ensure it IS bg_z4
                     # Safest is just to set it regardless
                     output_grid[r, c] = bg_z4

    # --- 3. Copy Pattern from Zone 2 to Zone 4 ---
    z2_pattern_pixels = _get_pattern_pixels(grid_np, 2, bg_z2, border_color)
    zone2_cols = ZONE_COLUMNS.get(2)

    if zone2_cols and zone4_cols: # Check both zones exist
        min_col2 = min(zone2_cols)
        min_col4 = min(zone4_cols)
        col_offset = min_col4 - min_col2

        for (r_rel, c_rel), color in z2_pattern_pixels:
            # Calculate absolute target coordinates
            r_abs_tgt = r_rel + 1
            c_abs_tgt = c_rel + min_col4 # Apply offset relative to Z4 start

            # Check bounds before writing
            if 1 <= r_abs_tgt < rows - 1 and min_col4 <= c_abs_tgt <= max(zone4_cols):
                 output_grid[r_abs_tgt, c_abs_tgt] = color

    # --- 4. Check for Zone 3 Modifier ---
    z3_pattern_pixels = _get_pattern_pixels(grid_np, 3, bg_z3, border_color)
    is_modifier = _is_horizontal_line(z3_pattern_pixels, 3, grid_np.shape)

    # --- 5. Apply Zone 3 Modifier (if applicable) ---
    if is_modifier:
        zone3_cols = ZONE_COLUMNS.get(3)
        if zone3_cols and zone4_cols: # Check both zones exist
            min_col3 = min(zone3_cols)
            min_col4 = min(zone4_cols)
            # No need for col_offset calculation here, relative coords are sufficient

            for (r_rel, c_rel), color in z3_pattern_pixels: # Color must be MODIFIER_COLOR
                # Calculate absolute target coordinates
                r_abs_tgt = r_rel + 1
                c_abs_tgt = c_rel + min_col4 # Apply offset relative to Z4 start

                # Check bounds before writing
                if 1 <= r_abs_tgt < rows - 1 and min_col4 <= c_abs_tgt <= max(zone4_cols):
                    output_grid[r_abs_tgt, c_abs_tgt] = color # Overlay green pixel

    # --- 6. Output ---
    return output_grid.tolist() # Return as list of lists
```