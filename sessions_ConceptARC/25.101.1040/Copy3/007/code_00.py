import copy
import collections
import numpy as np

"""
Transforms an input grid based on the presence or absence of magenta pixels (color 6).

Two distinct rules apply:

Rule 1: No Magenta Pixels Present
  - Precondition: The grid width `W` must be even.
  - Identifies all distinct connected components of non-white pixels located entirely within the left half of the grid (columns 0 to W/2 - 1).
  - For each pixel belonging to these left-half components, its value is copied to the corresponding position in the right half of the grid, shifted horizontally by W/2 columns.
  - The left half of the grid remains unchanged. Pixels in the right half not overwritten by copied component pixels remain unchanged.
  - If the grid width is odd, or if no non-white components are found in the left half, the grid remains unchanged.

Rule 2: Magenta Pixels Present
  - Finds all distinct non-white connected components in the entire grid.
  - Identifies the 'main pattern' (P): The non-magenta-only component with the largest bounding box area (ties broken by top-most, then left-most row/col).
  - Identifies the 'marker' (M): The magenta-containing component whose minimum column index is greater than the main pattern's maximum column index. Among candidates, selects the one with the minimum row index, then minimum column index (top-most, left-most).
  - Calculates a destination top-left corner based on the marker's position: `(marker_min_row + 2, marker_min_col)`.
  - Copies the entire rectangular region defined by the main pattern's (P) bounding box from the input grid to the calculated destination area in the output grid, overwriting existing pixels.
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
    
    # Define search boundaries
    if bounds:
        min_r_bound, min_c_bound, max_r_bound, max_c_bound = bounds
        # Clip bounds to grid dimensions
        min_r_bound = max(0, min_r_bound)
        min_c_bound = max(0, min_c_bound)
        max_r_bound = min(height - 1, max_r_bound)
        max_c_bound = min(width - 1, max_c_bound)
    else: # Default to full grid if no bounds provided
        min_r_bound, min_c_bound = 0, 0
        max_r_bound, max_c_bound = height - 1, width - 1

    visited = set()
    components = []
    component_id_counter = 0

    # Iterate through the search area
    for r in range(min_r_bound, max_r_bound + 1):
        for c in range(min_c_bound, max_c_bound + 1):
            # If a pixel is valid (not ignored, within bounds) and not visited, start BFS
            if grid_np[r, c] != ignore_color and (r, c) not in visited:
                component_id_counter += 1
                component_coords = set()
                component_colors = set()
                q = collections.deque([(r, c)])
                visited.add((r, c))
                # Track component properties during BFS
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    row, col = q.popleft()
                    component_coords.add((row, col))
                    # Use item() to ensure native Python int type
                    component_colors.add(grid_np[row, col].item()) 
                    # Update bounding box
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Explore neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        # Check if neighbor is valid: within grid, within search bounds, not ignored, not visited
                        if min_r_bound <= nr <= max_r_bound and min_c_bound <= nc <= max_c_bound and \
                           grid_np[nr, nc] != ignore_color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))

                # Store component information if it's not empty
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
    Applies the transformation rules based on magenta presence.
    """
    # Initialize output_grid as a deep copy to avoid modifying the input
    output_grid = copy.deepcopy(input_grid)
    grid_np = np.array(input_grid)
    height, width = grid_np.shape
    magenta_color = 6
    white_color = 0

    # Check for the presence of magenta pixels
    has_magenta = np.any(grid_np == magenta_color)

    if not has_magenta:
        # --- Rule 1: No Magenta ---
        # Apply rule only if width is even
        if width % 2 == 0:
            mid_col = width // 2
            # Define bounds for the left half of the grid
            left_bounds = (0, 0, height - 1, mid_col - 1)
            
            # Find non-white components strictly within the left half
            left_components = find_connected_components(input_grid, ignore_color=white_color, bounds=left_bounds)

            # Copy each pixel of each found component to the right half
            for component in left_components:
                for r_src, c_src in component['coords']:
                    # Calculate the destination column by shifting
                    c_dest = c_src + mid_col
                    # Ensure destination is within grid bounds before copying
                    if 0 <= r_src < height and 0 <= c_dest < width:
                        # Copy the pixel value
                        output_grid[r_src][c_dest] = input_grid[r_src][c_src]
        # If width is odd, do nothing (return the initial copy)

    else:
        # --- Rule 2: Magenta Present ---
        # Find all non-white components in the entire grid
        all_components = find_connected_components(input_grid, ignore_color=white_color)

        # Identify the 'main pattern' (P)
        main_pattern = None
        # Filter for components that are not purely magenta
        non_magenta_only_components = [
            comp for comp in all_components if not (comp['colors'] == {magenta_color})
        ]
        if non_magenta_only_components:
            # Sort by: 1. BBox Area (desc), 2. Min Row (asc), 3. Min Col (asc)
            non_magenta_only_components.sort(key=lambda c: (-c['bounding_box_area'], c['bounding_box'][0], c['bounding_box'][1]))
            main_pattern = non_magenta_only_components[0] # Select the top candidate

        # Identify the 'marker' (M)
        marker = None
        # Filter for components containing magenta
        magenta_components = [
            comp for comp in all_components if magenta_color in comp['colors']
        ]
        # Marker depends on main_pattern existing
        if main_pattern and magenta_components:
            pattern_max_c = main_pattern['bounding_box'][3] # Rightmost column of pattern P
            # Filter markers to those starting strictly to the right of the main pattern
            relevant_markers = [
                m for m in magenta_components if m['bounding_box'][1] > pattern_max_c
            ]
            if relevant_markers:
                # Sort relevant markers by: 1. Min Row (asc), 2. Min Col (asc)
                relevant_markers.sort(key=lambda c: (c['bounding_box'][0], c['bounding_box'][1]))
                marker = relevant_markers[0] # Select the top candidate

        # Perform the copy operation only if both pattern (P) and marker (M) were successfully identified
        if main_pattern and marker:
            # Get bounding box coordinates for the pattern
            pattern_min_r, pattern_min_c, pattern_max_r, pattern_max_c = main_pattern['bounding_box']
            # Get relevant coordinates for the marker
            marker_min_r, marker_min_c, _, _ = marker['bounding_box']

            # Calculate the top-left corner for the destination copy area
            dest_row_start = marker_min_r + 2
            dest_col_start = marker_min_c

            # Calculate dimensions of the pattern's bounding box
            pattern_height = pattern_max_r - pattern_min_r + 1
            pattern_width = pattern_max_c - pattern_min_c + 1

            # Iterate through the source bounding box region
            for r_offset in range(pattern_height):
                for c_offset in range(pattern_width):
                    # Calculate source coordinates within the input grid
                    src_r = pattern_min_r + r_offset
                    src_c = pattern_min_c + c_offset
                    # Calculate destination coordinates within the output grid
                    dest_r = dest_row_start + r_offset
                    dest_c = dest_col_start + c_offset

                    # Check if the destination coordinates are within the grid bounds
                    if 0 <= dest_r < height and 0 <= dest_c < width:
                        # Ensure source coords are valid (should be if bbox is correct)
                         if 0 <= src_r < height and 0 <= src_c < width:
                             # Copy the pixel value from input source to output destination
                             output_grid[dest_r][dest_c] = input_grid[src_r][src_c]
        # If P or M were not found, do nothing (return the initial copy)

    # Return the potentially modified grid
    return output_grid