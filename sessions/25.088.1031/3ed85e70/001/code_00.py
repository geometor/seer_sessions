import numpy as np
from collections import deque

"""
Identify template patterns in the upper green-background region (rows 0-6).
Identify fragment objects (contiguous blocks of a single non-white color) in the lower white-background region (rows 7-29).
For each fragment in the lower region, check if its color matches the outer border color of any template found in the upper region.
If a match is found, replace the area in the output grid starting at the fragment's top-left corner with the complete pattern of the matching template.
The upper region (rows 0-6) remains unchanged from input to output.
"""

def find_connected_components(grid, start_r, start_c, target_color, visited):
    """Finds a connected component of a specific color using BFS."""
    rows, cols = grid.shape
    q = deque([(start_r, start_c)])
    component_pixels = set()
    visited[start_r, start_c] = True
    min_r, min_c = start_r, start_c
    max_r, max_c = start_r, start_c

    while q:
        r, c = q.popleft()
        component_pixels.add((r, c))
        min_r = min(min_r, r)
        min_c = min(min_c, c)
        max_r = max(max_r, r)
        max_c = max(max_c, c)

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # 4-way connectivity
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and \
               not visited[nr, nc] and grid[nr, nc] == target_color:
                visited[nr, nc] = True
                q.append((nr, nc))
                
    return component_pixels, (min_r, min_c, max_r, max_c)

def find_template_components(grid, start_r, start_c, background_color, visited):
    """Finds a connected component of non-background colors using BFS."""
    rows, cols = grid.shape
    q = deque([(start_r, start_c)])
    component_pixels = set()
    visited[start_r, start_c] = True
    min_r, min_c = start_r, start_c
    max_r, max_c = start_r, start_c
    
    border_pixels = set() # Pixels adjacent to the background

    while q:
        r, c = q.popleft()
        component_pixels.add((r, c))
        min_r = min(min_r, r)
        min_c = min(min_c, c)
        max_r = max(max_r, r)
        max_c = max(max_c, c)
        
        is_border = False
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]: # 8-way adjacency check for border
            nr, nc = r + dr, c + dc
            # Check if adjacent pixel is background
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == background_color:
                 is_border = True
            # Check neighbors for component continuation (4-way)
            if abs(dr) + abs(dc) == 1: # Only consider 4-way neighbors for component growth
                if 0 <= nr < nc < cols and \
                   not visited[nr, nc] and grid[nr, nc] != background_color:
                    visited[nr, nc] = True
                    q.append((nr, nc))

        if is_border:
             border_pixels.add((r, c))
             
    # Determine the primary border color (assuming it's uniform or taking one example)
    border_color = -1 # Default if no border found / single pixel component not touching background
    if border_pixels:
        # Simple approach: take color of one border pixel
        br, bc = next(iter(border_pixels))
        border_color = grid[br, bc]
        # # More robust: find most frequent color among border pixels (if needed)
        # border_colors = [grid[r, c] for r, c in border_pixels]
        # if border_colors:
        #     counts = np.bincount(border_colors)
        #     border_color = np.argmax(counts)

    return component_pixels, border_color, (min_r, min_c, max_r, max_c)


def transform(input_grid_list):
    """
    Transforms the input grid based on template matching.

    1. Identifies templates (non-green shapes) in the upper region (rows 0-6). Stores their
       outer border color and the rectangular pattern containing the shape.
    2. Identifies fragments (non-white shapes) in the lower region (rows 7-end). Stores their
       color and top-left position.
    3. Creates a copy of the input grid.
    4. Iterates through fragments. If a fragment's color matches a template's border color,
       pastes the template's pattern onto the output grid at the fragment's top-left position.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # --- 1. Identify Templates (Upper Region: Rows 0-6) ---
    template_map = {} # Maps border_color -> pattern_array
    upper_region = input_grid[0:7, :]
    upper_rows, upper_cols = upper_region.shape
    visited_upper = np.zeros_like(upper_region, dtype=bool)
    template_background_color = 3 # green

    for r in range(upper_rows):
        for c in range(upper_cols):
            if upper_region[r, c] != template_background_color and not visited_upper[r, c]:
                component_pixels, border_color, bbox = find_template_components(upper_region, r, c, template_background_color, visited_upper)
                
                if border_color != -1: # Found a valid template with a border
                    min_r, min_c, max_r, max_c = bbox
                    # Extract the pattern as the rectangular bounding box of the component
                    pattern = upper_region[min_r:max_r+1, min_c:max_c+1]
                    
                    # Check if this border color is already mapped, maybe prioritize larger patterns?
                    # For now, simply overwrite if encountered again.
                    template_map[border_color] = pattern
                    
                    # Mark component as visited (redundant as find_template_components updates visited_upper)
                    # for pr, pc in component_pixels:
                    #      visited_upper[pr, pc] = True # Ensure component pixels are marked


    # --- 2. Identify Fragments (Lower Region: Rows 7 onwards) ---
    fragments = [] # List of (color, top_left_coord (r,c))
    lower_region_start_row = 7
    if rows <= lower_region_start_row: # Handle case where grid is too small
         return output_grid.tolist() 
         
    lower_region = input_grid[lower_region_start_row:, :]
    lower_rows, lower_cols = lower_region.shape
    visited_lower = np.zeros_like(lower_region, dtype=bool)
    fragment_background_color = 0 # white

    for r in range(lower_rows):
        for c in range(lower_cols):
            if lower_region[r, c] != fragment_background_color and not visited_lower[r, c]:
                frag_color = lower_region[r, c]
                # Find the component using the fragment's specific color
                component_pixels, bbox = find_connected_components(lower_region, r, c, frag_color, visited_lower)
                
                min_r, min_c, _, _ = bbox
                # Store fragment color and its top-left relative to the lower region
                # Adjust top-left coordinate to be relative to the *full* grid
                fragments.append((frag_color, (min_r + lower_region_start_row, min_c)))


    # Sort fragments by top-left coordinate (row then column) for deterministic pasting
    fragments.sort(key=lambda x: x[1])

    # --- 3. & 4. Apply Transformations ---
    for frag_color, (r_anchor, c_anchor) in fragments:
        if frag_color in template_map:
            pattern_array = template_map[frag_color]
            h, w = pattern_array.shape

            # Define target slice boundaries
            r_end = r_anchor + h
            c_end = c_anchor + w

            # Check if the pattern fits within the grid boundaries
            if r_end <= rows and c_end <= cols:
                # Paste the pattern onto the output grid
                output_grid[r_anchor:r_end, c_anchor:c_end] = pattern_array

    return output_grid.tolist()