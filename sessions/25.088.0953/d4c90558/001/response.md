```python
import numpy as np
from collections import deque

"""
Identifies non-white, non-gray contiguous shapes ("containers") in the input grid.
For each container, counts the number of gray pixels strictly enclosed within its bounding box.
Constructs an output grid where each row corresponds to a container.
The color of the row matches the container's color.
The number of colored cells in the row equals the count of enclosed gray pixels for that container.
The rows are sorted in ascending order based on the count of enclosed gray pixels.
The width of the output grid is determined by the maximum count of enclosed gray pixels found in any container.
"""

def find_connected_component(grid, start_r, start_c, visited):
    """
    Finds a connected component of the same color starting from (start_r, start_c) using BFS.

    Args:
        grid (np.array): The input grid.
        start_r (int): Starting row index.
        start_c (int): Starting column index.
        visited (np.array): Boolean array marking visited cells.

    Returns:
        tuple: (color, list_of_pixels)
               color (int): The color of the component.
               list_of_pixels (list): A list of (row, col) tuples for the component's pixels.
               Returns (None, []) if the starting pixel is already visited or invalid.
    """
    rows, cols = grid.shape
    if not (0 <= start_r < rows and 0 <= start_c < cols) or visited[start_r, start_c]:
        return None, []

    target_color = grid[start_r, start_c]
    pixels = []
    queue = deque([(start_r, start_c)])
    visited[start_r, start_c] = True

    while queue:
        r, c = queue.popleft()
        pixels.append((r, c))

        # Check 4 neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            if 0 <= nr < rows and 0 <= nc < cols and \
               not visited[nr, nc] and grid[nr, nc] == target_color:
                visited[nr, nc] = True
                queue.append((nr, nc))

    return target_color, pixels

def get_bounding_box(pixels):
    """
    Calculates the bounding box for a list of pixels.

    Args:
        pixels (list): A list of (row, col) tuples.

    Returns:
        tuple: (min_r, max_r, min_c, max_c) or None if pixels is empty.
    """
    if not pixels:
        return None

    min_r = min(r for r, c in pixels)
    max_r = max(r for r, c in pixels)
    min_c = min(c for r, c in pixels)
    max_c = max(c for r, c in pixels)
    return min_r, max_r, min_c, max_c

def transform(input_grid):
    """
    Transforms the input grid based on identifying containers and counting enclosed gray pixels.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    visited = np.zeros_like(input_np, dtype=bool)
    container_data = []

    # 1. Scan the input grid to identify all distinct contiguous objects (containers)
    #    that are not white (0) or gray (5).
    for r in range(rows):
        for c in range(cols):
            pixel_color = input_np[r, c]
            if pixel_color != 0 and pixel_color != 5 and not visited[r, c]:
                # Found a potential start of a container
                container_color, container_pixels = find_connected_component(input_np, r, c, visited)

                if container_pixels:
                    # 2a. Record its primary color.
                    # (Done above: container_color)

                    # 2b. Determine its bounding box.
                    bounding_box = get_bounding_box(container_pixels)
                    if bounding_box:
                        min_r, max_r, min_c, max_c = bounding_box

                        # 2c. Count the number of gray (5) pixels located strictly within this bounding box.
                        gray_count = 0
                        for rr in range(min_r + 1, max_r):
                            for cc in range(min_c + 1, max_c):
                                if input_np[rr, cc] == 5:
                                    gray_count += 1

                        # 2d. Store the container's color and the count of gray pixels.
                        container_data.append({'color': container_color, 'count': gray_count})

    # 3. Collect all such (color, count) pairs. (Done in container_data)

    # 4. Sort these pairs in ascending order based on the count.
    sorted_data = sorted(container_data, key=lambda item: item['count'])

    # 5. Calculate the required height of the output grid.
    output_height = len(sorted_data)

    # 6. Calculate the required width of the output grid.
    output_width = 0
    if sorted_data:
        output_width = max(item['count'] for item in sorted_data)

    # 7. Create a new grid with the calculated height and width, initially filled with white (0).
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # 8. Iterate through the sorted (color, count) pairs and populate the output grid.
    for i, item in enumerate(sorted_data):
        color = item['color']
        count = item['count']
        # Fill the first 'count' cells of row 'i' with the color 'c'.
        # Remaining cells default to white (0).
        if count > 0: # Ensure count is positive before slicing
            output_grid[i, :count] = color

    # 9. The resulting grid is the final output.
    return output_grid.tolist()
```