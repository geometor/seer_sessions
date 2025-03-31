import numpy as np
from collections import Counter

"""
The transformation operates on a grid divided into four zones (1-4) separated by
vertical borders, all enclosed within a main border. The zones are assumed to be
of equal width (5 pixels inner content) and the separators are 1 pixel wide.

The core logic is to generate the content of Zone 4 based on the contents of Zone 2 and Zone 3.

1.  **Initialization:** Create a copy of the input grid to serve as the output grid.
2.  **Identify Structure:**
    *   Determine the `border_color` from the top-left pixel.
    *   Define the inner column ranges for each of the four zones based on a fixed `ZONE_WIDTH` (5) and `ZONE_SEPARATOR_WIDTH` (1).
3.  **Analyze Zone 2:**
    *   Determine the `background_color_z2` by finding the most frequent color within the inner area of Zone 2, excluding the `border_color`. Default to 0 (white) if only border color or nothing else is found.
    *   Identify `pattern_pixels_z2` within the inner area of Zone 2: find all pixels whose color is neither `background_color_z2` nor `border_color`. Record their relative coordinates (row, col within the zone's inner area) and colors.
4.  **Analyze Zone 3:**
    *   Determine the `background_color_z3` similarly for Zone 3.
    *   Identify `pattern_pixels_z3` similarly for Zone 3, using `background_color_z3`.
5.  **Prepare Zone 4 Canvas:**
    *   Fill the inner area of Zone 4 in the `output_grid` with `background_color_z2`.
6.  **Copy Zone 2 Pattern:**
    *   Copy the `pattern_pixels_z2` to the corresponding relative positions within Zone 4's inner area in the `output_grid`.
7.  **Check for and Apply Zone 3 Influence:**
    *   **Check for Modifier:** Search within Zone 3's inner area for a single, continuous horizontal line composed entirely of green (3) pixels that spans the full `ZONE_WIDTH`.
    *   **Apply Modifier:** If such a green line (`modifier_line_pixels`) is found:
        *   Overlay these `modifier_line_pixels` onto the corresponding relative positions within Zone 4's inner area in the `output_grid`.
    *   **Apply Full Pattern:** If no such green line modifier is found:
        *   Overlay *all* `pattern_pixels_z3` onto the corresponding relative positions within Zone 4's inner area in the `output_grid`.
8.  **Output:** Return the modified `output_grid`.
"""

# Define constants based on observed structure
ZONE_WIDTH = 5
ZONE_SEPARATOR_WIDTH = 1
MODIFIER_COLOR = 3  # green

# Pre-calculate zone column indices for efficiency (inner content columns)
# Assumes border is col 0, separator is between zones
# Adjusting calculation slightly for clarity and robustness
def _calculate_zone_inner_columns(zone_index):
    """ Calculates the inner column indices for a given zone index (1-based)."""
    if not 1 <= zone_index <= 4:
        return []
    start_col_zone = 1 + (zone_index - 1) * (ZONE_WIDTH + ZONE_SEPARATOR_WIDTH)
    end_col_zone = start_col_zone + ZONE_WIDTH -1 # Inclusive end column
    return list(range(start_col_zone, end_col_zone + 1))

ZONE_INNER_COLUMNS = { i: _calculate_zone_inner_columns(i) for i in range(1, 5) }


def _get_border_color(grid_np):
    """Gets the border color, assumed to be the top-left pixel."""
    if grid_np.size == 0:
        return 0 # Default for empty grid
    return grid_np[0, 0]

def _get_zone_subgrid(grid_np, zone_index):
    """Extracts the inner content part (excluding outer borders) of a specified zone."""
    rows, cols_total = grid_np.shape
    # Inner rows are from 1 to rows-2 (0-based index)
    if rows <= 2:
        return np.array([[]], dtype=grid_np.dtype) # No inner rows

    cols = ZONE_INNER_COLUMNS.get(zone_index)
    if not cols:
         # This should not happen if zone_index is 1-4 due to precalculation
         # but good to have a safeguard.
         print(f"Warning: Could not find columns for zone {zone_index}")
         return np.array([[]], dtype=grid_np.dtype)

    min_col, max_col = min(cols), max(cols)

    # Ensure column indices are within the grid's boundaries (specifically, less than the last column index)
    # Need to check against cols_total - 1 because max_col is an index
    if min_col >= cols_total -1 or max_col >= cols_total - 1:
         # This suggests grid structure doesn't match expected zone layout or is too narrow
         print(f"Warning: Zone {zone_index} columns ({min_col}-{max_col}) exceed grid width ({cols_total}).")
         return np.array([[]], dtype=grid_np.dtype) # Return empty

    # Extract inner rows [1:rows-1] and the calculated inner columns for the zone
    return grid_np[1:rows-1, min_col:max_col+1]

def _get_zone_background(grid_np, zone_index, border_color):
    """
    Finds the most frequent color within a zone's inner area,
    excluding the border color. Defaults to 0 if only border color or nothing is found.
    """
    zone_subgrid = _get_zone_subgrid(grid_np, zone_index)

    if zone_subgrid.size == 0:
        return 0 # Default background for empty or invalid zone subgrid

    counts = Counter(zone_subgrid.flatten())

    # Remove border color count if present
    if border_color in counts:
        del counts[border_color]

    if not counts:
         # This means the zone's inner area only contained the border color (or was empty after removing border color)
         # Default to 0 (white)
         return 0
    else:
        # Return the most frequent *remaining* color
        return counts.most_common(1)[0][0]


def _get_pattern_pixels(grid_np, zone_index, bg_color, border_color):
    """
    Finds relative coordinates (within zone's inner area) and colors
    of pattern pixels (pixels that are neither background nor border).
    Returns a list of tuples: [((rel_row, rel_col), color), ...].
    """
    pattern_pixels = []
    rows, cols_total = grid_np.shape
    zone_inner_cols = ZONE_INNER_COLUMNS.get(zone_index)

    if not zone_inner_cols or rows <= 2: # No zone or no inner rows
        return []

    min_col_inner, max_col_inner = min(zone_inner_cols), max(zone_inner_cols)

    # Check bounds to prevent errors with column indexing
    if max_col_inner >= cols_total -1:
        return [] # Zone definition exceeds grid boundary

    # Iterate through the *inner* rows (absolute indices 1 to rows-2)
    # and the zone's specific *inner* columns (absolute indices)
    for r_abs in range(1, rows - 1):
        for c_abs in range(min_col_inner, max_col_inner + 1):
            color = grid_np[r_abs, c_abs]
            if color != bg_color and color != border_color:
                # Store relative coordinates (r_rel, c_rel) and color
                # r_rel is relative to the top inner row (row 1), so r_rel = r_abs - 1
                # c_rel is relative to the leftmost inner column of the zone, so c_rel = c_abs - min_col_inner
                r_rel = r_abs - 1
                c_rel = c_abs - min_col_inner
                pattern_pixels.append(((r_rel, c_rel), color))
    return pattern_pixels

def _find_horizontal_modifier_line(grid_np, zone_index, border_color):
    """
    Checks Zone 3's inner area for a horizontal line of MODIFIER_COLOR (green)
    spanning the full ZONE_WIDTH.
    Returns a list of the pixels ((rel_row, rel_col), color) forming the first such line found,
    or an empty list if no such line exists.
    """
    modifier_line_pixels = []
    rows, cols_total = grid_np.shape
    zone_inner_cols = ZONE_INNER_COLUMNS.get(zone_index)

    if not zone_inner_cols or rows <= 2 or ZONE_WIDTH <= 0:
        return [] # Cannot form a line

    min_col_inner, max_col_inner = min(zone_inner_cols), max(zone_inner_cols)

    # Check bounds
    if max_col_inner >= cols_total - 1:
        return []

    inner_rows_count = rows - 2 # Number of inner rows (e.g., if rows=7, inner rows are 1,2,3,4,5 -> 5 rows)

    # Iterate through each potential *inner* row (absolute index)
    for r_abs in range(1, rows - 1):
        current_row_pixels = []
        is_potential_modifier_line = True
        
        # Check all columns within the zone's inner width for this row
        for c_abs in range(min_col_inner, max_col_inner + 1):
            color = grid_np[r_abs, c_abs]
            if color == MODIFIER_COLOR:
                # Calculate relative coordinates for storage if line is confirmed
                r_rel = r_abs - 1
                c_rel = c_abs - min_col_inner
                current_row_pixels.append(((r_rel, c_rel), color))
            else:
                # If any pixel in the row within the zone is not the modifier color,
                # this row cannot be the modifier line.
                is_potential_modifier_line = False
                break # No need to check rest of this row

        # After checking all columns in the zone for this row:
        # Was it a potential line and did it span the full expected width?
        if is_potential_modifier_line and len(current_row_pixels) == ZONE_WIDTH:
            # Found the modifier line! Return its pixels.
            return current_row_pixels

    # If we looped through all rows and didn't find a full-width green line
    return []


def transform(input_grid):
    # --- 1. Initialization ---
    try:
        grid_np = np.array(input_grid, dtype=np.int64)
        output_grid = np.copy(grid_np)
        rows, cols = grid_np.shape
    except Exception as e:
        print(f"Error converting input to numpy array: {e}")
        # Return input as is if conversion fails
        return input_grid

    # --- 2. Identify Structure ---
    # Basic check for minimum grid size needed for borders and at least one zone block
    min_expected_cols = 1 + ZONE_WIDTH + 1 # Border, Zone1, Separator
    if rows <= 2 or cols < min_expected_cols:
        # Grid is too small for even minimal structure
        print("Warning: Grid dimensions too small for expected structure.")
        return output_grid.tolist()

    border_color = _get_border_color(grid_np)

    # --- 3. Analyze Zone 2 ---
    bg_z2 = _get_zone_background(grid_np, 2, border_color)
    z2_pattern_pixels = _get_pattern_pixels(grid_np, 2, bg_z2, border_color)

    # --- 4. Analyze Zone 3 ---
    bg_z3 = _get_zone_background(grid_np, 3, border_color)
    z3_pattern_pixels = _get_pattern_pixels(grid_np, 3, bg_z3, border_color) # Used if modifier not found

    # --- 5. Prepare Zone 4 Canvas ---
    zone4_inner_cols = ZONE_INNER_COLUMNS.get(4)
    if not zone4_inner_cols:
        print("Error: Could not determine Zone 4 columns. Structure likely invalid.")
        # Return copy as Zone 4 cannot be processed
        return output_grid.tolist()

    min_col4_inner, max_col4_inner = min(zone4_inner_cols), max(zone4_inner_cols)

    # Check bounds before clearing Zone 4
    if 1 <= rows - 2 and min_col4_inner <= max_col4_inner < cols - 1:
        # Fill the inner area of Zone 4 with the background color from Zone 2
        output_grid[1:rows-1, min_col4_inner:max_col4_inner+1] = bg_z2
    else:
        # If bounds are invalid, Zone 4 probably doesn't exist as expected
        print("Warning: Zone 4 inner area calculation out of bounds. Cannot clear.")
        # Proceed, but Zone 4 might not be cleared or drawn correctly

    # --- 6. Copy Zone 2 Pattern to Zone 4 ---
    if 1 <= rows - 2 and min_col4_inner <= max_col4_inner < cols - 1: # Check bounds again before drawing
        for (r_rel, c_rel), color in z2_pattern_pixels:
            # Calculate absolute target coordinates in Zone 4's inner area
            r_abs_tgt = r_rel + 1 # Add 1 for top border offset
            c_abs_tgt = c_rel + min_col4_inner # Add Z4 inner start column offset

            # Ensure target coordinates are within the valid drawing area of Zone 4
            if 1 <= r_abs_tgt < rows - 1 and min_col4_inner <= c_abs_tgt <= max_col4_inner:
                 output_grid[r_abs_tgt, c_abs_tgt] = color
            # else: Pixel from Z2 maps outside Z4 bounds - ignore


    # --- 7. Check for and Apply Zone 3 Influence ---
    modifier_line_pixels = _find_horizontal_modifier_line(grid_np, 3, border_color)

    pixels_to_apply_from_z3 = []
    if modifier_line_pixels:
        # Modifier found - use only the green line pixels
        pixels_to_apply_from_z3 = modifier_line_pixels
        # print(f"Debug: Modifier line found with {len(pixels_to_apply_from_z3)} pixels.")
    else:
        # No modifier found - use all pattern pixels from Zone 3
        pixels_to_apply_from_z3 = z3_pattern_pixels
        # print(f"Debug: No modifier line found. Using {len(pixels_to_apply_from_z3)} pattern pixels from Z3.")

    # Apply the selected pixels (either modifier line or full Z3 pattern) onto Zone 4
    if 1 <= rows - 2 and min_col4_inner <= max_col4_inner < cols - 1: # Check bounds again
        for (r_rel, c_rel), color in pixels_to_apply_from_z3:
            # Calculate absolute target coordinates in Zone 4's inner area
            r_abs_tgt = r_rel + 1
            c_abs_tgt = c_rel + min_col4_inner

            # Ensure target coordinates are within the valid drawing area of Zone 4
            if 1 <= r_abs_tgt < rows - 1 and min_col4_inner <= c_abs_tgt <= max_col4_inner:
                output_grid[r_abs_tgt, c_abs_tgt] = color # Overlay the pixel
            # else: Pixel from Z3 maps outside Z4 bounds - ignore


    # --- 8. Output ---
    return output_grid.tolist() # Return as list of lists
