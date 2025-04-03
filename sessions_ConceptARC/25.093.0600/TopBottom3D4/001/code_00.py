import numpy as np
from collections import deque

"""
Identify connected components (shapes) of non-zero values in the input grid.
Check for horizontal adjacencies between cells of different non-zero values.
If two adjacent cells (r, c) and (r, c+1) have values V1 and V2 (both > 0, V1 != V2), 
identify the shape associated with the minimum value (min(V1, V2)).
Mark this minimum-value shape for a leftward shift (move one column to the left).
Apply all identified shifts simultaneously: 
  - First, clear the original positions of all shifting shapes in the output grid.
  - Second, fill the new, left-shifted positions of all shifting shapes in the output grid, overwriting existing values.
Shapes not marked for shifting remain in place unless overwritten by a shifting shape.
"""

def _find_shapes(grid):
    """
    Identifies all connected components (shapes) of non-zero values using BFS.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A tuple containing:
        - shapes: A dictionary mapping shape_id to {'value': int, 'cells': set((r, c))}.
        - cell_to_shape_id: A numpy array of the same shape as grid, where each cell 
                           contains the shape_id it belongs to, or -1 if background (0).
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    cell_to_shape_id = np.full((rows, cols), -1, dtype=int)
    shapes = {}
    shape_id_counter = 0

    for r in range(rows):
        for c in range(cols):
            # If the cell is non-zero and not visited yet, start a BFS
            if grid[r, c] != 0 and not visited[r, c]:
                value = grid[r, c]
                current_shape_id = shape_id_counter
                shapes[current_shape_id] = {'value': value, 'cells': set()}
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    row, col = q.popleft()
                    # Add cell to the current shape
                    shapes[current_shape_id]['cells'].add((row, col))
                    cell_to_shape_id[row, col] = current_shape_id

                    # Explore 4-directional neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check boundaries, if neighbor has the same value, and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == value and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                shape_id_counter += 1
                
    return shapes, cell_to_shape_id

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Identifies shapes based on horizontal adjacency of different non-zero colors.
    Shifts the shape with the minimum value in such adjacent pairs one step to the left.

    Args:
        input_grid: A list of lists or numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    grid = np.array(input_grid)
    rows, cols = grid.shape
    output_grid = grid.copy() # Initialize output grid as a copy

    # 1. Identify all shapes in the input grid
    shapes, cell_to_shape_id = _find_shapes(grid)
    
    # 2. Identify shapes to shift based on horizontal adjacency
    shapes_to_shift_ids = set()
    for r in range(rows):
        for c in range(cols - 1): # Iterate up to the second-to-last column
            v1 = grid[r, c]
            v2 = grid[r, c + 1]

            # Check for horizontal adjacency between different non-zero values
            if v1 != 0 and v2 != 0 and v1 != v2:
                # Determine the minimum value and the corresponding shape_id
                if v1 < v2:
                    min_val_shape_id = cell_to_shape_id[r, c]
                else: # v2 < v1
                    min_val_shape_id = cell_to_shape_id[r, c + 1]
                
                # Add the shape_id to the set of shapes to be shifted
                # Check if min_val_shape_id is valid (not -1) before adding
                if min_val_shape_id != -1:
                    shapes_to_shift_ids.add(min_val_shape_id)

    # 3. Apply the shifts (in two phases to handle overlaps correctly)
    
    # Phase 1: Clear the original positions of shifting shapes
    for shape_id in shapes_to_shift_ids:
        shape_info = shapes[shape_id]
        for r, c in shape_info['cells']:
            output_grid[r, c] = 0 # Set original cell to background

    # Phase 2: Fill the new, left-shifted positions
    for shape_id in shapes_to_shift_ids:
        shape_info = shapes[shape_id]
        shape_value = shape_info['value']
        for r, c in shape_info['cells']:
            # Check if the shift is possible (not shifting from column 0)
            if c > 0:
                new_c = c - 1
                output_grid[r, new_c] = shape_value # Set new cell value, overwriting if necessary

    return output_grid.tolist() # Return as list of lists per standard format