import numpy as np
from collections import deque
import copy

"""
Identifies a unique composite object in the input grid, characterized by an outer shape of one color (Co) 
enclosing an inner shape of a different color (Ci). All other objects in the input are discarded.
This target object is duplicated, and the copy is placed adjacent to the original.

The placement direction (below or right) and the gap size between the original and the copy depend 
on the object's dimensions (Height H, Width W) and the values of the inner (Ci) and outer (Co) colors 
according to the following rules:

1.  **Placement Direction:**
    *   Place BELOW if the Inner Color (Ci) is less than the Outer Color (Co) AND the Outer Color (Co) is an integer multiple of the Inner Color (Ci) (i.e., Co % Ci == 0).
    *   Otherwise, place RIGHT.

2.  **Gap Size:**
    *   If Inner Color (Ci) > Outer Color (Co), Gap = abs(Ci - Co).
    *   Else if Outer Color (Co) == 2 * Inner Color (Ci), Gap = Height (H).
    *   Otherwise (i.e., Ci <= Co AND (Co != 2*Ci or Co % Ci != 0)), Gap = Inner Color (Ci).

The output grid size is determined dynamically to accommodate both the original object in its 
input position and the placed copy, ensuring it's at least as large as the input grid.
"""

def find_connected_components(grid):
    """Finds all connected components of non-zero cells using BFS."""
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    for r in range(rows):
        for c in range(cols):
            # Start BFS from an unvisited non-zero cell
            if grid[r, c] != 0 and not visited[r, c]:
                component_cells = set()
                q = deque([(r, c)])
                visited[r, c] = True
                component_cells.add((r, c))

                # Perform BFS to find all connected cells of the same object
                while q:
                    row, col = q.popleft()
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds and if the neighbor is non-zero and unvisited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] != 0 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            component_cells.add((nr, nc))
                
                # Add the found component (set of cell coordinates) to the list
                if component_cells:
                    components.append(component_cells)
    return components

def get_bounding_box(component_cells):
    """Calculates the bounding box (min_r, min_c, max_r, max_c) for a set of cells."""
    if not component_cells:
        return None
    # Find min/max row and column indices from the component's cells
    min_r = min(r for r, c in component_cells)
    min_c = min(c for r, c in component_cells)
    max_r = max(r for r, c in component_cells)
    max_c = max(c for r, c in component_cells)
    return min_r, min_c, max_r, max_c

def identify_inner_outer_colors(subgrid):
    """
    Identifies the inner (Ci) and outer (Co) colors within a subgrid representing a composite object.
    Assumes the subgrid contains exactly two non-zero colors.
    The outer color is determined by checking the pixels on the boundary of the subgrid.
    """
    height, width = subgrid.shape
    # Find the two distinct non-zero colors present
    colors = set(np.unique(subgrid[subgrid != 0]))
    if len(colors) != 2:
        # This function should only be called for subgrids known to have 2 colors
        return None, None 

    outer_color = None
    # Collect pixels from the boundary of the subgrid
    boundary_pixels = []
    if height > 0:
        boundary_pixels.extend(subgrid[0, :].tolist()) # Top row
        boundary_pixels.extend(subgrid[height-1, :].tolist()) # Bottom row
    if width > 0:
        boundary_pixels.extend(subgrid[:, 0].tolist()) # Left col
        boundary_pixels.extend(subgrid[:, width-1].tolist()) # Right col
        
    # Iterate through boundary pixels to find which of the two colors is the outer one
    for pixel_color in boundary_pixels:
        if pixel_color in colors:
            outer_color = pixel_color
            break # Found the outer color

    if outer_color is None:
         # Fallback: if no boundary pixel matches the object colors (e.g., very thin object 
         # or error in logic), assume the numerically larger color is outer. This is a heuristic.
         outer_color = max(colors)

    # The inner color is the one that's not the outer color
    inner_color = (colors - {outer_color}).pop()
    return inner_color, outer_color


def transform(input_grid_list):
    """
    Applies the transformation rule to the input grid list.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    rows, cols = input_grid.shape

    # Workflow Step 1: Find all connected components (objects)
    components = find_connected_components(input_grid)

    target_object_info = None

    # Workflow Step 2: Identify the target composite object
    for component in components:
        if not component: continue
        
        # Get the bounding box of the current component
        bbox = get_bounding_box(component)
        if bbox is None: continue
        r1, c1, r2, c2 = bbox

        # Extract the subgrid corresponding to the bounding box
        subgrid = input_grid[r1:r2+1, c1:c2+1]

        # Find unique non-zero colors within this bounding box
        unique_colors_in_bbox = set(np.unique(subgrid[subgrid != 0]))

        # Check if this is the target object (exactly two non-zero colors)
        if len(unique_colors_in_bbox) == 2:
            height = r2 - r1 + 1
            width = c2 - c1 + 1
            
            # Workflow Step 3: Identify Inner (Ci) and Outer (Co) colors
            Ci, Co = identify_inner_outer_colors(subgrid)
            if Ci is None or Co is None:
                 # Skip if colors couldn't be reliably determined
                continue 

            # Store information about the target object
            target_object_info = {
                 'bbox': bbox,
                 'inner_color': Ci,
                 'outer_color': Co,
                 'width': width,
                 'height': height,
                 'pattern': subgrid
             }
            # Assume there's only one target object per input grid
            break 

    # If no target object was found, return the input grid unchanged
    if target_object_info is None:
        return input_grid_list 

    # Extract properties for calculating placement and gap
    bbox = target_object_info['bbox']
    Ci = target_object_info['inner_color']
    Co = target_object_info['outer_color']
    W = target_object_info['width']
    H = target_object_info['height']
    r1, c1, r2, c2 = bbox
    object_pattern = target_object_info['pattern']

    # Workflow Step 4: Determine Placement Direction
    # Place BELOW if Ci < Co AND Co is a multiple of Ci. Otherwise RIGHT.
    place_below = (Ci < Co) and (Co % Ci == 0)

    # Workflow Step 5: Calculate Gap Size based on the rules
    if Ci > Co:
        gap = abs(Ci - Co)
    elif Co == 2 * Ci: # Check this specific condition before the general Ci <= Co case
        gap = H
    else: # Handles the remaining cases where Ci <= Co
        gap = Ci

    # Workflow Step 6: Calculate Copy Position
    if place_below:
        copy_r = r2 + 1 + gap  # Below original, add gap
        copy_c = c1            # Align horizontally
    else: # Place Right
        copy_r = r1            # Align vertically
        copy_c = c2 + 1 + gap  # Right of original, add gap

    # Workflow Step 7: Calculate Output Grid Size
    # Determine the maximum row and column needed to fit both original and copy
    required_rows = max(r1 + H, copy_r + H)
    required_cols = max(c1 + W, copy_c + W)
    
    # Ensure the output grid is at least as large as the input grid dimensions
    out_rows = max(rows, required_rows)
    out_cols = max(cols, required_cols)

    # Workflow Step 8: Construct Output Grid
    # Initialize the output grid with background color (0)
    output_grid = np.zeros((out_rows, out_cols), dtype=int)

    # Place the original target object pattern into the output grid
    # Use slicing that respects the calculated output grid boundaries
    orig_end_r = r1 + H
    orig_end_c = c1 + W
    output_grid[r1:orig_end_r, c1:orig_end_c] = object_pattern

    # Place the copied target object pattern into the output grid
    # Use slicing that respects the calculated output grid boundaries
    copy_end_r = copy_r + H
    copy_end_c = copy_c + W
    output_grid[copy_r:copy_end_r, copy_c:copy_end_c] = object_pattern

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()