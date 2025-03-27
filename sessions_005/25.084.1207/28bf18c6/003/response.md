```python
"""
Identifies the single contiguous non-white object in the input grid.
Determines its minimal bounding box (height H, width W).
Creates an output grid of size H x (2*W).
Extracts the object's pattern relative to its bounding box.
Places this pattern twice into the output grid, side-by-side, filling the grid completely.
The first pattern occupies columns 0 to W-1.
The second pattern occupies columns W to 2*W-1.
"""

import numpy as np
from collections import deque

def find_colored_object(grid):
    """
    Finds the first contiguous non-white object in the grid using Breadth-First Search.

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: A tuple containing:
            - set: Coordinates (row, col) of the object's pixels.
            - int: The color of the object.
        Returns (None, -1) if no non-white object is found.
    """
    rows, cols = grid.shape
    visited = set()
    q = deque()

    for r in range(rows):
        for c in range(cols):
            # Start search from the first non-white, unvisited pixel
            if grid[r, c] != 0 and (r, c) not in visited:
                color = grid[r, c]
                object_pixels = set()
                q.append((r, c))
                visited.add((r, c))

                # Perform BFS to find all connected pixels of the same color
                while q:
                    row, col = q.popleft()
                    object_pixels.add((row, col))

                    # Check neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds, color match, and visited status
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                
                # Assuming only one non-white object per task requirements
                return object_pixels, int(color) 

    # No non-white object found
    return None, -1


def get_bounding_box(pixels):
    """
    Calculates the minimal bounding box for a set of pixel coordinates.

    Args:
        pixels (set): A set of (row, col) tuples representing the object pixels.

    Returns:
        tuple: (min_row, min_col, height, width)
               Returns (0, 0, 0, 0) if the pixels set is empty or None.
    """
    if not pixels:
        return 0, 0, 0, 0

    # Find the min/max row and column indices from the object pixels
    min_row = min(r for r, c in pixels)
    max_row = max(r for r, c in pixels)
    min_col = min(c for r, c in pixels)
    max_col = max(c for r, c in pixels)

    # Calculate height and width
    height = max_row - min_row + 1
    width = max_col - min_col + 1

    return min_row, min_col, height, width


def transform(input_grid):
    """
    Transforms the input grid by duplicating the found object's pattern side-by-side.

    Args:
        input_grid (list[list[int]]): The input grid as a list of lists.

    Returns:
        list[list[int]]: The transformed output grid.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    input_np = np.array(input_grid, dtype=int)

    # 1. Find the single contiguous non-white object and its color.
    object_pixels, color = find_colored_object(input_np)

    # Handle case where no object is found (return empty or original, based on convention)
    if object_pixels is None:
        # Let's return an empty grid if no object is found.
        return [[]] 

    # 2. Determine the minimal bounding box of the object.
    min_row, min_col, height, width = get_bounding_box(object_pixels)
    
    # Handle edge case of zero-dimension bounding box (shouldn't happen if object_pixels is not None)
    if height == 0 or width == 0:
        return [[]]

    # 3. Create the object pattern grid (size: height x width).
    # Initialize with white (0).
    object_pattern = np.zeros((height, width), dtype=int)
    # Populate the pattern grid with the object's color at relative coordinates.
    for r, c in object_pixels:
        relative_r = r - min_row
        relative_c = c - min_col
        # Ensure coordinates are within the pattern bounds (sanity check)
        if 0 <= relative_r < height and 0 <= relative_c < width:
            object_pattern[relative_r, relative_c] = color

    # 4. Create the new output grid with dimensions height x (2 * width).
    # Initialize with white (0).
    output_height = height
    output_width = 2 * width
    output_grid_np = np.zeros((output_height, output_width), dtype=int)

    # 5. Place the object pattern into the left half of the output grid.
    # Slicing handles the copy: output[rows, cols] = pattern
    output_grid_np[0:height, 0:width] = object_pattern

    # 6. Place the object pattern into the right half of the output grid.
    output_grid_np[0:height, width:output_width] = object_pattern

    # 7. Convert the output NumPy array back to a list of lists format.
    output_grid = output_grid_np.tolist()

    # 8. Return the resulting grid.
    return output_grid

```