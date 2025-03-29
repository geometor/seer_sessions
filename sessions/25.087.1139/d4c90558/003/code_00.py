import numpy as np
from collections import deque

"""
Identify all distinct, connected non-white (0) and non-gray (5) shapes in the input grid.
For each shape, count the number of gray (5) pixels located within its bounding box.
Construct an output grid where each row corresponds to a shape from the input.
The rows are ordered based on the count of gray pixels within the shape's bounding box, in ascending order.
Each output row contains the shape's color repeated N times, where N is the count of gray pixels within its bounding box.
Rows are padded with white (0) on the right to match the width of the row with the maximum gray pixel count.
"""

def find_objects(grid):
    """
    Finds distinct connected objects (shapes) of non-background, non-gray colors.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'color', 'pixels' (set of (r, c) tuples),
              'bounding_box' (min_row, max_row, min_col, max_col),
              and 'top_row'.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    ignored_colors = {0, 5} # white and gray

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color not in ignored_colors and not visited[r, c]:
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c

                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                objects.append({
                    'color': color,
                    'pixels': obj_pixels,
                    'bounding_box': (min_r, max_r, min_c, max_c),
                    'top_row': min_r # Keep top_row in case it's needed for tie-breaking
                })
    return objects

def count_gray_in_bbox(grid, bounding_box):
    """
    Counts the number of gray (5) pixels within a given bounding box.

    Args:
        grid (np.array): The input grid.
        bounding_box (tuple): (min_row, max_row, min_col, max_col).

    Returns:
        int: The count of gray pixels.
    """
    min_r, max_r, min_c, max_c = bounding_box
    count = 0
    # Iterate within the bounding box (inclusive)
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if grid[r, c] == 5:
                count += 1
    return count

def transform(input_grid_list):
    """
    Transforms the input grid based on shape analysis and gray pixel counts,
    ordering output rows by ascending gray pixel count.

    Args:
        input_grid_list (list of lists): The 2D input grid.

    Returns:
        list of lists: The transformed 2D output grid.
    """
    input_grid = np.array(input_grid_list)

    # 1. Identify all distinct colored shapes (non-white, non-gray)
    shapes = find_objects(input_grid)

    # Handle cases with no shapes
    if not shapes:
        # Return an empty grid representation consistent with ARC examples if needed
        # E.g., a 0x0 grid might be [[ ]] or similar depending on ARC format.
        # For now, returning a 1x0 grid might be safer.
        return [[]]

    shape_summaries = []
    max_gray_count = 0

    # 2. For each shape, calculate its bounding box and count gray pixels within it
    for shape in shapes:
        gray_count = count_gray_in_bbox(input_grid, shape['bounding_box'])
        shape_summaries.append({
            'color': shape['color'],
            'gray_count': gray_count,
            'top_row': shape['top_row'] # Store for potential tie-breaking
        })
        # Track the maximum gray count to determine output width
        max_gray_count = max(max_gray_count, gray_count)

    # 3. Determine output dimensions
    output_height = len(shape_summaries)
    # Ensure width is at least 0, even if max_gray_count is 0
    output_width = max(0, max_gray_count)

    # 4. Sort shapes based on gray_count (ascending)
    # If gray counts are equal, a secondary sort might be needed, but not observed yet.
    # Using top_row as a stable secondary sort for consistency.
    shape_summaries.sort(key=lambda x: (x['gray_count'], x['top_row']))

    # 5. Construct the output grid
    # Initialize with background color (white = 0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # 6. Populate the output grid row by row according to sorted shapes
    for i, summary in enumerate(shape_summaries):
        color = summary['color']
        count = summary['gray_count']
        # Fill the row with the shape's color up to its gray count
        # Use min(count, output_width) in case count exceeds calculated width (shouldn't happen with max_gray_count logic)
        output_grid[i, :count] = color
        # The rest of the row remains white (0) due to initialization

    # Convert back to list of lists for the required ARC format
    return output_grid.tolist()