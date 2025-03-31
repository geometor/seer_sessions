import numpy as np
from typing import List, Dict, Tuple

"""
Transformation Rule Description:

1.  Create a new output grid with the same dimensions as the input grid, filled entirely with the background color (white, 0).
2.  Search the input grid, starting from the bottom row and moving upwards, to find the first row composed entirely of azure (8) pixels. If found, copy this azure line to the exact same row in the output grid and record its row index as `base_row`. If no such line is found, set `base_row` to be the total height of the grid (effectively placing the base just below the last row).
3.  Identify all distinct horizontal, contiguous lines of pixels in the input grid that are *not* white (0) and *not* azure (8). For each such line (object), record its color, its length (number of pixels), and its original row index in the input grid.
4.  Create a list of these identified objects.
5.  Sort this list of objects based on two criteria:
    *   Primary criterion: Sort by object length in descending order (longest objects first).
    *   Secondary criterion (for ties in length): Sort by the original row index in ascending order (objects that were originally higher in the input grid come first).
6.  Determine the width of the grid.
7.  Initialize a `current_stack_row` variable to `base_row - 1`.
8.  Iterate through the sorted list of objects:
    *   For the current object, retrieve its color and length.
    *   Calculate the starting column for placing the object in the output grid: `start_column = grid_width - object_length`.
    *   Place the object's color into the output grid at the `current_stack_row`, filling the cells from `start_column` up to the last column (inclusive).
    *   Decrement the `current_stack_row` by 1 (to move up one row for the next object).
9.  Return the completed output grid.
"""

def find_movable_objects(input_grid: np.ndarray) -> List[Dict]:
    """
    Finds all horizontal contiguous lines of non-background (0) and non-base (8) colors.

    Args:
        input_grid: The input numpy array representing the grid.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        with keys: 'color', 'length', 'row', 'col_start', 'col_end'.
    """
    objects = []
    height, width = input_grid.shape
    visited = np.zeros_like(input_grid, dtype=bool)

    for r in range(height):
        for c in range(width):
            if visited[r, c]:
                continue

            color = input_grid[r, c]
            # Ignore background (0) and base (8) colors
            if color == 0 or color == 8:
                visited[r, c] = True
                continue

            # Found the start of a potential horizontal object
            col_start = c
            col_end = c
            # Extend to the right as long as the color is the same in the same row
            while col_end + 1 < width and input_grid[r, col_end + 1] == color and not visited[r, col_end + 1]:
                col_end += 1

            # Mark all pixels of this object as visited
            visited[r, col_start:col_end + 1] = True

            # Calculate length and store object details
            length = col_end - col_start + 1
            objects.append({
                'color': int(color),
                'length': int(length),
                'row': int(r),
                'col_start': int(col_start), # Store original columns for potential future use, though not used for placement here
                'col_end': int(col_end)
            })

    return objects

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # 1. Initialize output grid with background color (0)
    output_grid = np.zeros_like(input_np)

    # 2. Find the azure base line (color 8) and copy it
    base_row = -1
    for r in range(height - 1, -1, -1):
        is_azure_line = True
        has_azure = False
        for c in range(width):
            if input_np[r, c] != 8:
                is_azure_line = False
            else:
                has_azure = True
        # The base must be a full row of 8s
        if is_azure_line and has_azure:
            base_row = r
            output_grid[base_row, :] = 8
            break
        # If we encounter non-8s in a row after seeing 8s lower down,
        # it confirms the lower rows weren't the base.
        # If we hit the top without finding a full line, base_row remains -1.

    # 3. Identify all movable objects (horizontal lines not 0 or 8)
    movable_objects = find_movable_objects(input_np)

    # 5. Sort the objects:
    #    - Primary: length (descending)
    #    - Secondary: original row (ascending)
    sorted_objects = sorted(movable_objects, key=lambda obj: (-obj['length'], obj['row']))

    # 7. Initialize the starting row for stacking
    # If a base was found, stack above it. Otherwise, stack from the bottom edge.
    stack_row = base_row - 1 if base_row != -1 else height - 1

    # 8. Iterate through sorted objects and place them right-aligned in the output grid
    for obj in sorted_objects:
        if stack_row < 0:
            # Grid is full, cannot place more objects (edge case)
            print(f"Warning: Not enough space to stack object: {obj}")
            continue

        # Retrieve object properties
        color = obj['color']
        length = obj['length']

        # Calculate target columns for right-alignment
        target_col_start = width - length
        target_col_end = width - 1 # Inclusive index for numpy slicing

        # Place the object
        if target_col_start >= 0: # Ensure start column is valid
             output_grid[stack_row, target_col_start : target_col_end + 1] = color

        # Decrement stack_row for the next object
        stack_row -= 1

    # 9. Return the completed output grid as a list of lists
    return output_grid.tolist()