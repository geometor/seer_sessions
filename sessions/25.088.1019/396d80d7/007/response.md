```python
import numpy as np
import collections

"""
Transformation Rule:

1.  Analyze Colors:
    a.  Identify the most frequent color in the input grid; this is the `background_color`.
    b.  Identify the two other colors present. If there are not exactly two other colors, return the input grid unchanged.
    c.  Count, for each of the two non-background colors, how many times its pixels are orthogonally adjacent to a `background_color` pixel.
    d.  The non-background color with the strictly *higher* count of adjacencies to the background is the `frame_color`. The other non-background color is the `fill_color`.
    e.  If the adjacency counts are equal, the non-background color with the *lower* numerical value is the `frame_color`, and the other is the `fill_color`.
    f.  If *neither* non-background color has any adjacency to the background, return the input grid unchanged.
2.  Prepare Output: Create a mutable copy of the input grid.
3.  Process Frame Objects:
    a.  Find all distinct groups (objects) of orthogonally connected pixels that have the `frame_color`.
    b.  For each `frame_object` found:
        i.  Identify all `background_color` pixels that are orthogonally adjacent to *any* pixel within this `frame_object`. Let this set be `adjacent_background_pixels`.
        ii. Determine Fill Targets: Select *all* pixels from `adjacent_background_pixels` to be filled. (Simplified hypothesis, replacing previous complex rule).
        iii. Apply Fill: Change the color of the selected target pixels in the output grid to the `fill_color`.
4.  Return Result: Return the modified output grid.
"""

def _identify_colors(input_array):
    """
    Identifies background, frame, and fill colors based on frequency and adjacency.

    Args:
        input_array: numpy array representing the input grid.

    Returns:
        A tuple (background_color, frame_color, fill_color).
        Returns (None, None, None) if the criteria (e.g., exactly 3 colors,
        non-background colors adjacent to background) are not met.
    """
    colors, counts = np.unique(input_array, return_counts=True)

    # Check for exactly 3 colors
    if len(colors) != 3:
        return None, None, None

    # Identify background color (most frequent)
    background_color = colors[np.argmax(counts)]
    non_background_colors = sorted([c for c in colors if c != background_color])
    color1, color2 = non_background_colors[0], non_background_colors[1]

    rows, cols = input_array.shape
    adj_counts = {color1: 0, color2: 0}
    shifts = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Orthogonal neighbors

    # Count adjacencies to background for each non-background color
    for r in range(rows):
        for c in range(cols):
            current_color = input_array[r, c]
            if current_color == color1 or current_color == color2:
                for dr, dc in shifts:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if input_array[nr, nc] == background_color:
                            adj_counts[current_color] += 1

    c1_adj = adj_counts[color1]
    c2_adj = adj_counts[color2]

    # Check if at least one non-background color touches the background
    if c1_adj == 0 and c2_adj == 0:
         return None, None, None

    # Determine frame and fill based on adjacency counts and tie-breaking
    if c1_adj > c2_adj:
        frame_color = color1
        fill_color = color2
    elif c2_adj > c1_adj:
        frame_color = color2
        fill_color = color1
    else: # Equal adjacency counts - tie-break using numerical value
        frame_color = min(color1, color2)
        fill_color = max(color1, color2)

    return background_color, frame_color, fill_color

def _find_objects(grid, target_color):
    """
    Finds all distinct orthogonally connected objects of a target color in the grid.

    Args:
        grid: numpy array representing the grid.
        target_color: The color of the objects to find.

    Returns:
        A list of lists, where each inner list contains (row, col) tuples
        representing the coordinates of one object.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    shifts = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Orthogonal neighbors

    for r in range(rows):
        for c in range(cols):
            # If it's the target color and not visited yet, start BFS
            if grid[r, c] == target_color and not visited[r, c]:
                obj_coords = []
                q = collections.deque([(r, c)])
                visited[r, c] = True
                while q:
                    row, col = q.popleft()
                    obj_coords.append((row, col))
                    # Explore neighbors
                    for dr, dc in shifts:
                        nr, nc = row + dr, col + dc
                        # Check bounds, target color, and visited status
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == target_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                if obj_coords: # Add the found object
                    objects.append(obj_coords)
    return objects

def _get_adjacent_coords(coords, grid_shape, target_color, grid):
    """
    Finds all coordinates of a specific target_color orthogonally adjacent
    to any coordinate in the input list `coords`.

    Args:
        coords: A list or set of (row, col) tuples representing the source object.
        grid_shape: A tuple (rows, cols) of the grid dimensions.
        target_color: The color to search for in adjacent cells.
        grid: The numpy array representing the grid.

    Returns:
        A set of (row, col) tuples of adjacent cells with the target_color.
    """
    rows, cols = grid_shape
    adjacent = set()
    shifts = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Orthogonal neighbors
    object_coords_set = set(coords) # Use set for faster checking if neighbor is part of object

    for r, c in coords:
        for dr, dc in shifts:
            nr, nc = r + dr, c + dc
            # Check bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                 # Check if the neighbor is the target color AND not part of the object itself
                 if grid[nr, nc] == target_color and (nr, nc) not in object_coords_set:
                    adjacent.add((nr, nc))
    return adjacent

def transform(input_grid):
    """
    Transforms the input grid by finding 'frame' objects and filling adjacent
    'background' pixels with the 'fill' color. Color roles are determined by
    frequency and adjacency counts.
    """
    input_array = np.array(input_grid, dtype=int)
    output_array = np.copy(input_array)
    rows, cols = input_array.shape

    # 1. Analyze Colors
    background_color, frame_color, fill_color = _identify_colors(input_array)

    # If colors can't be determined as required, return the original grid
    if background_color is None or frame_color is None or fill_color is None:
        # Convert back to list of lists for ARC standard
        return input_array.tolist()

    # 3a. Find Frame Objects
    frame_objects = _find_objects(input_array, frame_color)

    # 3b. Process Each Frame Object
    pixels_to_fill = set()
    for obj_coords in frame_objects:
        # 3bi. Identify adjacent background pixels
        adjacent_background_pixels = _get_adjacent_coords(
            obj_coords, (rows, cols), background_color, input_array
        )

        # 3bii. Determine Fill Targets: Select all adjacent background pixels
        # (Simplified hypothesis compared to previous attempts)
        pixels_to_fill.update(adjacent_background_pixels)

    # 3biii. Apply Fill (modify the output array)
    for r, c in pixels_to_fill:
         # Check bounds just in case, although _get_adjacent_coords should ensure this
         if 0 <= r < rows and 0 <= c < cols:
             output_array[r, c] = fill_color

    # 4. Return Result
    # Convert back to list of lists for ARC standard
    return output_array.tolist()
```