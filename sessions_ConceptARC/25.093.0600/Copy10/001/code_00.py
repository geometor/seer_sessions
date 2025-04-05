import numpy as np
from collections import deque

"""
Identifies a composite object (an outer shape enclosing an inner shape of a different color) in the input grid.
Duplicates this object and places the copy adjacent to the original.
The gap between the original and the copy is determined by the color of the inner shape.
The placement direction (right or below) depends on the object's aspect ratio (width vs. height).
All other objects in the input are discarded. The output grid size is adjusted to fit the original and the copy.

Workflow:
1. Find all connected components (objects) of non-zero cells in the input grid.
2. Identify the 'target' object: the one whose bounding box contains exactly two distinct non-zero colors.
3. Determine the properties of the target object: bounding box, width, height, and the two colors.
4. Identify the 'inner' color (the minimum of the two non-zero colors).
5. Calculate the gap size between the original and copy (gap = inner_color).
6. Determine the placement direction: 'right' if width >= height, 'below' otherwise.
7. Calculate the top-left coordinates for the copied object based on direction and gap.
8. Extract the pattern (subgrid) of the target object from the input.
9. Determine the required dimensions for the output grid to hold the original and the copy.
10. Create the output grid, initialized with zeros.
11. Place the original object pattern into the output grid.
12. Place the copied object pattern into the output grid at the calculated position.
13. Return the output grid.
"""

def find_connected_components(grid):
    """Finds all connected components of non-zero cells."""
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                component_cells = set()
                q = deque([(r, c)])
                visited[r, c] = True
                component_cells.add((r, c))

                while q:
                    row, col = q.popleft()
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] != 0 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            component_cells.add((nr, nc))
                components.append(component_cells)
    return components

def get_bounding_box(component_cells):
    """Calculates the bounding box (min_r, min_c, max_r, max_c) for a component."""
    if not component_cells:
        return None
    min_r = min(r for r, c in component_cells)
    min_c = min(c for r, c in component_cells)
    max_r = max(r for r, c in component_cells)
    max_c = max(c for r, c in component_cells)
    return min_r, min_c, max_r, max_c

def transform(input_grid_list):
    """
    Transforms the input grid according to the specified object duplication rule.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    rows, cols = input_grid.shape

    # 1. Find all connected components
    components = find_connected_components(input_grid)

    target_object_info = None

    # 2. Identify the 'target' object
    for component in components:
        if not component: continue
        bbox = get_bounding_box(component)
        if bbox is None: continue
        r1, c1, r2, c2 = bbox
        
        # Extract subgrid based on bounding box
        subgrid = input_grid[r1:r2+1, c1:c2+1]
        
        # Find unique non-zero colors within the *bounding box*
        unique_colors_in_bbox = set(subgrid[subgrid != 0].flatten())

        # Target object has exactly two distinct non-zero colors in its bounding box
        if len(unique_colors_in_bbox) == 2:
             width = c2 - c1 + 1
             height = r2 - r1 + 1
             target_object_info = {
                 'bbox': bbox,
                 'colors': list(unique_colors_in_bbox),
                 'width': width,
                 'height': height
             }
             break # Assume only one such object

    if target_object_info is None:
        # Handle cases where no target object is found (e.g., return original or empty)
        # For this problem, examples suggest a target always exists.
        # If not, returning the original grid might be a safe default.
        print("Warning: No target object found.")
        return input_grid_list 

    # 3. Determine properties of the target object
    bbox = target_object_info['bbox']
    colors = target_object_info['colors']
    width = target_object_info['width']
    height = target_object_info['height']
    r1, c1, r2, c2 = bbox

    # 4. Identify the 'inner' color (minimum of the two non-zero colors)
    inner_color = min(colors)

    # 5. Calculate the gap size
    gap = inner_color

    # 6. Determine placement direction
    if height > width:
        placement_direction = 'below'
    else: # width >= height
        placement_direction = 'right'

    # 7. Calculate the top-left coordinates for the copy
    if placement_direction == 'below':
        r_copy = r2 + 1 + gap
        c_copy = c1
        # 9. Determine the required dimensions for the output grid
        out_rows = r_copy + height
        out_cols = max(cols, c1 + width) # Ensure width accommodates original
    else: # placement_direction == 'right'
        r_copy = r1
        c_copy = c2 + 1 + gap
        # 9. Determine the required dimensions for the output grid
        out_rows = max(rows, r1 + height) # Ensure height accommodates original
        out_cols = c_copy + width

    # 8. Extract the pattern (subgrid) of the target object
    object_pattern = input_grid[r1:r2+1, c1:c2+1]

    # 10. Create the output grid, initialized with zeros
    output_grid = np.zeros((out_rows, out_cols), dtype=int)

    # 11. Place the original object pattern into the output grid
    output_grid[r1:r1+height, c1:c1+width] = object_pattern

    # 12. Place the copied object pattern into the output grid
    output_grid[r_copy:r_copy+height, c_copy:c_copy+width] = object_pattern

    # Convert back to list of lists for the required output format
    return output_grid.tolist()