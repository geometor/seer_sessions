```python
import numpy as np
from collections import Counter

"""
The transformation identifies a background color, a dominant separator line (horizontal or vertical), and distinct objects. The specific transformation depends on the separator's orientation:

1.  **Vertical Separator:**
    *   Identifies "significant" objects (contiguous shapes of non-background, non-separator color with size >= 3).
    *   For each significant object, it fills the rectangular area between the object's vertical extent and the separator line with the *separator's color*.
    *   This fill only occurs within the horizontal row span of the object.
    *   Only pixels matching the original background color are modified.

2.  **Horizontal Separator:**
    *   Identifies all contiguous objects (including size 1) of non-background, non-separator color.
    *   Focuses only on objects located *below* the separator line.
    *   For each column spanned by an object below the line:
        *   It fills the portion of that column *above* the separator line (from the top edge down to the separator).
        *   The fill color depends on the color of the object(s) below the separator in that column:
            *   If any Green (3) object exists below the separator in that column, the fill color is Green (3).
            *   Otherwise, if any Blue (1) object exists below the separator in that column, the fill color is the *separator's color*.
        *   Only pixels matching the original background color are modified.
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

    if h_count > v_count and h_count > 0:
        separator = ('horizontal', h_idx, h_color)
    elif v_count >= h_count and v_count > 0: # Prefer vertical if counts equal
        separator = ('vertical', v_idx, v_color)
    else:
        separator = None # No dominant line found

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

    # 2. Locate the Separator Line
    separator_info = find_separator(input_grid_np, background_color)
    if not separator_info:
        # If no clear separator found, return the original grid
        return output_grid.tolist()
    orientation, separator_index, separator_color = separator_info

    # 3. Find all objects
    all_objects = find_objects(input_grid_np, background_color, separator_color)
    if not all_objects:
        # No target objects found, return original
        return output_grid.tolist()

    # 4. Apply Transformation Logic based on Orientation
    if orientation == 'vertical':
        sep_c = separator_index
        # Filter for significant objects (size >= 3) for vertical case
        significant_objects = [obj for obj in all_objects if len(obj[1]) >= 3]

        for obj_color, pixels, min_r, max_r, min_c, max_c in significant_objects:
            # Determine fill range based on object position relative to separator
            fill_min_c, fill_max_c = -1, -1
            if max_c < sep_c: # Target is left of separator
                fill_min_c = max_c + 1
                fill_max_c = sep_c - 1
            elif min_c > sep_c: # Target is right of separator
                fill_min_c = sep_c + 1
                fill_max_c = min_c - 1
            else: # Target overlaps or touches separator - skip filling for this object
                continue

            # Ensure fill range is valid
            if fill_min_c > fill_max_c:
                continue

            # Fill the region with separator color if it's background
            for r in range(min_r, max_r + 1):
                # Check bounds just in case (should be fine)
                if 0 <= r < height:
                    for c in range(fill_min_c, fill_max_c + 1):
                         # Check bounds
                         if 0 <= c < width:
                             # Only change background pixels
                             if output_grid[r, c] == background_color:
                                 output_grid[r, c] = separator_color

    elif orientation == 'horizontal':
        sep_r = separator_index
        # Consider only objects BELOW the separator
        objects_below = [obj for obj in all_objects if obj[2] > sep_r]

        # Determine fill color for each column above the separator
        # Iterate through columns 0 to width-1
        for c in range(width):
            fill_color_for_col = None # Default: no fill
            has_green_below = False
            has_blue_below = False

            # Check objects below the separator that span this column
            for obj_color, pixels, min_r, max_r, min_c, max_c in objects_below:
                if min_c <= c <= max_c: # Object spans this column
                    if obj_color == 3: # Green
                        has_green_below = True
                        break # Green takes priority
                    elif obj_color == 1: # Blue
                        has_blue_below = True
                        # Don't break, check if there's a green one

            # Determine fill color based on findings
            if has_green_below:
                fill_color_for_col = 3 # Green
            elif has_blue_below:
                fill_color_for_col = separator_color # Use separator color for blue

            # If a fill color was determined, fill the column above the separator
            if fill_color_for_col is not None:
                for r in range(sep_r): # Rows 0 to sep_r - 1
                    # Check bounds (should be fine)
                    if 0 <= r < height and 0 <= c < width:
                        # Only change background pixels
                        if output_grid[r, c] == background_color:
                            output_grid[r, c] = fill_color_for_col

    # 5. Return the modified grid as a list of lists
    return output_grid.tolist()
```