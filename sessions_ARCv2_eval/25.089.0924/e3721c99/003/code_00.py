import numpy as np
from collections import deque

"""
Transformation Rule:
1. Identify "reference patterns": These are small, contiguous shapes of non-white (0), non-gray (5) colors. Exclude large structures like long lines (e.g., the blue separator often seen). Store each pattern's color, dimensions (height, width), and its 'form' - the set of relative coordinates of its colored pixels from its top-left corner.
2. Initialize the output grid as a copy of the input grid.
3. Create a boolean mask (`processed_mask`) of the same dimensions as the grid, initialized to False. This tracks pixels successfully colored by a pattern match.
4. Iterate through every possible top-left anchor position (r, c) in the input grid.
5. For each anchor (r, c):
    a. Iterate through each identified reference pattern.
    b. Check if a sub-grid of the pattern's dimensions, starting at (r, c), can fit within the input grid boundaries.
    c. If it fits, extract this sub-grid from the input grid.
    d. Compare the pattern of *gray* pixels within the sub-grid to the 'form' of the reference pattern. A match occurs if:
        i. For every relative coordinate (dr, dc) present in the reference pattern's form, the corresponding pixel `sub_grid[dr, dc]` is gray (5).
        ii. For every relative coordinate (dr, dc) *not* present in the reference pattern's form (within the pattern's bounding box), the corresponding pixel `sub_grid[dr, dc]` is *not* gray (5).
    e. If an exact match is found:
        i. Get the color of the matching reference pattern.
        ii. For each relative coordinate (dr, dc) in the reference pattern's form:
            - Calculate the absolute coordinate `(abs_r, abs_c) = (r + dr, c + dc)`.
            - Update the `output_grid[abs_r, abs_c]` to the pattern's color.
            - Mark `processed_mask[abs_r, abs_c] = True`.
        iii. Break the inner loop (stop checking other patterns for this anchor (r, c)), as a region can only match one pattern starting at a specific anchor.
6. After checking all anchors, perform a final cleanup: Iterate through the `output_grid`. If any pixel `(r, c)` is still gray (5) AND `processed_mask[r, c]` is False, change `output_grid[r, c]` to white (0).
7. Return the modified output grid.
"""

def find_objects_with_details(grid, colors_to_find):
    """
    Finds contiguous objects of specified colors, returning details including form.

    Args:
        grid (np.array): The input grid.
        colors_to_find (set): A set of color values to search for.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains:
              'color': The color of the object.
              'pixels': A set of (row, col) tuples for the object's pixels.
              'min_r', 'min_c': Coordinates of the top-left corner.
              'height', 'width': Dimensions of the bounding box.
              'form': A set of (dr, dc) relative coordinates from the top-left.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color in colors_to_find and not visited[r, c]:
                obj_pixels_list = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                # BFS to find all connected pixels
                while q:
                    row, col = q.popleft()
                    obj_pixels_list.append((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                # Calculate properties
                obj_pixels_set = set(obj_pixels_list)
                height = max_r - min_r + 1
                width = max_c - min_c + 1
                form = set((p_r - min_r, p_c - min_c) for p_r, p_c in obj_pixels_set)

                objects.append({
                    'color': color,
                    'pixels': obj_pixels_set,
                    'min_r': min_r,
                    'min_c': min_c,
                    'height': height,
                    'width': width,
                    'form': form
                })

    return objects

def filter_reference_patterns(objects, grid_rows, grid_cols):
    """Filters potential objects to identify true reference patterns."""
    patterns = []
    # Heuristic threshold to exclude large lines/structures
    # Exclude if object spans full grid width/height or is just very large
    max_reasonable_dim = max(grid_rows, grid_cols) * 0.8

    for obj in objects:
        is_separator_line = (
            obj['color'] == 1 and # Assuming blue lines are separators
            (obj['width'] >= max_reasonable_dim or obj['height'] >= max_reasonable_dim)
        )
        # Add other filtering conditions if needed (e.g., minimum size)
        is_too_small = len(obj['pixels']) < 2 # Exclude single pixels? Maybe not needed for this task.

        if not is_separator_line: # and not is_too_small:
             patterns.append(obj)
    return patterns


def transform(input_grid):
    """
    Applies the template-matching transformation rule to the input grid.
    """
    rows, cols = input_grid.shape
    output_grid = np.copy(input_grid)
    processed_mask = np.zeros_like(input_grid, dtype=bool)

    # 1. & 2. Identify and filter reference patterns
    all_colors = set(np.unique(input_grid))
    potential_ref_colors = all_colors - {0, 5} # Exclude white (0) and gray (5)
    if not potential_ref_colors: # Handle case with no references
        reference_patterns = []
    else:
        potential_objects = find_objects_with_details(input_grid, potential_ref_colors)
        reference_patterns = filter_reference_patterns(potential_objects, rows, cols)

    # 3. Iterate through grid anchors and try to match patterns
    for r in range(rows):
        for c in range(cols):
            # Optimization: Can skip if input[r,c] is not gray?
            # No, because a pattern might start here even if the top-left isn't gray,
            # but the *anchor point* logic implies we only *start* checking if the anchor
            # pixel could potentially be part of a match. Let's stick to the plan:
            # check every r,c as a potential top-left corner.

            for pattern in reference_patterns:
                p_h, p_w = pattern['height'], pattern['width']
                p_form = pattern['form']
                p_color = pattern['color']

                # Check bounds: Can the pattern fit starting at (r, c)?
                if r + p_h <= rows and c + p_w <= cols:
                    # Extract sub-grid
                    sub_grid = input_grid[r : r + p_h, c : c + p_w]

                    # Compare sub-grid's gray pixels to pattern form
                    match = True
                    pixels_to_color = [] # Store coords relative to (r,c) for this match

                    for dr in range(p_h):
                        for dc in range(p_w):
                            sub_pixel_is_gray = (sub_grid[dr, dc] == 5)
                            coord_in_form = ((dr, dc) in p_form)

                            if coord_in_form:
                                if not sub_pixel_is_gray:
                                    match = False
                                    break
                                else:
                                     # Only store the coordinates that should be colored
                                     pixels_to_color.append((dr, dc))
                            elif sub_pixel_is_gray: # Pixel is gray but shouldn't be based on pattern
                                match = False
                                break
                        if not match:
                            break

                    # If match found, update output and mask
                    if match:
                        for dr, dc in pixels_to_color: # Use the stored coordinates
                            abs_r, abs_c = r + dr, c + dc
                            # Check if not already processed by another pattern match
                            # This prevents overwriting parts of successful previous matches
                            # anchored elsewhere, which might happen with overlapping patterns.
                            # Only color if the target pixel in output is still gray
                            if output_grid[abs_r, abs_c] == 5:
                                output_grid[abs_r, abs_c] = p_color
                                processed_mask[abs_r, abs_c] = True

                        # Break from pattern loop for this anchor (r,c)
                        # Assumes only one pattern can match starting at a given anchor
                        break
            # End pattern loop
        # End col loop
    # End row loop

    # 4. Final cleanup: Change remaining, unprocessed gray pixels to white
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 5 and not processed_mask[r, c]:
                output_grid[r, c] = 0

    return output_grid