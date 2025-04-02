import numpy as np
from collections import deque

"""
Transforms an input grid by performing the following steps:
1. Identifies all distinct contiguous non-white objects (patterns) in the input grid.
2. For each pattern, determines the minimum required downward vertical shift (delta_r > 0) such that all pixels of the shifted pattern land on white (0) cells relative to the *original* input grid state or outside the original grid's bottom boundary.
3. Calculates the maximum row index required to accommodate both the original grid content and all the shifted patterns.
4. If necessary, resizes the output grid vertically, padding with white pixels, to meet the required height.
5. Copies the pixels of each original pattern to their calculated shifted positions in the (potentially resized) output grid. The original patterns remain in place.
"""

def _find_objects(grid_np):
    """
    Finds contiguous non-white objects in the grid using BFS.

    Args:
        grid_np (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              with keys 'color' (int) and 'pixels' (list of (r, c) tuples).
    """
    rows, cols = grid_np.shape
    visited = np.zeros_like(grid_np, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid_np[r, c] != 0 and not visited[r, c]:
                color = grid_np[r, c]
                obj_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    row, col = q.popleft()
                    obj_pixels.append((row, col))

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc

                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid_np[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                if obj_pixels:
                    objects.append({'color': int(color), 'pixels': sorted(obj_pixels)}) # Sort pixels for consistency

    # Sort objects primarily by top-most row, then left-most column for deterministic processing order (though order shouldn't affect outcome here)
    objects.sort(key=lambda obj: obj['pixels'][0])
    return objects


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed grid.
    """
    input_np = np.array(input_grid, dtype=int)
    output_np = input_np.copy() # Start with a copy
    input_rows, input_cols = input_np.shape
    
    # 1. Find all non-white objects in the input
    objects = _find_objects(input_np)
    
    if not objects:
        return input_grid # No objects to move, return original

    object_shifts = []
    max_required_row = input_rows - 1 # Track the max row index needed

    # 2. For each object, determine its minimum downward shift
    for obj in objects:
        obj_pixels = obj['pixels']
        delta_r = 1
        while True:
            can_place = True
            current_max_r_for_copy = -1 # Track max row for *this* potential copy
            for r, c in obj_pixels:
                target_r = r + delta_r
                target_c = c
                current_max_r_for_copy = max(current_max_r_for_copy, target_r)

                # Check if the target location is within the *original* grid bounds
                # AND if it lands on a non-white pixel in the *original* grid
                if target_r < input_rows and input_np[target_r, target_c] != 0:
                    can_place = False
                    break # This delta_r is invalid for this object

            if can_place:
                # Found the minimum valid shift for this object
                object_shifts.append({'object': obj, 'delta_r': delta_r})
                # Update the overall maximum row needed for the final grid
                max_required_row = max(max_required_row, current_max_r_for_copy)
                break # Move to the next object

            # If placement wasn't possible, try the next shift distance
            delta_r += 1

    # 3. Determine final grid size and resize if needed
    required_rows = max_required_row + 1
    current_rows = output_np.shape[0]

    if required_rows > current_rows:
        # Create a new larger grid filled with white (0)
        resized_output = np.zeros((required_rows, input_cols), dtype=int)
        # Copy the existing content into the top part
        resized_output[:current_rows, :] = output_np
        output_np = resized_output

    # 4. Apply the shifts to copy objects onto the output grid
    for item in object_shifts:
        obj = item['object']
        delta_r = item['delta_r']
        color = obj['color']
        
        for r, c in obj['pixels']:
            target_r = r + delta_r
            target_c = c
            # Ensure target is within the (potentially resized) output grid bounds
            # This check should technically be redundant due to resizing, but good practice
            if 0 <= target_r < output_np.shape[0] and 0 <= target_c < output_np.shape[1]:
                 output_np[target_r, target_c] = color

    # 5. Convert back to list of lists and return
    return output_np.tolist()