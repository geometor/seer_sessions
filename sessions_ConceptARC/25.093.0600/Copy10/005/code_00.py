import numpy as np
from collections import deque
import copy

"""
Identifies a unique composite object in the input grid, characterized by an outer shape of one color (Co) enclosing an inner shape of a different color (Ci).
All other objects in the input are discarded.
This target object is duplicated, and the copy is placed adjacent to the original.
The placement direction (below or right) and the gap size between the original and the copy depend on the object's dimensions (Height H, Width W) and the values of the inner (Ci) and outer (Co) colors according to the following rules:

1.  **Placement Direction:**
    *   Place BELOW if Height (H) > Width (W) OR if the Outer Color (Co) is exactly twice the Inner Color (Ci) (Co == 2 * Ci).
    *   Otherwise, place RIGHT.

2.  **Gap Size:**
    *   If Inner Color (Ci) > Outer Color (Co), Gap = abs(Ci - Co).
    *   Else if Outer Color (Co) == 2 * Inner Color (Ci), Gap = Height (H).
    *   Otherwise (Ci <= Co and Co != 2 * Ci), Gap = Inner Color (Ci).

The output grid size is determined dynamically to accommodate both the original object in its input position and the placed copy.
"""

def find_connected_components(grid):
    """Finds all connected components of non-zero cells using BFS."""
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
                
                if component_cells:
                    components.append(component_cells)
    return components

def get_bounding_box(component_cells):
    """Calculates the bounding box (min_r, min_c, max_r, max_c) for a set of cells."""
    if not component_cells:
        return None
    min_r = min(r for r, c in component_cells)
    min_c = min(c for r, c in component_cells)
    max_r = max(r for r, c in component_cells)
    max_c = max(c for r, c in component_cells)
    return min_r, min_c, max_r, max_c

def identify_inner_outer_colors(subgrid):
    """Identifies the inner (Ci) and outer (Co) colors within a subgrid."""
    height, width = subgrid.shape
    colors = set(np.unique(subgrid[subgrid != 0]))
    if len(colors) != 2:
        return None, None # Should not happen for target object

    outer_color = None
    # Check boundary pixels of the subgrid
    boundary_pixels = []
    if height > 0:
        boundary_pixels.extend(subgrid[0, :].tolist()) # Top row
        boundary_pixels.extend(subgrid[height-1, :].tolist()) # Bottom row
    if width > 0:
        boundary_pixels.extend(subgrid[:, 0].tolist()) # Left col
        boundary_pixels.extend(subgrid[:, width-1].tolist()) # Right col
        
    for pixel_color in boundary_pixels:
        if pixel_color in colors:
            outer_color = pixel_color
            break

    if outer_color is None:
         # Fallback or error: If no boundary pixel has one of the two colors,
         # this indicates an issue or a very thin object.
         # Let's make an assumption or raise error. Assume the larger color is outer?
         # Or maybe the color covering more area? Let's stick to boundary for now.
         # If boundary doesn't work, maybe check corners?
         # A simpler assumption might be needed if boundary fails.
         # Let's assume the numerically larger color is outer if boundary fails.
         # print("Warning: Could not determine outer color from boundary pixels. Assuming numerically larger.")
         outer_color = max(colors)


    inner_color = (colors - {outer_color}).pop()
    return inner_color, outer_color


def transform(input_grid_list):
    """
    Applies the transformation rule to the input grid.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    rows, cols = input_grid.shape

    # 1. Find all connected components
    components = find_connected_components(input_grid)

    target_object_info = None

    # 2. Identify the 'target' object (composite object with 2 colors)
    for component in components:
        if not component: continue
        
        bbox = get_bounding_box(component)
        if bbox is None: continue
        r1, c1, r2, c2 = bbox

        # Extract subgrid based on the component's bounding box
        subgrid = input_grid[r1:r2+1, c1:c2+1]

        # Find unique non-zero colors *within the component's bounding box*
        unique_colors_in_bbox = set(np.unique(subgrid[subgrid != 0]))

        # Target object has exactly two distinct non-zero colors in its bounding box
        if len(unique_colors_in_bbox) == 2:
            height = r2 - r1 + 1
            width = c2 - c1 + 1
            
            # 3. Identify Inner (Ci) and Outer (Co) colors
            Ci, Co = identify_inner_outer_colors(subgrid)
            if Ci is None or Co is None:
                continue # Skip if colors couldn't be determined

            target_object_info = {
                 'bbox': bbox,
                 'inner_color': Ci,
                 'outer_color': Co,
                 'width': width,
                 'height': height,
                 'pattern': subgrid
             }
            break # Assume only one such object per input

    if target_object_info is None:
        # If no target object found, return the input unchanged (as per some ARC tasks)
        # Or handle as an error, depending on expected behavior.
        # print("Warning: No target object found matching criteria.")
        return input_grid_list 

    # Extract properties for calculation
    bbox = target_object_info['bbox']
    Ci = target_object_info['inner_color']
    Co = target_object_info['outer_color']
    W = target_object_info['width']
    H = target_object_info['height']
    r1, c1, r2, c2 = bbox
    object_pattern = target_object_info['pattern']

    # 4. Determine Placement Direction
    place_below = (H > W) or (Co == 2 * Ci)

    # 5. Calculate Gap Size
    if Ci > Co:
        gap = abs(Ci - Co)
    elif Co == 2 * Ci:
        gap = H
    else: # Ci <= Co and Co != 2 * Ci
        gap = Ci

    # 6. Calculate Copy Position
    if place_below:
        placement_direction = 'below'
        copy_r = r2 + 1 + gap
        copy_c = c1
    else:
        placement_direction = 'right'
        copy_r = r1
        copy_c = c2 + 1 + gap

    # 7. Calculate Output Grid Size
    # Max row needed considers original position and copy position
    required_rows = max(r1 + H, copy_r + H)
    # Max col needed considers original position and copy position
    required_cols = max(c1 + W, copy_c + W)
    
    # Output grid should be at least as large as input, and large enough for content
    out_rows = max(rows, required_rows)
    out_cols = max(cols, required_cols)

    # 8. Construct Output Grid
    # Initialize with zeros (background color)
    output_grid = np.zeros((out_rows, out_cols), dtype=int)

    # Place the original target object pattern
    # Ensure slicing does not go out of bounds of the output grid
    orig_end_r = min(r1 + H, out_rows)
    orig_end_c = min(c1 + W, out_cols)
    output_grid[r1:orig_end_r, c1:orig_end_c] = object_pattern[:orig_end_r-r1, :orig_end_c-c1]

    # Place the copied target object pattern
    # Ensure slicing does not go out of bounds of the output grid
    copy_end_r = min(copy_r + H, out_rows)
    copy_end_c = min(copy_c + W, out_cols)
    output_grid[copy_r:copy_end_r, copy_c:copy_end_c] = object_pattern[:copy_end_r-copy_r, :copy_end_c-copy_c]

    # Convert back to list of lists for the required output format
    return output_grid.tolist()