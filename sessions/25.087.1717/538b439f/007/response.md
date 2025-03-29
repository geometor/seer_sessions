```python
import numpy as np
from collections import Counter

"""
The transformation identifies a background color, a dominant separator line (horizontal or vertical), and distinct objects. The specific transformation depends on the separator's orientation:

1.  **Vertical Separator:**
    *   Identifies "significant" objects (contiguous shapes of non-background, non-separator color with size >= 3).
    *   For each significant object, it finds the vertical range (min_r to max_r) of the object.
    *   It then identifies the horizontal range of columns strictly *between* the object's edge and the separator line.
    *   Within this vertical and horizontal range (forming a rectangle), it fills any pixels matching the original background color with the *separator's color*.

2.  **Horizontal Separator:**
    *   Identifies all contiguous objects (including size 1) of non-background, non-separator color.
    *   Focuses only on objects located *below* the separator line.
    *   Iterates through each column of the grid.
    *   For a given column `c`:
        *   Checks if any Green (3) object exists *below* the separator and spans column `c`.
        *   If yes, it fills the portion of column `c` *above* the separator line (from row 0 to `separator_index - 1`) with Green (3), but only modifies pixels that were originally the background color.
        *   If no Green object exists below in column `c`, it then checks if any Blue (1) object exists *below* the separator and spans column `c`.
        *   If yes, it fills the portion of column `c` *above* the separator line with the *separator's color*, again only modifying background pixels.
    *   Objects located *above* the separator line do not influence the output.
"""

# Helper function to find the most frequent color, assumed to be the background
def find_background_color(grid):
    """Finds the most frequent color in the grid."""
    counts = Counter(grid.flatten())
    if not counts:
        return 0 # Default if grid is empty
    # Find the color with the maximum count
    background_color = counts.most_common(1)[0][0]
    return background_color

# Helper function to find a dominant separator line
def find_separator(grid, background_color):
    """
    Finds a dominant horizontal or vertical line that is not the background color.
    Returns (orientation, index, color) or None.
    Uses a threshold heuristic (default 70% coverage).
    """
    height, width = grid.shape
    separator = None
    # Heuristic threshold: a line must cover at least this fraction of the dimension
    threshold_factor = 0.7

    # Check for horizontal lines
    best_h_line = (-1, -1, -1) # index, color, count
    for r in range(height):
        row = grid[r, :]
        counts_non_bg = Counter(c for c in row if c != background_color)
        # Check if the row consists predominantly of one non-background color
        if len(counts_non_bg) == 1:
            line_color = list(counts_non_bg.keys())[0]
            line_count = counts_non_bg[line_color]
            # Check if it covers a significant portion of the width
            if line_count >= width * threshold_factor:
                # Prioritize longer lines
                if line_count > best_h_line[2]:
                    best_h_line = (r, line_color, line_count)

    # Check for vertical lines
    best_v_line = (-1, -1, -1) # index, color, count
    for c in range(width):
        col = grid[:, c]
        counts_non_bg = Counter(r for r in col if r != background_color)
        # Check if the column consists predominantly of one non-background color
        if len(counts_non_bg) == 1:
            line_color = list(counts_non_bg.keys())[0]
            line_count = counts_non_bg[line_color]
             # Check if it covers a significant portion of the height
            if line_count >= height * threshold_factor:
                 # Prioritize longer lines
                if line_count > best_v_line[2]:
                     best_v_line = (c, line_color, line_count)

    # Determine the best separator (prefer vertical if counts are equal and both exist)
    h_idx, h_color, h_count = best_h_line
    v_idx, v_color, v_count = best_v_line

    if h_count > 0 and h_count > v_count:
        separator = ('horizontal', h_idx, h_color)
    elif v_count > 0 and v_count >= h_count: # Prefer vertical if counts equal or greater
        separator = ('vertical', v_idx, v_color)
    else:
        separator = None # No dominant line found

    #print(f"Separator Found: {separator}") # Debug print
    return separator

# Helper function to find contiguous objects using Breadth-First Search (BFS)
def find_objects(grid, background_color, separator_color):
    """
    Finds all contiguous objects of colors other than background and separator.
    Uses BFS.
    Returns a list of tuples: [(color, set_of_pixels, min_r, max_r, min_c, max_c), ...].
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects_found = []
    potential_target_colors = set(np.unique(grid)) - {background_color}
    if separator_color is not None:
        potential_target_colors -= {separator_color}

    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            # Start BFS if we find an unvisited pixel of a potential target color
            if color in potential_target_colors and not visited[r, c]:
                q = [(r, c)]
                visited[r, c] = True
                object_pixels = set()
                min_r_obj, max_r_obj, min_c_obj, max_c_obj = r, r, c, c

                head = 0
                while head < len(q):
                    row, col = q[head]
                    head += 1
                    object_pixels.add((row, col))
                    min_r_obj = min(min_r_obj, row)
                    max_r_obj = max(max_r_obj, row)
                    min_c_obj = min(min_c_obj, col)
                    max_c_obj = max(max_c_obj, col)

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                # Store the found object
                objects_found.append((color, object_pixels, min_r_obj, max_r_obj, min_c_obj, max_c_obj))

    #print(f"Objects Found: {len(objects_found)}") # Debug print
    #for o in objects_found: print(f"  Color: {o[0]}, Size: {len(o[1])}, Bounds: ({o[2]}-{o[3]}, {o[4]}-{o[5]})") # Debug
    return objects_found


def transform(input_grid):
    """
    Transforms the input grid based on the rules derived from examples.
    Handles vertical and horizontal separator cases differently.
    """
    # Convert to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_grid_np)
    height, width = input_grid_np.shape

    # 1. Identify Background Color
    background_color = find_background_color(input_grid_np)
    #print(f"Background Color: {background_color}") # Debug print

    # 2. Locate the Separator Line
    separator_info = find_separator(input_grid_np, background_color)
    if not separator_info:
        # If no clear separator found, return the original grid
        #print("No separator found.") # Debug
        return output_grid.tolist()
    orientation, separator_index, separator_color = separator_info

    # 3. Find all objects (excluding background and separator)
    all_objects = find_objects(input_grid_np, background_color, separator_color)
    if not all_objects:
        # No target objects found, return original
        #print("No target objects found.") # Debug
        return output_grid.tolist()

    # 4. Apply Transformation Logic based on Orientation
    if orientation == 'vertical':
        sep_c = separator_index
        # Filter for significant objects (size >= 3) for vertical case
        significant_objects = [obj for obj in all_objects if len(obj[1]) >= 3]
        #print(f"Processing Vertical Separator at c={sep_c}, color={separator_color}. Significant Objects: {len(significant_objects)}") #Debug

        for obj_color, pixels, min_r, max_r, min_c, max_c in significant_objects:
            #print(f"  Processing obj: Color={obj_color}, Size={len(pixels)}, Bounds=({min_r}-{max_r}, {min_c}-{max_c})") # Debug
            # Determine fill range columns based on object position relative to separator
            fill_min_c, fill_max_c = -1, -1
            if max_c < sep_c: # Target is left of separator
                fill_min_c = max_c + 1
                fill_max_c = sep_c - 1
                #print(f"    Object left of separator. Fill columns: {fill_min_c} to {fill_max_c}") # Debug
            elif min_c > sep_c: # Target is right of separator
                fill_min_c = sep_c + 1
                fill_max_c = min_c - 1
                #print(f"    Object right of separator. Fill columns: {fill_min_c} to {fill_max_c}") # Debug
            else: # Target overlaps or touches separator - skip filling for this object
                #print(f"    Object overlaps/touches separator. Skipping fill.") # Debug
                continue

            # Ensure fill range is valid and within grid bounds
            fill_min_c = max(0, fill_min_c)
            fill_max_c = min(width - 1, fill_max_c)

            if fill_min_c > fill_max_c:
                #print(f"    Invalid fill range after bounds check. Skipping.") # Debug
                continue

            # Fill the rectangular region with separator color if it's background
            for r in range(min_r, max_r + 1):
                # Check row bounds just in case
                if 0 <= r < height:
                    for c in range(fill_min_c, fill_max_c + 1):
                         # Check col bounds (redundant given loop range, but safe)
                         if 0 <= c < width:
                             # Only change background pixels
                             if output_grid[r, c] == background_color:
                                 output_grid[r, c] = separator_color
                                 #print(f"      Filling ({r}, {c}) with {separator_color}") # Debug


    elif orientation == 'horizontal':
        sep_r = separator_index
        # Consider only objects BELOW the separator
        objects_below = [obj for obj in all_objects if obj[2] > sep_r] # obj[2] is min_r
        #print(f"Processing Horizontal Separator at r={sep_r}, color={separator_color}. Objects below: {len(objects_below)}") # Debug

        # Determine fill color for each column above the separator
        # Iterate through columns 0 to width-1
        for c in range(width):
            fill_color_for_col = None # Default: no fill
            has_green_below_in_col = False
            has_blue_below_in_col = False

            # Check objects below the separator that span this column 'c'
            for obj_color, pixels, min_r_obj, max_r_obj, min_c_obj, max_c_obj in objects_below:
                if min_c_obj <= c <= max_c_obj: # Object spans this column
                    #print(f"  Col {c}: Found object below: Color={obj_color}, Bounds=({min_r_obj}-{max_r_obj}, {min_c_obj}-{max_c_obj})") # Debug
                    if obj_color == 3: # Green
                        has_green_below_in_col = True
                        #print(f"    Found GREEN below in col {c}") # Debug
                        break # Green takes priority for this column
                    elif obj_color == 1: # Blue
                        #print(f"    Found BLUE below in col {c}") # Debug
                        has_blue_below_in_col = True
                        # Don't break, need to check if there's also a green one further down the list

            # Determine fill color based on findings for this specific column
            if has_green_below_in_col:
                fill_color_for_col = 3 # Green
                #print(f"  Col {c}: Setting fill color to GREEN (3)") # Debug
            elif has_blue_below_in_col:
                fill_color_for_col = separator_color # Use separator color for blue
                #print(f"  Col {c}: Setting fill color to Separator Color ({separator_color})") # Debug
            #else:
                #print(f"  Col {c}: No Green or Blue found below. No fill.") # Debug

            # If a fill color was determined, fill this column 'c' above the separator
            if fill_color_for_col is not None:
                for r in range(sep_r): # Rows 0 to sep_r - 1
                    # Check bounds (should be fine)
                    if 0 <= r < height and 0 <= c < width:
                        # Only change background pixels
                        if output_grid[r, c] == background_color:
                            output_grid[r, c] = fill_color_for_col
                            #print(f"    Filling ({r}, {c}) with {fill_color_for_col}") # Debug


    # 5. Return the modified grid as a list of lists
    return output_grid.tolist()
```