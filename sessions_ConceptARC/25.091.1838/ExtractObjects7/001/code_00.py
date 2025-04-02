import numpy as np
from collections import deque

"""
Identifies a single-color line (vertical or horizontal) separator in the input grid.
Identifies distinct objects (contiguous blocks of color other than background or separator) on either side/top/bottom of the separator.
Extracts each object into its minimal bounding box grid.
If the separator was vertical, removes the top row from each extracted object grid.
Concatenates the processed object grids: horizontally if the separator was vertical, vertically if it was horizontal, maintaining original relative order.
"""

def find_separator(grid):
    """
    Finds a horizontal or vertical line of a single non-background color.

    Args:
        grid (np.array): Input grid.

    Returns:
        tuple: (separator_color, orientation, index) or (None, None, None) if not found.
               orientation is 'horizontal' or 'vertical'.
               index is the row or column index of the separator.
    """
    rows, cols = grid.shape
    background_color = 0

    # Check for horizontal separator
    for r in range(rows):
        color = grid[r, 0]
        if color != background_color and np.all(grid[r, :] == color):
            # Check if it truly separates regions (not just a border line)
            has_non_bg_above = r > 0 and np.any(grid[:r, :] != background_color)
            has_non_bg_below = r < rows - 1 and np.any(grid[r+1:, :] != background_color)
            if has_non_bg_above and has_non_bg_below:
                 return color, 'horizontal', r

    # Check for vertical separator
    for c in range(cols):
        color = grid[0, c]
        if color != background_color and np.all(grid[:, c] == color):
             # Check if it truly separates regions
            has_non_bg_left = c > 0 and np.any(grid[:, :c] != background_color)
            has_non_bg_right = c < cols - 1 and np.any(grid[:, c+1:] != background_color)
            if has_non_bg_left and has_non_bg_right:
                return color, 'vertical', c

    return None, None, None


def find_and_extract_objects(grid, ignore_color):
    """
    Finds connected components (objects) of the same color, ignoring background and a specific color.
    Extracts each object into its minimal bounding box.

    Args:
        grid (np.array): Input grid.
        ignore_color (int): Color to ignore (typically the separator color).

    Returns:
        list: A list of tuples, where each tuple is (object_grid, bounding_box).
              bounding_box is (min_r, min_c, max_r, max_c).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    background_color = 0

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # Start search if pixel is not background, not ignored, and not visited
            if color != background_color and color != ignore_color and not visited[r, c]:
                component_color = color
                q = deque([(r, c)])
                visited[r, c] = True
                points = [(r, c)]
                min_r, min_c, max_r, max_c = r, c, r, c

                while q:
                    row, col = q.popleft()

                    # Update bounding box
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == component_color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            points.append((nr, nc))

                # Extract the object into its own grid
                height = max_r - min_r + 1
                width = max_c - min_c + 1
                # Initialize with background color (important for shapes like 'C')
                obj_grid = np.full((height, width), background_color, dtype=int) 
                for pr, pc in points:
                    obj_grid[pr - min_r, pc - min_c] = component_color

                objects.append((obj_grid, (min_r, min_c, max_r, max_c)))

    return objects

def crop_top_row(obj_grid):
    """Removes the top row of a grid."""
    if obj_grid.shape[0] > 1:
        return obj_grid[1:, :]
    else:
        # Handle case of 1-row object, return empty grid of same width?
        # Or maybe just the original grid if cropping makes it disappear?
        # For this task, based on examples, objects are > 1 row high when cropped.
        return obj_grid[1:, :] # This will be empty if height was 1


def transform(input_grid):
    """
    Transforms the input grid based on separator and object manipulation rules.
    """
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape

    # 1. Identify the separator line
    sep_color, sep_orientation, sep_index = find_separator(grid)
    if sep_color is None:
        # Handle error or return input? Based on task, assume separator exists.
        return input_grid # Or raise an error

    # 2. Identify and extract objects
    objects = find_and_extract_objects(grid, sep_color)

    # 3. Filter and sort objects based on separator position
    objects_part1 = [] # Left or Top
    objects_part2 = [] # Right or Bottom

    if sep_orientation == 'vertical':
        for obj_grid, bbox in objects:
            min_r, min_c, max_r, max_c = bbox
            if max_c < sep_index:
                objects_part1.append((obj_grid, bbox))
            elif min_c > sep_index:
                objects_part2.append((obj_grid, bbox))
        # Sort by horizontal position (min_c) just in case, though examples have one per side
        objects_part1.sort(key=lambda x: x[1][1])
        objects_part2.sort(key=lambda x: x[1][1])

    elif sep_orientation == 'horizontal':
        for obj_grid, bbox in objects:
             min_r, min_c, max_r, max_c = bbox
             if max_r < sep_index:
                 objects_part1.append((obj_grid, bbox))
             elif min_r > sep_index:
                 objects_part2.append((obj_grid, bbox))
        # Sort by vertical position (min_r)
        objects_part1.sort(key=lambda x: x[1][0])
        objects_part2.sort(key=lambda x: x[1][0])

    ordered_objects = objects_part1 + objects_part2
    processed_grids = [obj[0] for obj in ordered_objects] # Get just the grids

    # 4. Conditional Step: Crop top row if separator was vertical
    if sep_orientation == 'vertical':
        processed_grids = [crop_top_row(g) for g in processed_grids]

    # 5. Combine the processed object grids
    if not processed_grids:
        return [] # Return empty if no objects found/processed

    if sep_orientation == 'vertical':
        # Concatenate horizontally
        output_grid_np = np.hstack(processed_grids)
    elif sep_orientation == 'horizontal':
        # Concatenate vertically
        output_grid_np = np.vstack(processed_grids)
    else: # Should not happen if separator was found
        return input_grid

    # Convert final numpy array back to list of lists
    output_grid = output_grid_np.tolist()

    return output_grid