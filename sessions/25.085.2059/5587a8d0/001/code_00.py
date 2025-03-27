"""
Creates a layered square grid based on the sizes of non-background objects in the input grid.

1.  Identify the most frequent color in the input grid; this is the background color.
2.  Find all contiguous groups (objects) of pixels (using 4-way adjacency) that are *not* the background color.
3.  For each distinct non-background color found, determine the size (number of pixels) of its largest contiguous object.
4.  Count the number of distinct non-background colors (N).
5.  Sort these distinct colors in descending order based on their largest object size. Let the sorted colors be C1, C2, ..., CN.
6.  Calculate the output grid dimensions as (2N - 1) x (2N - 1).
7.  Create the output grid. Fill it concentrically, layer by layer, starting from the outside:
    - Layer 0 (outermost border) is filled with color C1.
    - Layer 1 (next layer inwards) is filled with color C2.
    - ...
    - Layer k is filled with color C(k+1).
    - Layer N-1 (center pixel or block) is filled with color CN.
"""

import numpy as np
from collections import Counter, deque

def _find_objects(grid, background_color):
    """
    Finds all contiguous objects of non-background colors using BFS.

    Args:
        grid (np.array): The input grid.
        background_color (int): The color to ignore.

    Returns:
        dict: A dictionary mapping each non-background color to a list of its
              objects, where each object is represented by a set of (row, col) tuples.
    """
    rows, cols = grid.shape
    visited = set()
    objects_by_color = {}

    for r in range(rows):
        for c in range(cols):
            if (r, c) in visited:
                continue

            color = grid[r, c]
            if color == background_color:
                visited.add((r, c))
                continue

            # Start BFS for a new object
            current_object_coords = set()
            q = deque([(r, c)])
            visited.add((r, c))
            current_object_coords.add((r, c))

            while q:
                row, col = q.popleft()

                # Check 4-directional neighbors
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = row + dr, col + dc

                    if 0 <= nr < rows and 0 <= nc < cols and \
                       (nr, nc) not in visited and \
                       grid[nr, nc] == color:
                        visited.add((nr, nc))
                        current_object_coords.add((nr, nc))
                        q.append((nr, nc))

            # Store the found object
            if color not in objects_by_color:
                objects_by_color[color] = []
            objects_by_color[color].append(current_object_coords)

    return objects_by_color

def _get_largest_object_sizes(objects_by_color):
    """
    Calculates the size of the largest object for each color.

    Args:
        objects_by_color (dict): Dictionary from _find_objects.

    Returns:
        dict: A dictionary mapping each color to the size of its largest object.
    """
    largest_sizes = {}
    for color, objects_list in objects_by_color.items():
        if objects_list:
            largest_sizes[color] = max(len(obj) for obj in objects_list)
        else:
             largest_sizes[color] = 0 # Should not happen if color is in keys
    return largest_sizes


def transform(input_grid):
    """
    Transforms the input grid based on the sizes of non-background objects.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape

    # 1. Identify Background Color (most frequent)
    colors, counts = np.unique(input_array, return_counts=True)
    background_color = colors[np.argmax(counts)]

    # 2. Find all contiguous non-background objects
    objects_by_color = _find_objects(input_array, background_color)

    # 3. Get unique non-background colors
    non_background_colors = list(objects_by_color.keys())

    # Handle edge case: No non-background objects found
    if not non_background_colors:
        # Returning a 1x1 grid with the background color might be a safe default,
        # though the examples suggest this won't happen.
        # Or perhaps return an empty grid or the original? Let's stick to 1x1.
        return [[background_color]] # Or potentially adjust based on expected behavior

    # 4. Determine the size of the largest object for each color
    largest_sizes = _get_largest_object_sizes(objects_by_color)

    # 5. Sort colors by largest object size (descending)
    sorted_colors = sorted(non_background_colors, key=lambda c: largest_sizes[c], reverse=True)

    # 6. Calculate output grid dimensions
    N = len(sorted_colors)
    output_dim = 2 * N - 1

    # 7. Create the output grid
    # Initialize with a dummy value like -1 or the center color CN
    output_grid = np.full((output_dim, output_dim), -1, dtype=int)
    center = N - 1 # Center index for both row and column

    # 8. Fill the output grid layer by layer
    for layer_index in range(N):
        # Color for this layer (outermost is layer 0)
        layer_color = sorted_colors[layer_index]
        # The distance from the center for this layer's boundary
        dist = N - 1 - layer_index

        for r in range(output_dim):
            for c in range(output_dim):
                # Calculate Manhattan distance-like metric for square layers
                current_dist = max(abs(r - center), abs(c - center))
                # Fill if this pixel is exactly on the boundary of the current layer
                if current_dist == dist:
                    output_grid[r, c] = layer_color

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()