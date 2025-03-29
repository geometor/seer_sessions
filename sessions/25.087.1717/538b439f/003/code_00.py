import numpy as np
from collections import Counter

"""
Identifies a background color, a single dominant separator line (horizontal or vertical), and target objects (contiguous shapes of other colors).
Transformation logic depends on the separator's orientation:

1.  **Vertical Separator:** Fills the rectangular area between each target object and the separator line (on the side facing the separator) with the separator's color. The fill occurs within the row span of the target object. Only pixels matching the original background color are changed.

2.  **Horizontal Separator:**
    *   For target objects BELOW the separator: Fills the rectangular area ABOVE the separator line, within the column span of the object, with the OBJECT's color. Only pixels matching the original background color or noise colors (scattered non-background/non-separator pixels) are changed.
    *   For target objects ABOVE the separator: Fills the rectangular area BELOW the separator line, within the column span of the object, with the SEPARATOR's color. Only pixels matching the original background color or noise colors are changed.
"""

def find_background_color(grid):
    """Finds the most frequent color in the grid."""
    counts = Counter(grid.flatten())
    if not counts:
        return 0 # Default if grid is empty
    # Find the color with the maximum count
    background_color = counts.most_common(1)[0][0]
    return background_color

def find_separator(grid, background_color):
    """
    Finds a dominant horizontal or vertical line that is not the background color.
    Returns (orientation, index, color) or None.
    Uses a threshold heuristic (default 70% coverage).
    """
    height, width = grid.shape
    separator = None
    threshold_factor = 0.7

    # Check for horizontal lines
    for r in range(height):
        row = grid[r, :]
        counts_non_bg = Counter(c for c in row if c != background_color)
        # Check if the row consists predominantly of one non-background color
        if len(counts_non_bg) == 1:
            line_color = list(counts_non_bg.keys())[0]
            line_count = counts_non_bg[line_color]
            # Check if it covers a significant portion of the width
            if line_count >= width * threshold_factor:
                 # Prioritize longer lines if multiple candidates exist
                current_sep_strength = separator[3] if separator else -1
                if separator is None or line_count > current_sep_strength:
                     separator = ('horizontal', r, line_color, line_count)

    # Check for vertical lines
    for c in range(width):
        col = grid[:, c]
        counts_non_bg = Counter(r for r in col if r != background_color)
        # Check if the column consists predominantly of one non-background color
        if len(counts_non_bg) == 1:
            line_color = list(counts_non_bg.keys())[0]
            line_count = counts_non_bg[line_color]
             # Check if it covers a significant portion of the height
            if line_count >= height * threshold_factor:
                current_sep_strength = separator[3] if separator else -1
                # Prioritize longer lines or vertical lines if strengths are equal
                if line_count > current_sep_strength or \
                   (separator and line_count == current_sep_strength and separator[0] == 'horizontal'):
                    separator = ('vertical', c, line_color, line_count)

    return separator[:3] if separator else None


def find_objects(grid, background_color, separator_color, min_size=1):
    """
    Finds all contiguous objects of colors other than background and separator.
    Uses BFS. Filters objects smaller than min_size.
    Returns a list of tuples: [(color, min_r, max_r, min_c, max_c), ...].
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects_found = []
    potential_target_colors = set(np.unique(grid)) - {background_color, separator_color}

    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color in potential_target_colors and not visited[r, c]:
                # Start BFS for a new potential object
                q = [(r, c)]
                visited[r, c] = True
                object_pixels = []
                min_r_obj, max_r_obj, min_c_obj, max_c_obj = r, r, c, c

                head = 0
                while head < len(q):
                    row, col = q[head]
                    head += 1
                    object_pixels.append((row, col))
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

                # Add object if it meets the minimum size requirement
                if len(object_pixels) >= min_size:
                    objects_found.append((color, min_r_obj, max_r_obj, min_c_obj, max_c_obj))

    return objects_found

def get_noise_colors(grid, background_color, separator_color, target_object_colors):
    """Identifies colors present in the grid that are not background, separator, or part of identified target objects."""
    all_colors = set(np.unique(grid))
    noise = all_colors - {background_color, separator_color} - set(target_object_colors)
    return noise


def transform(input_grid):
    """
    Applies the transformation rule based on separator and target shapes.
    """
    # Initialize
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

    # 3. Identify Target Objects (consider min_size=2 to filter noise initially?)
    # Let's stick with min_size=1 for now and handle noise explicitly if needed.
    target_objects = find_objects(input_grid_np, background_color, separator_color, min_size=1)
    if not target_objects:
        # No target objects found, return original
        return output_grid.tolist()
        
    target_object_colors = {obj[0] for obj in target_objects}
    noise_colors = get_noise_colors(input_grid_np, background_color, separator_color, target_object_colors)


    # 4. Apply Fill Logic based on Orientation
    if orientation == 'vertical':
        sep_c = separator_index
        for obj_color, min_r, max_r, min_c, max_c in target_objects:
            fill_min_c, fill_max_c = -1, -1
            # Determine fill range based on object position relative to separator
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
                # Clamp row index just in case, though should be within bounds
                r_clamped = max(0, min(r, height - 1))
                for c in range(fill_min_c, fill_max_c + 1):
                     # Clamp column index
                     c_clamped = max(0, min(c, width - 1))
                     # Only change background pixels
                     if output_grid[r_clamped, c_clamped] == background_color:
                         output_grid[r_clamped, c_clamped] = separator_color

    elif orientation == 'horizontal':
        sep_r = separator_index
        for obj_color, min_r, max_r, min_c, max_c in target_objects:
            # Fill based on object position relative to separator
            if min_r > sep_r: # Target is BELOW separator
                fill_color = obj_color
                fill_min_row = 0
                fill_max_row = sep_r - 1
            elif max_r < sep_r: # Target is ABOVE separator
                fill_color = separator_color
                fill_min_row = sep_r + 1
                fill_max_row = height - 1 # Fill all the way down? Or just to object? Analysis says all the way down.
            else: # Target overlaps or touches separator - skip filling for this object
                continue

            # Define column bounds for filling
            fill_min_col = min_c
            fill_max_col = max_c

            # Fill the region
            for r in range(fill_min_row, fill_max_row + 1):
                 # Clamp row index
                r_clamped = max(0, min(r, height - 1))
                for c in range(fill_min_col, fill_max_col + 1):
                     # Clamp column index
                     c_clamped = max(0, min(c, width - 1))
                     # Change pixel if it's background OR considered noise
                     current_pixel_color = output_grid[r_clamped, c_clamped]
                     if current_pixel_color == background_color or current_pixel_color in noise_colors:
                         output_grid[r_clamped, c_clamped] = fill_color

    # 5. Return the modified grid
    return output_grid.tolist()