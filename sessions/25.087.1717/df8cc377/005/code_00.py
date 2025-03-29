import numpy as np
from collections import deque

"""
Identify all hollow rectangular border objects in the input grid. For each 
rectangle, find any single marker pixel object located strictly within that 
rectangle's interior boundaries. If such a marker is found for a rectangle, 
fill the entire interior area defined by that rectangle's bounding box 
(excluding the border pixels) with the color of the marker pixel. The 
rectangle borders themselves and pixels outside any identified rectangle remain 
unchanged. If multiple rectangle-marker pairs exist, apply the transformation 
to all of them independently.
"""

def find_connected_components(grid):
    """
    Finds all connected components of non-background (non-zero) pixels using
    4-way (cardinal) connectivity.

    Args:
        grid (np.array): Input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents a
              component and contains:
              'pixels': set of (row, col) tuples for the component's pixels.
              'color': the color of the component.
              'bbox': tuple (min_row, min_col, max_row, max_col).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    for r in range(rows):
        for c in range(cols):
            # Start BFS from an unvisited non-background pixel
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                component_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                # Breadth-First Search
                while q:
                    row, col = q.popleft()
                    component_pixels.add((row, col))
                    # Update bounding box
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check 4 cardinal neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds, color match, and visited status
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                # Store the found component
                components.append({
                    'pixels': component_pixels,
                    'color': color,
                    'bbox': (min_r, min_c, max_r, max_c)
                })
    return components

def is_hollow_rectangle(component):
    """
    Checks if a component forms a hollow rectangle border based on its
    pixels and bounding box.

    Args:
        component (dict): A component dictionary from find_connected_components.

    Returns:
        bool: True if the component is a hollow rectangle border, False otherwise.
    """
    pixels = component['pixels']
    min_r, min_c, max_r, max_c = component['bbox']

    height = max_r - min_r + 1
    width = max_c - min_c + 1

    # Basic dimension check: must be at least 3x3 to have an interior.
    if width < 3 or height < 3:
        return False

    # Check if the number of pixels matches the expected perimeter length.
    # Perimeter = 2 * width + 2 * height - 4 (subtract corners counted twice)
    expected_perimeter = 2 * width + 2 * height - 4
    if len(pixels) != expected_perimeter:
        return False

    # Check if all component pixels lie exactly on the bounding box border.
    for r_pix, c_pix in pixels:
        is_on_border = (r_pix == min_r or r_pix == max_r or
                        c_pix == min_c or c_pix == max_c)
        if not is_on_border:
            return False # Pixel found strictly inside the border

    # Verify that all border positions defined by the bbox contain a pixel
    # from the component. This ensures there are no gaps in the border.
    # This check adds robustness, though potentially redundant with the others.
    for r in range(min_r, max_r + 1):
        if (r, min_c) not in pixels or (r, max_c) not in pixels:
            return False # Gap in vertical sides
    for c in range(min_c + 1, max_c): # Avoid rechecking corners
         if (min_r, c) not in pixels or (max_r, c) not in pixels:
            return False # Gap in horizontal sides

    # If all checks pass, it's likely a hollow rectangle border.
    return True


def transform(input_grid):
    """
    Transforms the input grid by finding all hollow rectangles and associated 
    internal single-pixel markers, then filling each rectangle's interior with 
    its corresponding marker's color.

    Args:
        input_grid (list): A list of lists representing the input grid.

    Returns:
        list: A list of lists representing the transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np) # Start with a copy of the input

    # 1. Find all connected components in the input grid
    components = find_connected_components(input_np)

    rectangles = []
    markers = []

    # 2. Classify components into potential rectangles and markers
    for comp in components:
        if len(comp['pixels']) == 1:
            # Single pixel component - potential marker
            markers.append(comp)
        elif len(comp['pixels']) > 1:
            # Check if it's a hollow rectangle
            if is_hollow_rectangle(comp):
                rectangles.append(comp)

    # 3. Iterate through each identified hollow rectangle
    for rect in rectangles:
        min_r, min_c, max_r, max_c = rect['bbox']
        interior_marker = None

        # 4. Search for a single-pixel marker strictly inside this rectangle
        for marker in markers:
            # Get the coordinate of the single pixel marker
            marker_coord = list(marker['pixels'])[0]
            marker_r, marker_c = marker_coord

            # Check if the marker is strictly within the rectangle bounds
            if (min_r < marker_r < max_r) and (min_c < marker_c < max_c):
                # Found a marker strictly inside.
                # If multiple markers exist inside, we'll use the first one found.
                # Based on examples, seems only one relevant marker per rectangle.
                if interior_marker is None:
                    interior_marker = marker
                # else: handle multiple markers if needed, currently takes the first

        # 5. Fill the interior if a valid marker was found inside this rectangle
        if interior_marker is not None:
            fill_color = interior_marker['color']

            # Iterate through the *strict* interior coordinates of the rectangle
            for r in range(min_r + 1, max_r):
                for c in range(min_c + 1, max_c):
                    # Fill every pixel in the strict interior with the marker's color
                    # This modifies the output grid directly.
                    output_np[r, c] = fill_color
            
            # Optionally remove the used marker from the list to avoid reuse if needed,
            # but current logic allows markers outside rectangles to persist.
            # Example 1 has outside markers remaining.

    # 6. Return the modified grid as a list of lists
    return output_np.tolist()