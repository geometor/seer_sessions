import numpy as np
from collections import Counter

"""
Transforms an input grid by drawing a line or path based on the relationship between two identified non-background elements: a 'marker pixel' and a 'reference structure'.

1.  **Identify Background:** Determine the background color (most frequent).
2.  **Identify Objects:**
    *   Find all non-background pixels.
    *   Identify the 'Marker Pixel':
        *   If one color appears exactly once, its pixel is the marker.
        *   If all non-background pixels share the same color, the marker is the one with the maximum row index, and among those, the maximum column index.
    *   Identify the 'Reference Structure': All non-background pixels that are not the marker pixel.
    *   Determine the orientation of the Reference Structure (Vertical, Horizontal, or Diagonal) and collect the set of unique rows and columns it occupies.
3.  **Prepare Output:** Create a copy of the input grid.
4.  **Execute Drawing Rule based on Reference Structure Orientation:**
    *   **Vertical Reference:** Draw a horizontal line using the marker's color, in the marker's row, extending between the column immediately after the reference structure's column and the marker's column (inclusive).
    *   **Horizontal Reference:** Draw a vertical line using the marker's color, in the marker's column, extending between the row immediately after the reference structure's row and the marker's row (inclusive).
    *   **Diagonal Reference:** Draw a diagonal path using the marker's color.
        *   Determine the diagonal step direction (dr, dc) from the marker towards the reference structure's center.
        *   Start the path one step (dr, dc) away from the marker.
        *   Continue stepping in the (dr, dc) direction, drawing pixels, until a point (r, c) is reached where either r is a row occupied by the reference structure OR c is a column occupied by the reference structure. Draw this final point and stop.
5.  **Return Output:** Return the modified grid.
"""

def find_objects(grid):
    """
    Identifies the background color, marker pixel, reference structure pixels,
    reference structure orientation, and occupied rows/columns in the grid.
    """
    rows, cols = grid.shape
    flat_grid = grid.flatten()
    
    # Handle edge case of empty or single-color grid
    if len(np.unique(flat_grid)) <= 1:
        # If all same color, consider it background, no objects
        return grid[0,0] if grid.size > 0 else 0, None, [], None, set(), set()

    background_color = Counter(flat_grid).most_common(1)[0][0]

    non_background_pixels = {} # {(r, c): color}
    pixel_counts_by_color = Counter()

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != background_color:
                non_background_pixels[(r, c)] = color
                pixel_counts_by_color[color] += 1

    if not non_background_pixels:
         return background_color, None, [], None, set(), set()

    marker_pixel = None # ((r, c), color)
    marker_pos = None
    marker_color = -1

    # Strategy 1: Find a color with count 1
    unique_color = -1
    for color, count in pixel_counts_by_color.items():
        if count == 1:
            unique_color = color
            break

    if unique_color != -1:
        for pos, c in non_background_pixels.items():
            if c == unique_color:
                marker_pos = pos
                marker_color = c
                marker_pixel = (pos, c)
                break
    # Strategy 2: All non-background pixels have the same color
    elif len(pixel_counts_by_color) == 1:
        # Find the pixel with the max row, then max col
        marker_pos = max(non_background_pixels.keys(), key=lambda p: (p[0], p[1]))
        marker_color = non_background_pixels[marker_pos]
        marker_pixel = (marker_pos, marker_color)
    else:
         # Ambiguous case - more than one color, none unique.
         # This case is not covered by the examples provided.
         # Defaulting to max row/col strategy for now.
         print("Warning: Ambiguous marker identification. Defaulting to max row/col.")
         marker_pos = max(non_background_pixels.keys(), key=lambda p: (p[0], p[1]))
         marker_color = non_background_pixels[marker_pos]
         marker_pixel = (marker_pos, marker_color)


    # Identify reference pixels
    reference_pixels = [] # list of (r, c, color)
    ref_rows_set = set()
    ref_cols_set = set()
    for pos, color in non_background_pixels.items():
        if pos != marker_pos:
            r, c = pos
            reference_pixels.append((r, c, color))
            ref_rows_set.add(r)
            ref_cols_set.add(c)

    # Determine reference structure orientation
    orientation = None
    if reference_pixels:
        # Use the sets collected earlier
        ref_rows = ref_rows_set
        ref_cols = ref_cols_set

        if len(ref_cols) == 1 and len(ref_rows) > 0: # Need > 0 check in case ref is empty somehow
            orientation = "Vertical"
        elif len(ref_rows) == 1 and len(ref_cols) > 0:
            orientation = "Horizontal"
        elif len(ref_rows) > 1 and len(ref_cols) > 1:
            # Check for diagonal - assumes pure diagonal based on examples
            is_diag = True
            sorted_ref = sorted(reference_pixels, key=lambda x: (x[0], x[1]))
            if len(sorted_ref) > 1:
                 dr = sorted_ref[1][0] - sorted_ref[0][0]
                 dc = sorted_ref[1][1] - sorted_ref[0][1]
                 # Check if step is diagonal (abs(dr)==abs(dc) and both non-zero)
                 if not (abs(dr) == abs(dc) and dr != 0):
                     is_diag = False
                 else:
                    # Verify consistent step for all segments
                    for i in range(len(sorted_ref) -1):
                        if (sorted_ref[i+1][0] - sorted_ref[i][0] != dr or
                            sorted_ref[i+1][1] - sorted_ref[i][1] != dc):
                            is_diag = False
                            break
            else: # Single reference pixel - cannot determine line orientation
                is_diag = False

            if is_diag:
                 orientation = "Diagonal"
            else:
                 orientation = "Other" # Fallback if not clear line type
        else: # Only one reference pixel, or empty reference pixels
            orientation = "Other"


    return background_color, marker_pixel, reference_pixels, orientation, ref_rows_set, ref_cols_set


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    rows, cols = output_grid.shape

    # Find background, marker, reference structure, orientation, and ref rows/cols
    bg_color, marker_pixel, ref_pixels, orientation, ref_rows, ref_cols = find_objects(input_np)

    # If marker or reference not found, or orientation unclear, return original grid
    if not marker_pixel or not ref_pixels or orientation == "Other" or orientation is None:
        # Check if marker_pixel exists but ref_pixels is empty (only marker exists)
        if marker_pixel and not ref_pixels:
             # No reference, no transformation defined by examples
             return input_grid
        # Otherwise, return input for unclear cases
        print(f"Warning: No clear transformation possible. Marker: {marker_pixel}, Ref Pixels: {len(ref_pixels)}, Orientation: {orientation}")
        return input_grid

    marker_pos, marker_color = marker_pixel
    marker_r, marker_c = marker_pos

    # Execute drawing based on orientation
    if orientation == "Vertical":
        # Reference structure is vertical
        ref_c = list(ref_cols)[0] # Should only be one column in ref_cols

        # Define drawing range for columns
        draw_start_col = ref_c + 1
        draw_end_col = marker_c
        col_step = 1 if draw_end_col >= draw_start_col else -1

        # Draw horizontal line in marker's row
        for c in range(draw_start_col, draw_end_col + col_step, col_step):
             if 0 <= marker_r < rows and 0 <= c < cols:
                 output_grid[marker_r, c] = marker_color

    elif orientation == "Horizontal":
        # Reference structure is horizontal
        ref_r = list(ref_rows)[0] # Should only be one row in ref_rows

        # Define drawing range for rows
        draw_start_row = ref_r + 1
        draw_end_row = marker_r
        row_step = 1 if draw_end_row >= draw_start_row else -1

        # Draw vertical line in marker's column
        for r in range(draw_start_row, draw_end_row + row_step, row_step):
             if 0 <= r < rows and 0 <= marker_c < cols:
                 output_grid[r, marker_c] = marker_color

    elif orientation == "Diagonal":
        # Reference structure is diagonal

        # Determine the direction from marker towards the reference structure center (approximate)
        if not ref_pixels: # Should not happen due to earlier check, but safety first
             return output_grid.tolist()
             
        ref_center_r = sum(r for r, c, clr in ref_pixels) / len(ref_pixels)
        ref_center_c = sum(c for r, c, clr in ref_pixels) / len(ref_pixels)

        # Determine primary direction vector (dr, dc)
        dr = 0
        if ref_center_r < marker_r: dr = -1  # Target is above marker
        elif ref_center_r > marker_r: dr = 1 # Target is below marker

        dc = 0
        if ref_center_c < marker_c: dc = -1  # Target is left of marker
        elif ref_center_c > marker_c: dc = 1 # Target is right of marker
        
        # Ensure step is purely diagonal (abs(dr)=1 and abs(dc)=1)
        # If marker is directly aligned horizontally or vertically with the center,
        # infer diagonal direction based on relative quadrant (like in example 3)
        if dr == 0 or dc == 0:
            if marker_r > ref_center_r and marker_c < ref_center_c: dr, dc = -1, 1  # Lower Left -> Up Right
            elif marker_r < ref_center_r and marker_c < ref_center_c: dr, dc = 1, 1 # Upper Left -> Down Right
            elif marker_r < ref_center_r and marker_c > ref_center_c: dr, dc = 1, -1 # Upper Right -> Down Left
            elif marker_r > ref_center_r and marker_c > ref_center_c: dr, dc = -1, -1 # Lower Right -> Up Left
            else: # On axis or center? Need a default or better rule. Example 3 was LL.
                  # Defaulting based on example 3 if needed.
                  if dr == 0 and dc == 0: # Marker is exactly at center? Unlikely.
                       print("Warning: Cannot determine diagonal direction reliably.")
                       # Guessing based on Example 3's marker being lower-left of structure
                       dr, dc = -1, 1 
                  elif dr == 0: # Vertically aligned
                       dc = 1 if marker_c < ref_center_c else -1 # Move towards center col
                       dr = 1 if marker_r < ref_center_r else -1 # Also move towards center row
                  elif dc == 0: # Horizontally aligned
                       dr = 1 if marker_r < ref_center_r else -1 # Move towards center row
                       dc = 1 if marker_c < ref_center_c else -1 # Also move towards center col

        # Start drawing path one step away from marker
        curr_r, curr_c = marker_r + dr, marker_c + dc

        while 0 <= curr_r < rows and 0 <= curr_c < cols:
            # Check stop condition: current row OR current col is in reference sets
            stop_condition_met = (curr_r in ref_rows) or (curr_c in ref_cols)

            # Draw pixel
            output_grid[curr_r, curr_c] = marker_color

            # If stop condition met, break after drawing
            if stop_condition_met:
                break

            # Move to next step
            curr_r += dr
            curr_c += dc

    # Convert back to list of lists for the ARC standard format
    return output_grid.tolist()