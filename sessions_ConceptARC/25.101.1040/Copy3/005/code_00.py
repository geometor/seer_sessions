import copy
import collections
import numpy as np

"""
Transforms an input grid based on the presence or absence of magenta pixels (color 6).

Two distinct rules apply:

Rule 1: No Magenta Pixels Present
  - Assumes the grid width `W` is even.
  - Identifies all non-white pixels within the left half of the grid (columns 0 to W/2 - 1).
  - Determines the minimal bounding box enclosing these left-half non-white pixels.
  - Copies the rectangular region defined by this bounding box from the input grid's left half to the output grid's right half.
  - The top-left corner of the copied region in the output grid is `(bbox_min_row, W/2)`.
  - The left half of the grid remains unchanged. The right half is overwritten by the copied region.
  - If no non-white pixels are found in the left half, or if the width is odd, the grid remains unchanged.

Rule 2: Magenta Pixels Present
  - Finds all distinct non-white connected components in the entire grid.
  - Identifies the 'main pattern' (P): The non-magenta-only component with the largest bounding box area (ties broken by top-most, then left-most).
  - Identifies the 'marker' (M): The magenta-containing component whose top-left corner's column is greater than the main pattern's rightmost column. Among candidates, selects the one with the minimum row, then minimum column (top-most, left-most).
  - Calculates a destination top-left corner based on the marker's position: `(marker_min_row + 2, marker_min_col)`.
  - Copies the entire rectangular region defined by the main pattern's (P) bounding box from the input grid to the calculated destination area in the output grid.
  - All other parts of the grid (outside the destination copy area) remain unchanged from the input.
  - If either the main pattern (P) or the marker (M) cannot be identified according to the rules, the grid remains unchanged.
"""

def find_connected_components(grid: list[list[int]], ignore_color: int = 0, bounds: tuple = None) -> list[dict]:
    """
    Finds all connected components in the grid or within specified bounds, ignoring a specific color.
    Uses 4-connectivity (horizontal/vertical).

    Args:
        grid: The input grid (list of lists of integers).
        ignore_color: The color value to ignore (treat as background).
        bounds: Optional tuple (min_r, min_c, max_r, max_c) defining the search area.
                Components must start within bounds and only connected pixels within bounds are included.

    Returns:
        A list of dictionaries, where each dictionary represents a component.
    """
    grid_np = np.array(grid)
    height, width = grid_np.shape
    
    if bounds:
        min_r_bound, min_c_bound, max_r_bound, max_c_bound = bounds
        min_r_bound = max(0, min_r_bound)
        min_c_bound = max(0, min_c_bound)
        max_r_bound = min(height - 1, max_r_bound)
        max_c_bound = min(width - 1, max_c_bound)
    else:
        min_r_bound, min_c_bound = 0, 0
        max_r_bound, max_c_bound = height - 1, width - 1

    visited = set()
    components = []
    component_id_counter = 0

    for r in range(min_r_bound, max_r_bound + 1):
        for c in range(min_c_bound, max_c_bound + 1):
            if grid_np[r, c] != ignore_color and (r, c) not in visited:
                component_id_counter += 1
                component_coords = set()
                component_colors = set()
                q = collections.deque([(r, c)])
                visited.add((r, c))
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    row, col = q.popleft()
                    component_coords.add((row, col))
                    # Use item() to get native Python int if necessary, though sets handle numpy ints fine
                    component_colors.add(grid_np[row, col].item()) 
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if min_r_bound <= nr <= max_r_bound and min_c_bound <= nc <= max_c_bound and \
                           grid_np[nr, nc] != ignore_color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))

                if component_coords:
                    bbox = (min_r, min_c, max_r, max_c)
                    bbox_area = (max_r - min_r + 1) * (max_c - min_c + 1)
                    components.append({
                        'id': component_id_counter,
                        'coords': component_coords,
                        'colors': component_colors,
                        'bounding_box': bbox,
                        'bounding_box_area': bbox_area,
                        'pixel_count': len(component_coords)
                    })
    return components

def get_bounding_box_of_pixels(pixels: set, grid_shape: tuple) -> tuple | None:
    """
    Calculates the minimal bounding box enclosing a set of pixel coordinates.

    Args:
        pixels: A set of (row, col) tuples.
        grid_shape: A tuple (height, width) for boundary checks (though pixels should be valid).

    Returns:
        A tuple (min_row, min_col, max_row, max_col) or None if the set is empty.
    """
    if not pixels:
        return None
    min_r = grid_shape[0]
    min_c = grid_shape[1]
    max_r = -1
    max_c = -1
    for r, c in pixels:
        min_r = min(min_r, r)
        min_c = min(min_c, c)
        max_r = max(max_r, r)
        max_c = max(max_c, c)
    # Ensure valid bounds if only one pixel or a line exists
    if max_r == -1: # Should not happen if pixels is not empty, but safe check
        return None
    return (min_r, min_c, max_r, max_c)

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rules based on magenta presence.
    """
    # Initialize output_grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)
    grid_np = np.array(input_grid)
    height, width = grid_np.shape
    magenta_color = 6
    white_color = 0

    # Check for magenta presence
    has_magenta = np.any(grid_np == magenta_color)

    if not has_magenta:
        # --- Rule 1: No Magenta ---
        # Check if width is even (rule assumption)
        if width % 2 == 0:
            mid_col = width // 2
            
            # Find all non-white pixels in the left half
            left_half_pixels = set()
            for r in range(height):
                for c in range(mid_col):
                    if grid_np[r, c] != white_color:
                        left_half_pixels.add((r, c))

            # If non-white pixels exist, find their bounding box
            if left_half_pixels:
                source_bbox = get_bounding_box_of_pixels(left_half_pixels, (height, width))
                
                if source_bbox:
                    bbox_min_r, bbox_min_c, bbox_max_r, bbox_max_c = source_bbox
                    dest_start_col = mid_col

                    # Copy the region defined by the bounding box
                    for r_offset in range(bbox_max_r - bbox_min_r + 1):
                        for c_offset in range(bbox_max_c - bbox_min_c + 1):
                            src_r = bbox_min_r + r_offset
                            src_c = bbox_min_c + c_offset
                            
                            # Ensure source coords are valid and within the left half
                            if 0 <= src_r < height and 0 <= src_c < mid_col: 
                                dest_r = src_r  # Destination row is the same as source row
                                dest_c = dest_start_col + c_offset # Destination col starts at mid_col

                                # Check destination bounds before writing
                                if 0 <= dest_r < height and 0 <= dest_c < width:
                                    output_grid[dest_r][dest_c] = input_grid[src_r][src_c]
        # Implicit: If width is odd and no magenta, return the initial copy.

    else:
        # --- Rule 2: Magenta Present ---
        # Find all components in the entire grid
        all_components = find_connected_components(input_grid, ignore_color=white_color)

        # Identify the main pattern (P)
        main_pattern = None
        non_magenta_only_components = [
            comp for comp in all_components if not (comp['colors'] == {magenta_color})
        ]
        if non_magenta_only_components:
            non_magenta_only_components.sort(key=lambda c: (-c['bounding_box_area'], c['bounding_box'][0], c['bounding_box'][1]))
            main_pattern = non_magenta_only_components[0]

        # Identify the marker (M)
        marker = None
        magenta_components = [
            comp for comp in all_components if magenta_color in comp['colors']
        ]
        if main_pattern and magenta_components:
            pattern_max_c = main_pattern['bounding_box'][3]
            relevant_markers = [
                m for m in magenta_components if m['bounding_box'][1] > pattern_max_c
            ]
            if relevant_markers:
                relevant_markers.sort(key=lambda c: (c['bounding_box'][0], c['bounding_box'][1]))
                marker = relevant_markers[0]

        # Perform the copy if both pattern and marker were found
        if main_pattern and marker:
            pattern_min_r, pattern_min_c, pattern_max_r, pattern_max_c = main_pattern['bounding_box']
            marker_min_r, marker_min_c, _, _ = marker['bounding_box']

            dest_row_start = marker_min_r + 2
            dest_col_start = marker_min_c

            pattern_height = pattern_max_r - pattern_min_r + 1
            pattern_width = pattern_max_c - pattern_min_c + 1

            for r_offset in range(pattern_height):
                for c_offset in range(pattern_width):
                    src_r = pattern_min_r + r_offset
                    src_c = pattern_min_c + c_offset
                    dest_r = dest_row_start + r_offset
                    dest_c = dest_col_start + c_offset

                    if 0 <= dest_r < height and 0 <= dest_c < width:
                        # Source coords should be valid if bbox is correct
                         if 0 <= src_r < height and 0 <= src_c < width:
                             output_grid[dest_r][dest_c] = input_grid[src_r][src_c]

    # Return the potentially modified grid
    return output_grid