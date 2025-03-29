
Previous Code:
```python
import numpy as np
from collections import deque

"""
Transformation Rule:
1. Identify all separate connected groups (objects) of non-white pixels in the input grid, using 4-way (up, down, left, right) connections.
2. Find the object with the most pixels; this is the 'frame'. Note its color ('frame_color').
3. Identify all other non-white objects besides the frame; these are the 'internal objects'.
4. Create a set of 'barrier coordinates' containing the locations of *all* non-white pixels (from the frame and all internal objects).
5. Find all white pixels that can be reached starting from any white pixel on the border of the grid, moving only through other white pixels (4-way adjacency) and without entering any 'barrier coordinates'. Mark these as 'reachable white pixels'.
6. Find all white pixels that are orthogonally adjacent (share an edge) to any pixel belonging to an 'internal object'. Mark these as 'protected white pixels'.
7. Create the output grid as a copy of the input grid.
8. Examine every pixel location (row, column). If the pixel in the *input* grid is white AND it is *not* a 'reachable white pixel' AND it is *not* a 'protected white pixel', then change the color of that pixel in the *output* grid to the 'frame_color'.
9. If no non-white objects exist, return the input grid unchanged.
"""

def find_all_components(grid):
    """
    Finds all connected components of non-white pixels using 4-way adjacency.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A list of tuples [(color, coords_set), ...], where each tuple
        represents a connected non-white component. Returns an empty list
        if no non-white pixels are found. Components are sorted by size descending.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    all_components = [] # List to store (color, coords_set)

    # Iterate through each cell in the grid
    for r in range(rows):
        for c in range(cols):
            # If the cell is non-white and hasn't been visited as part of a component yet
            if grid[r, c] != 0 and not visited[r, c]:
                # Start a BFS to find the connected component
                component_color = grid[r, c]
                component_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True # Mark starting cell visited

                while q:
                    row, col = q.popleft()
                    component_coords.add((row, col))

                    # Check neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check if neighbor is within grid bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                           # Check if neighbor has the same color and hasn't been visited
                           if grid[nr, nc] == component_color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))

                # Store the found component (color and its coordinates)
                if component_coords: # Should always be true here
                    all_components.append((component_color, component_coords))

    # Sort components by size (number of coordinates) in descending order
    all_components.sort(key=lambda item: len(item[1]), reverse=True)

    return all_components

def find_reachable_white(grid, barrier_coords):
    """
    Finds white pixels reachable from the grid borders via white pixels,
    avoiding the specified barrier coordinates. Uses BFS.

    Args:
        grid: A numpy array representing the input grid.
        barrier_coords: A set of (row, col) tuples representing all barrier pixels
                       (typically all non-white pixels).

    Returns:
        A set of (row, col) tuples for the white pixels reachable from the border.
    """
    rows, cols = grid.shape
    reachable_white = set()
    q = deque()

    # Initialize queue with all border white cells that are NOT barriers
    for r in range(rows):
        for c in range(cols):
            if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
                coord = (r, c)
                if grid[r, c] == 0 and coord not in barrier_coords and coord not in reachable_white:
                    reachable_white.add(coord)
                    q.append(coord)

    # Perform BFS starting from the border white cells
    while q:
        r, c = q.popleft()
        # Explore orthogonal neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            neighbor_coord = (nr, nc)

            # Check if neighbor is within grid bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if neighbor is white, not a barrier, and not already visited/reachable
                if grid[nr, nc] == 0 and \
                   neighbor_coord not in barrier_coords and \
                   neighbor_coord not in reachable_white:
                    reachable_white.add(neighbor_coord)
                    q.append(neighbor_coord)

    return reachable_white

def find_protected_white(grid, internal_object_coords):
    """
    Finds white pixels that are orthogonally adjacent to any internal object pixel.

    Args:
        grid: A numpy array representing the input grid.
        internal_object_coords: A set of (row, col) tuples representing the coordinates
                                of all internal (non-frame) non-white objects.

    Returns:
        A set of (row, col) tuples for the white pixels adjacent to internal objects.
    """
    rows, cols = grid.shape
    protected_white = set()

    # Iterate through each coordinate belonging to an internal object
    for r, c in internal_object_coords:
        # Check orthogonal neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            neighbor_coord = (nr, nc)

            # Check if neighbor is within grid bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if neighbor is white
                if grid[nr, nc] == 0:
                    # Add this adjacent white pixel to the protected set
                    protected_white.add(neighbor_coord)

    return protected_white


def transform(input_grid):
    """Applies the transformation rule to the input grid."""
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify all non-white connected components, sorted by size descending
    all_components = find_all_components(input_grid)

    # 9. Handle edge case: If no non-white components exist, return original grid
    if not all_components:
        return output_grid

    # 2. Identify the largest component (the 'frame') and its color
    frame_component = all_components[0]
    frame_color = frame_component[0]
    # frame_coords = frame_component[1] # Not directly needed after barrier/internal sets built

    # 3. Identify internal objects (all components except the frame)
    internal_object_coords = set()
    if len(all_components) > 1:
        for _, coords in all_components[1:]: # Skip the first (largest) component
            internal_object_coords.update(coords)

    # 4. Create a single set of barrier coordinates from ALL non-white components
    barrier_coords = set()
    for _, coords in all_components:
        barrier_coords.update(coords)

    # 5. Find all white pixels reachable from the border, avoiding barriers
    reachable_white_coords = find_reachable_white(input_grid, barrier_coords)

    # 6. Find all white pixels orthogonally adjacent to internal objects
    protected_white_coords = find_protected_white(input_grid, internal_object_coords)

    # 7. & 8. Fill the 'internal fillable' white pixels
    # Iterate through every cell in the grid
    for r in range(rows):
        for c in range(cols):
            coord = (r, c)
            # Check if the pixel is white in the original input grid
            if input_grid[r, c] == 0:
                # Check if this white pixel is NOT reachable from border AND NOT protected
                if coord not in reachable_white_coords and coord not in protected_white_coords:
                    # This is an internal, fillable white pixel. Fill it.
                    output_grid[r, c] = frame_color
            # Else (if it's non-white, reachable white, or protected white),
            # it keeps its original color (already handled by copying input_grid)

    # Return the modified grid
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 2 2 0 0
0 2 0 0 0 0 0 0 2 0 0
0 2 0 5 0 0 5 0 2 0 0
0 2 0 0 0 5 0 0 2 0 0
0 2 0 0 0 0 0 0 2 0 0
0 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 2 2 0 0
0 2 2 2 2 2 2 2 2 0 0
0 2 2 5 0 0 5 2 2 0 0
0 2 2 0 0 5 0 2 2 0 0
0 2 2 2 2 2 2 2 2 0 0
0 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 2 2 0 0
0 2 2 0 2 2 0 2 2 0 0
0 2 0 5 0 0 5 0 2 0 0
0 2 2 0 0 5 0 2 2 0 0
0 2 2 2 2 0 2 2 2 0 0
0 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 5
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 11.363636363636346

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 2 2 0 0
0 2 0 0 0 0 0 0 2 0 0
0 2 0 0 0 0 0 0 2 0 0
0 2 0 5 0 0 0 0 2 0 0
0 2 0 0 5 0 0 0 2 0 0
0 2 0 0 0 0 0 0 2 0 0
0 2 0 0 0 0 0 0 2 0 0
0 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 2 2 0 0
0 2 2 2 2 2 2 2 2 0 0
0 2 2 2 2 2 2 2 2 0 0
0 2 2 5 0 2 2 2 2 0 0
0 2 2 0 5 2 2 2 2 0 0
0 2 2 2 2 2 2 2 2 0 0
0 2 2 2 2 2 2 2 2 0 0
0 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 2 2 0 0
0 2 2 2 2 2 2 2 2 0 0
0 2 2 0 2 2 2 2 2 0 0
0 2 0 5 0 2 2 2 2 0 0
0 2 2 0 5 0 2 2 2 0 0
0 2 2 2 0 2 2 2 2 0 0
0 2 2 2 2 2 2 2 2 0 0
0 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 6.060606060606062

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 2 2 2 2 0
0 2 0 0 0 0 0 0 0 0 2 0
0 2 0 0 0 0 0 0 0 0 2 0
0 2 0 0 5 0 0 0 0 0 2 0
0 2 0 0 0 0 5 0 0 0 2 0
0 2 0 0 5 0 0 5 0 0 2 0
0 2 0 0 0 0 0 0 0 0 2 0
0 2 2 2 2 2 2 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 2 2 2 2 0
0 2 2 2 2 2 2 2 2 2 2 0
0 2 2 2 2 2 2 2 2 2 2 0
0 2 2 2 5 0 0 0 2 2 2 0
0 2 2 2 0 0 5 0 2 2 2 0
0 2 2 2 5 0 0 5 2 2 2 0
0 2 2 2 2 2 2 2 2 2 2 0
0 2 2 2 2 2 2 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 2 2 2 2 0
0 2 2 2 2 2 2 2 2 2 2 0
0 2 2 2 0 2 2 2 2 2 2 0
0 2 2 0 5 0 0 2 2 2 2 0
0 2 2 2 0 0 5 0 2 2 2 0
0 2 2 0 5 0 0 5 0 2 2 0
0 2 2 2 0 2 2 0 2 2 2 0
0 2 2 2 2 2 2 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 7
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 9.722222222222229
