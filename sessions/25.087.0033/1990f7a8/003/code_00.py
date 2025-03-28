import numpy as np
from collections import deque

"""
Transforms an input grid containing scattered red pixel patterns into a fixed 7x7 output grid by grouping fragments based on input grid quadrants.

The transformation involves:
1. Identifying all distinct 4-connected components (fragments) of red (2) pixels in the input grid.
2. Calculating the center of the input grid.
3. Assigning each identified red fragment to one of four input grid quadrants (Top-Left, Top-Right, Bottom-Left, Bottom-Right) based on the location of the fragment's bounding box center relative to the input grid center.
4. For each quadrant, determining the overall top-left corner (minimum row, minimum column) across all fragments assigned to that quadrant. This defines a reference point for the group.
5. Creating a 7x7 output grid initialized with white (0).
6. For each quadrant group:
    a. Iterating through all pixels of all fragments belonging to that group.
    b. Calculating each pixel's position relative to the group's overall top-left corner found in step 4.
    c. If the relative position falls within a 3x3 area (0<=row<3, 0<=col<3), placing a red pixel at the corresponding position within the target 3x3 quadrant in the output grid (TL -> rows 0-2, cols 0-2; TR -> rows 0-2, cols 4-6; BL -> rows 4-6, cols 0-2; BR -> rows 4-6, cols 4-6).
7. The central row (3) and column (3) of the output remain white.
"""

def _find_objects(grid, color):
    """Finds all connected components (fragments) of a given color in the grid using 4-connectivity."""
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            if grid[r, c] == color and not visited[r, c]:
                obj_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    row, col = q.popleft()
                    obj_pixels.append((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                # Store the fragment's pixels and its bounding box
                objects.append({
                    'pixels': obj_pixels,
                    'bbox': (min_r, min_c, max_r, max_c)
                })
    return objects

def _get_bbox_center(obj_bbox):
    """Calculates the center coordinates of a bounding box."""
    min_r, min_c, max_r, max_c = obj_bbox
    center_r = (min_r + max_r) / 2.0
    center_c = (min_c + max_c) / 2.0
    return center_r, center_c

def transform(input_grid_list):
    """
    Transforms the input grid according to the described rules.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    input_height, input_width = input_grid.shape
    red_color = 2
    background_color = 0
    output_size = 7
    quadrant_size = 3

    # 1. Initialize the output grid
    output_grid = np.full((output_size, output_size), background_color, dtype=int)

    # Define the target quadrant top-left corners in the output grid
    target_quadrants_output_origin = {
        "TL": (0, 0),
        "TR": (0, 4),
        "BL": (4, 0),
        "BR": (4, 4)
    }

    # 2. Identify all red fragments
    fragments = _find_objects(input_grid, red_color)

    # 3. Calculate input grid center
    grid_center_r = (input_height - 1) / 2.0
    grid_center_c = (input_width - 1) / 2.0

    # 4. Create structure to hold fragments assigned to each quadrant
    quadrant_fragments = {"TL": [], "TR": [], "BL": [], "BR": []}

    # 5. Assign fragments to quadrants based on their bbox center
    for frag in fragments:
        frag_center_r, frag_center_c = _get_bbox_center(frag['bbox'])

        if frag_center_r <= grid_center_r and frag_center_c <= grid_center_c:
            quadrant_fragments["TL"].append(frag)
        elif frag_center_r <= grid_center_r and frag_center_c > grid_center_c:
            quadrant_fragments["TR"].append(frag)
        elif frag_center_r > grid_center_r and frag_center_c <= grid_center_c:
            quadrant_fragments["BL"].append(frag)
        else: # frag_center_r > grid_center_r and frag_center_c > grid_center_c
            quadrant_fragments["BR"].append(frag)

    # 6. Process each quadrant group
    for quadrant, frags_in_quadrant in quadrant_fragments.items():
        if not frags_in_quadrant:
            continue # Skip if no fragments were assigned to this quadrant

        # 6.a. Find the overall top-left corner for this group of fragments
        min_r_group = input_height  # Initialize with max possible value
        min_c_group = input_width   # Initialize with max possible value
        for frag in frags_in_quadrant:
            min_r, min_c, _, _ = frag['bbox']
            min_r_group = min(min_r_group, min_r)
            min_c_group = min(min_c_group, min_c)

        # Get the output grid starting position for this quadrant
        out_r_start, out_c_start = target_quadrants_output_origin[quadrant]

        # 6.b-c. Place pixels relative to group origin into the output quadrant
        for frag in frags_in_quadrant:
            for r, c in frag['pixels']:
                # Calculate position relative to the group's origin
                rel_r = r - min_r_group
                rel_c = c - min_c_group

                # Check if the relative position is within the 3x3 target area
                if 0 <= rel_r < quadrant_size and 0 <= rel_c < quadrant_size:
                    # Calculate absolute position in the output grid
                    output_r = out_r_start + rel_r
                    output_c = out_c_start + rel_c
                    
                    # Set the pixel color (ensure it's within output bounds, though logic should prevent issues)
                    if 0 <= output_r < output_size and 0 <= output_c < output_size:
                         output_grid[output_r, output_c] = red_color

    # 7. Return the final grid
    return output_grid.tolist()