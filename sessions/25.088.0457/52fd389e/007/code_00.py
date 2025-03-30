import numpy as np
from collections import deque

"""
Transformation Rule:
1. Initialize an output grid as an exact copy of the input grid.
2. Identify all distinct, contiguous groups of yellow (4) pixels in the input grid using 4-way adjacency (these are "yellow components"). For each component, determine its pixel coordinates and its minimal bounding box.
3. Analyze each yellow component:
    a. Find all pixels within the component's bounding box in the input grid that are *not* yellow (4) and *not* white (0). These are the "internal pixels".
    b. Check if any internal pixels were found.
    c. If internal pixels exist, check if they *all* share the same single color (the "inner color").
    d. If internal pixels exist and all share the same inner color, the component qualifies for a border. Calculate the border thickness (`T`) as the total number of internal pixels. Store the component's bounding box, original yellow pixel coordinates, the inner color, and the thickness `T`.
4. Draw borders for all qualifying components onto the output grid:
    a. For each qualifying component, calculate an expanded bounding box by extending its original bounding box outwards by thickness `T` in all directions (clamped to grid boundaries).
    b. Fill all pixels in the output grid that are within the expanded bounding box but *outside* the original bounding box with the component's inner color.
5. Preserve the original yellow pixels for all qualifying components:
    a. For each qualifying component, iterate through its original yellow pixel coordinates.
    b. Set the color of the corresponding pixel in the output grid back to yellow (4). This corrects any yellow pixels that might have been overwritten during border drawing.
6. Return the modified output grid.
"""

def find_yellow_components(grid):
    """
    Finds all connected components of yellow (4) pixels using 4-way adjacency.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents a
              yellow component and contains:
              - 'coords': A set of (row, col) tuples for the yellow pixels.
              - 'bbox': A tuple (min_r, min_c, max_r, max_c) representing
                        the bounding box of the component.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []
    yellow_color = 4

    for r in range(height):
        for c in range(width):
            if grid[r, c] == yellow_color and not visited[r, c]:
                component_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c, max_r, max_c = r, c, r, c

                while q:
                    row, col = q.popleft()
                    component_coords.add((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == yellow_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                if component_coords:
                    components.append({
                        'coords': component_coords,
                        'bbox': (min_r, min_c, max_r, max_c)
                    })
    return components

def find_internal_pixels_within_bbox(grid, bbox):
    """
    Finds pixels strictly inside the bbox that are not yellow (4) or white (0).

    Args:
        grid (np.array): The input grid.
        bbox (tuple): The bounding box (min_r, min_c, max_r, max_c).

    Returns:
        list: A list of dictionaries, each containing:
              - 'coord': (row, col) tuple of the internal pixel.
              - 'color': The color of the internal pixel.
    """
    min_r, min_c, max_r, max_c = bbox
    internal_pixels = []
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            color = grid[r, c]
            # Rule 3a: internal pixels are NOT yellow (4) and NOT white (0)
            if color != 4 and color != 0:
                internal_pixels.append({'coord': (r, c), 'color': color})
    return internal_pixels

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    # Step 1: Initialize output grid as a copy of the input
    output_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape

    # Step 2: Identify yellow components and their bounding boxes
    yellow_components = find_yellow_components(input_grid_np)

    qualifying_components = []

    # Step 3: Analyze each yellow component
    for component in yellow_components:
        bbox = component['bbox']
        yellow_coords = component['coords'] # Need original coords for step 5

        # Step 3a: Find internal pixels within this bounding box
        internal_pixels = find_internal_pixels_within_bbox(input_grid_np, bbox)

        # Step 3b & 3c: Check border conditions
        if not internal_pixels:
            continue # No internal pixels

        first_inner_color = internal_pixels[0]['color']
        all_same_color = all(p['color'] == first_inner_color for p in internal_pixels)

        if not all_same_color:
            continue # Internal pixels exist but have different colors

        # Step 3d: Qualify for border and calculate properties
        inner_color = first_inner_color
        thickness_t = len(internal_pixels)

        qualifying_components.append({
            'bbox': bbox,
            'inner_color': inner_color,
            'thickness': thickness_t,
            'yellow_coords': yellow_coords # Store original yellow coords
        })

    # Step 4: Draw borders for qualifying components
    for qc in qualifying_components:
        min_r, min_c, max_r, max_c = qc['bbox']
        inner_color = qc['inner_color']
        thickness = qc['thickness']

        # Step 4a: Calculate expanded bounding box coordinates
        exp_min_r = max(0, min_r - thickness)
        exp_min_c = max(0, min_c - thickness)
        exp_max_r = min(height - 1, max_r + thickness)
        exp_max_c = min(width - 1, max_c + thickness)

        # Step 4b: Fill border area
        for r in range(exp_min_r, exp_max_r + 1):
            for c in range(exp_min_c, exp_max_c + 1):
                # Check if the pixel (r, c) is outside the original bounding box
                is_outside_original_bbox = (r < min_r or r > max_r or c < min_c or c > max_c)
                if is_outside_original_bbox:
                    # Check bounds again just to be safe, though clamping should handle it
                    if 0 <= r < height and 0 <= c < width:
                         output_grid_np[r, c] = inner_color

    # Step 5: Preserve original yellow pixels for qualifying components
    for qc in qualifying_components:
        yellow_coords = qc['yellow_coords']
        for r, c in yellow_coords:
            # Check bounds just in case, though coords should be valid
            if 0 <= r < height and 0 <= c < width:
                 output_grid_np[r, c] = 4 # Set back to yellow

    # Step 6: Return the modified grid
    return output_grid_np.tolist()