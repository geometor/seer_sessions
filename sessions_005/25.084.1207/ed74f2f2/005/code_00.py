"""
Analyze two 3x3 patterns within the input grid, the Left Pattern (LP) at rows 1-3, 
cols 1-3 and the Right Pattern (RP) at rows 1-3, cols 5-7, to determine the color 
and shape of a 3x3 output grid.

1. Calculate the count of gray (5) pixels in the logical OR of LP and RP ('or_count').
2. Calculate the count of gray (5) pixels in RP ('right_count').
3. Conditionally, count the number of 4-connected gray objects in RP ('rp_object_count').
4. Determine an output color based on these counts:
    - Red (2) if or_count is 5, 7, 6, or 9.
    - Blue (1) if or_count is 8 and right_count is 7.
    - Green (3) if or_count is 8 and right_count is 8 and rp_object_count is 1.
    - Green (3) if or_count is 8 and right_count is 6 and rp_object_count is 1.
    - Blue (1) if or_count is 8 and right_count is 6 and rp_object_count is 2.
    - Default White (0) otherwise.
5. Determine the output shape:
    - If the output color is Blue (1), use a fixed shape mask: 
      [[F, T, F], [F, T, F], [T, T, T]].
    - Otherwise (Red or Green), use the shape mask defined by gray pixels in RP.
6. Construct the 3x3 output grid by filling the determined shape with the 
   determined color, leaving other cells White (0).
"""

import numpy as np

def count_objects_4_connectivity(grid, target_color):
    """
    Counts contiguous objects of a target color in a grid using 4-connectivity.

    Args:
        grid (np.array): The 2D grid to search within.
        target_color (int): The color value of the objects to count.

    Returns:
        int: The number of distinct connected objects of the target color.
    """
    mask = (grid == target_color)
    if not np.any(mask):
        return 0

    visited = np.zeros_like(mask, dtype=bool)
    count = 0
    rows, cols = grid.shape

    for r in range(rows):
        for c in range(cols):
            # If it's the target color and hasn't been visited yet, start a flood fill (DFS)
            if mask[r, c] and not visited[r, c]:
                count += 1
                stack = [(r, c)]
                visited[r, c] = True
                while stack:
                    row, col = stack.pop()
                    # Check neighbors (4-connectivity: N, S, E, W)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds and if the neighbor is target color and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           mask[nr, nc] and not visited[nr, nc]:
                            visited[nr, nc] = True
                            stack.append((nr, nc))
    return count

def transform(input_grid):
    """
    Transforms the input grid based on comparing two 3x3 subgrids (LP and RP).

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed 3x3 output grid.
    """
    # Convert input to numpy array for easier slicing and operations
    grid = np.array(input_grid, dtype=int)

    # 1. Identify the Left Pattern (LP) and Right Pattern (RP) subgrids
    left_pattern = grid[1:4, 1:4]
    right_pattern = grid[1:4, 5:8]

    # 2. Analyze Patterns
    # Create boolean masks for gray pixels
    lp_mask = (left_pattern == 5)
    rp_mask = (right_pattern == 5)

    # a. Calculate OR pattern and count
    or_pattern_mask = lp_mask | rp_mask
    or_count = np.count_nonzero(or_pattern_mask)

    # b. Calculate Right Pattern count
    right_count = np.count_nonzero(rp_mask)

    # c. Initialize rp_object_count (calculated only if needed)
    rp_object_count = None

    # 3. Determine Output Color
    output_color = 0 # Default to White (0)

    if or_count in [5, 6, 7, 9]:
        output_color = 2 # Red
    elif or_count == 8:
        if right_count == 7:
            output_color = 1 # Blue
        elif right_count == 8:
            # Calculate object count for this specific case
            rp_object_count = count_objects_4_connectivity(right_pattern, 5)
            if rp_object_count == 1:
                output_color = 3 # Green
            # else: output_color remains 0 (default)
        elif right_count == 6:
             # Calculate object count for this specific case
            rp_object_count = count_objects_4_connectivity(right_pattern, 5)
            if rp_object_count == 1:
                output_color = 3 # Green
            elif rp_object_count == 2:
                output_color = 1 # Blue
            # else: output_color remains 0 (default)
        # else: output_color remains 0 (default for other right_counts when or_count=8)
    # else: output_color remains 0 (default for other or_counts)


    # 4. Determine Output Shape Mask (3x3 boolean array)
    if output_color == 1: # Blue
        # Use the fixed shape for Blue
        output_shape_mask = np.array([
            [False, True, False],
            [False, True, False],
            [True, True, True]
        ])
    else:
        # For Red(2) or Green(3), use the Right Pattern's gray shape
        # Also applies if output_color defaulted to 0 (White)
        output_shape_mask = rp_mask

    # 5. Construct the 3x3 output grid
    # Initialize with White (0)
    output_grid = np.zeros((3, 3), dtype=int)
    # Apply the color based on the shape mask
    output_grid = np.where(output_shape_mask, output_color, 0)

    # 6. Return the final output grid as a list of lists
    return output_grid.tolist()