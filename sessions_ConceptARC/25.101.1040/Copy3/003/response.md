```python
import copy
import collections
import numpy as np

"""
Transforms an input grid based on the presence or absence of magenta pixels (color 6).

Rule 1: If no magenta pixels are present:
- Find all distinct non-white connected components in the left half of the grid.
- For each component found, copy its pixels to the corresponding positions in the right half of the grid, shifted horizontally by half the grid width.
- Assumes the grid width is even.

Rule 2: If magenta pixels are present:
- Find all distinct non-white connected components in the entire grid.
- Identify the 'main pattern' (P): The non-magenta-only component with the largest bounding box area (ties broken by top-most, then left-most).
- Identify the 'marker' (M): The magenta-containing component starting furthest to the right of P, prioritizing the top-most, then left-most among candidates.
- Calculate a destination top-left corner based on the marker's position (marker_row + 2, marker_col).
- Copy the entire rectangular region defined by the main pattern's bounding box from the input grid to the calculated destination in the output grid.
- If either the main pattern or the marker cannot be identified according to the rules, no copy operation is performed for this case.
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
        A list of dictionaries, where each dictionary represents a component and contains:
        - 'id': A unique identifier for the component.
        - 'coords': A set of (row, col) tuples belonging to the component.
        - 'colors': A set of color values present in the component.
        - 'bounding_box': A tuple (min_row, min_col, max_row, max_col).
        - 'bounding_box_area': The area of the bounding box.
        - 'pixel_count': The number of pixels in the component.
    """
    grid_np = np.array(grid)
    height, width = grid_np.shape
    
    if bounds:
        min_r_bound, min_c_bound, max_r_bound, max_c_bound = bounds
        # Ensure bounds are within grid dimensions
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
            # Start a new component search if the pixel is within bounds, not ignored, and not visited
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

                    # Process the current pixel (already checked it's valid and within bounds)
                    component_coords.add((row, col))
                    component_colors.add(grid_np[row, col])
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Explore neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        # Check if neighbor is within grid boundaries AND specified search bounds
                        if min_r_bound <= nr <= max_r_bound and min_c_bound <= nc <= max_c_bound and \
                           grid_np[nr, nc] != ignore_color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))

                # Only add component if it has coordinates (should always be true if started)
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


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the presence or absence of magenta pixels.
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
        # Assume width is even for this rule based on examples
        if width % 2 == 0:
            mid_col = width // 2
            # Define bounds for the left half
            left_bounds = (0, 0, height - 1, mid_col - 1)
            # Find components only within the left half
            left_components = find_connected_components(input_grid, ignore_color=white_color, bounds=left_bounds)

            # Copy each component found to the right half
            for component in left_components:
                for r_src, c_src in component['coords']:
                    # Calculate destination column
                    c_dest = c_src + mid_col
                    # Copy pixel if destination is within grid bounds (should be if width is even)
                    if 0 <= r_src < height and 0 <= c_dest < width:
                        output_grid[r_src][c_dest] = input_grid[r_src][c_src]
        # If width is odd and no magenta, do nothing (based on lack of examples)

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
            # Sort by: 1. BBox Area (desc), 2. Min Row (asc), 3. Min Col (asc)
            non_magenta_only_components.sort(key=lambda c: (-c['bounding_box_area'], c['bounding_box'][0], c['bounding_box'][1]))
            main_pattern = non_magenta_only_components[0]

        # Identify the marker (M)
        marker = None
        magenta_components = [
            comp for comp in all_components if magenta_color in comp['colors']
        ]
        if main_pattern and magenta_components:
            pattern_max_c = main_pattern['bounding_box'][3]
            # Filter markers to those starting to the right of the main pattern
            relevant_markers = [
                m for m in magenta_components if m['bounding_box'][1] > pattern_max_c
            ]
            if relevant_markers:
                # Sort by: 1. Min Row (asc), 2. Min Col (asc)
                relevant_markers.sort(key=lambda c: (c['bounding_box'][0], c['bounding_box'][1]))
                marker = relevant_markers[0]

        # Perform the copy if both pattern and marker were found
        if main_pattern and marker:
            pattern_min_r, pattern_min_c, pattern_max_r, pattern_max_c = main_pattern['bounding_box']
            marker_min_r, marker_min_c, _, _ = marker['bounding_box']

            # Calculate destination top-left corner
            dest_row_start = marker_min_r + 2
            dest_col_start = marker_min_c

            # Copy the *bounding box* content of the main pattern
            pattern_height = pattern_max_r - pattern_min_r + 1
            pattern_width = pattern_max_c - pattern_min_c + 1

            for r_offset in range(pattern_height):
                for c_offset in range(pattern_width):
                    src_r = pattern_min_r + r_offset
                    src_c = pattern_min_c + c_offset
                    dest_r = dest_row_start + r_offset
                    dest_c = dest_col_start + c_offset

                    # Ensure source is valid (it should be) and destination is within grid bounds
                    if 0 <= dest_r < height and 0 <= dest_c < width:
                         # Check source is valid just in case bbox extends beyond grid (shouldn't happen with correct find_components)
                        if 0 <= src_r < height and 0 <= src_c < width:
                             output_grid[dest_r][dest_c] = input_grid[src_r][src_c]

    # Return the modified grid
    return output_grid
```