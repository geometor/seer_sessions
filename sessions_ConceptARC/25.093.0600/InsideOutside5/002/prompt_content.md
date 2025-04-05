
Previous Code:
```python
import numpy as np
from collections import deque

"""
Identifies connected objects of the same non-zero color in the input grid.
Determines if an object is completely enclosed by cells of exactly one other *single* non-zero color (using 8-way adjacency).
Outputs a grid containing only the cells of such enclosed objects, with all other cells set to the background color (0).
"""

def _find_neighbors(grid_shape, object_coords):
    """
    Finds all unique neighboring cells (8-way adjacency) adjacent to any cell
    of the object, excluding cells that are part of the object itself.

    Args:
        grid_shape (tuple): The (rows, cols) shape of the grid.
        object_coords (set): A set of (row, col) tuples representing the object's cells.

    Returns:
        set: A set of (row, col) tuples representing unique neighbor cells.
    """
    rows, cols = grid_shape
    neighbors = set()
    # Define 8 directions (including diagonals)
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  ( 0, -1),          ( 0, 1),
                  ( 1, -1), ( 1, 0), ( 1, 1)]

    for r, c in object_coords:
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            # Check grid boundaries
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbor_coord = (nr, nc)
                # Add if it's not part of the object itself
                if neighbor_coord not in object_coords:
                    neighbors.add(neighbor_coord)
    return neighbors

def _is_enclosed(grid, neighbor_coords):
    """
    Checks if all neighbor cells belong to exactly one other single non-zero object.

    Args:
        grid (np.array): The input grid.
        neighbor_coords (set): A set of (row, col) tuples for neighbor cells.

    Returns:
        bool: True if the object is enclosed according to the rules, False otherwise.
    """
    if not neighbor_coords:
        return False  # Object is isolated or fills the grid, cannot be enclosed

    first_neighbor_val = -1 # Initialize with an invalid value

    for r, c in neighbor_coords:
        val = grid[r, c]
        # Condition 1: No neighbor can be background (0)
        if val == 0:
            return False
        # Condition 2: All neighbors must have the same non-zero color
        if first_neighbor_val == -1:
             first_neighbor_val = val # Record the color of the first neighbor
        elif val != first_neighbor_val:
             return False # Found a neighbor with a different color

    # If loop completes, all neighbors have the same non-zero color
    return True


def transform(input_grid):
    """
    Filters the input grid to keep only objects enclosed by exactly one other object.

    Args:
        input_grid (list of lists): The input 2D grid represented as a list of lists.

    Returns:
        list of lists: The transformed 2D grid.
    """
    # Convert input to numpy array for easier processing
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape
    # Initialize output grid with zeros
    output_grid = np.zeros_like(grid)
    # Keep track of visited cells to avoid processing the same object multiple times
    visited = np.zeros_like(grid, dtype=bool)

    # Iterate through each cell in the grid
    for r in range(rows):
        for c in range(cols):
            # If the cell is part of a non-zero object and hasn't been visited yet
            if grid[r, c] != 0 and not visited[r, c]:
                object_color = grid[r, c]
                object_coords = set()
                q = deque([(r, c)]) # Queue for BFS
                visited[r, c] = True

                # Perform BFS to find all connected cells of the same color (the object)
                while q:
                    curr_r, curr_c = q.popleft()
                    object_coords.add((curr_r, curr_c))

                    # Explore 8 neighbors
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue # Skip self
                            nr, nc = curr_r + dr, curr_c + dc

                            # Check boundaries, color match, and visited status
                            if (0 <= nr < rows and 0 <= nc < cols and
                                    not visited[nr, nc] and
                                    grid[nr, nc] == object_color):
                                visited[nr, nc] = True
                                q.append((nr, nc))

                # Find the neighbors of the identified object
                neighbor_coords = _find_neighbors(grid.shape, object_coords)

                # Check if the object is enclosed according to the rules
                if _is_enclosed(grid, neighbor_coords):
                    # If enclosed, copy the object's cells to the output grid
                    for obj_r, obj_c in object_coords:
                        output_grid[obj_r, obj_c] = object_color

    # Convert the output numpy array back to a list of lists
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 2 2 0 3 3 3 3 0 0 0
0 0 2 0 0 0 0 0 0 2 0 3 0 0 3 0 0 0
0 0 2 0 4 4 4 0 0 2 0 3 0 0 3 0 0 0
0 0 2 0 4 0 4 0 0 2 0 3 3 3 3 0 0 0
0 0 2 0 4 4 4 0 0 2 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 2 0 0 6 6 6 0 0 0
0 0 2 2 2 2 2 2 2 2 0 0 6 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 6 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 8
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 7.407407407407419

## Example 2:
Input:
```
0 0 0 0 4 4 4 0 0 0 0 0 0 0 0
6 6 0 0 4 0 4 0 0 0 0 0 0 0 0
6 6 0 0 4 0 4 0 0 0 0 0 0 0 0
0 0 0 0 4 0 4 0 0 0 0 0 0 0 0
0 0 0 0 4 4 4 5 5 5 5 5 5 0 0
7 7 7 0 0 0 0 5 0 0 0 0 5 0 0
7 7 7 0 0 0 0 5 0 3 3 0 5 0 0
7 7 7 0 0 0 0 5 0 3 3 0 5 0 0
0 0 0 0 0 0 0 5 0 0 0 0 5 0 0
0 0 0 0 0 0 0 5 0 0 0 0 5 0 0
0 0 0 0 0 0 0 5 5 5 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 4.444444444444457

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 9 9 9 9 9 0 0
0 0 7 0 0 8 8 8 8 8 8 8 8 8 8 0 7 0 9 0 0 0 9 0 0
0 0 7 0 0 8 0 0 0 0 0 0 0 0 8 0 7 0 9 0 0 0 9 0 0
0 0 7 0 0 8 0 0 3 3 3 3 0 0 8 0 7 0 9 9 9 9 9 0 0
0 0 7 0 0 8 0 0 3 3 3 3 0 0 8 0 7 0 0 0 0 0 0 0 0
0 0 7 0 0 8 0 0 0 0 0 0 0 0 8 0 7 0 3 3 3 3 3 3 3
0 0 7 0 0 8 8 8 8 8 8 8 8 8 8 0 7 0 3 0 0 0 0 0 3
0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 3 0 8 8 8 0 3
0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 3 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 3 3 3 3 0 0 8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 3 3 3 3 0 0 8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 39
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 26.0

Test Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 1 1 1 0 0 0 0 0
0 1 0 0 0 0 0 0 0 1 0 0 0 0 0
0 1 0 2 2 2 2 2 2 1 0 0 0 0 0
0 1 0 2 0 0 0 0 2 1 0 6 6 6 6
0 1 0 2 0 0 0 0 2 1 0 6 0 0 6
0 1 0 2 2 2 2 2 2 1 0 6 0 0 6
0 1 0 0 0 0 0 0 0 1 0 6 0 0 6
0 1 1 1 1 1 1 1 1 1 0 6 6 6 6
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 3 3 3 3 0 0 0 0
0 0 0 3 0 4 4 4 0 0 3 0 6 6 6
0 0 0 3 0 0 0 0 0 0 3 0 6 6 6
0 0 0 3 3 3 3 3 3 3 3 0 6 6 6
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2 0 0 0 0 0 0
0 0 0 2 0 0 0 0 2 0 0 0 0 0 0
0 0 0 2 0 0 0 0 2 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 19
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 16.888888888888886

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 4 0 0 0 0 0 3 0 0 0
0 0 0 0 0 4 0 0 0 4 0 0 0 3 0 3 0 0
0 0 0 0 4 0 0 6 0 0 4 0 3 0 0 0 3 0
0 0 0 4 0 0 6 0 6 0 0 4 0 3 0 3 0 0
0 0 4 0 0 6 0 0 0 6 0 0 4 0 3 0 0 0
0 0 0 4 0 0 6 0 6 0 0 4 0 0 0 0 0 0
0 0 0 0 4 0 0 6 0 0 4 0 0 0 1 0 0 0
0 0 0 0 0 4 0 0 0 4 0 0 0 1 0 1 0 0
0 0 0 0 0 0 4 0 4 0 0 0 1 0 0 0 1 0
0 0 0 0 0 0 0 4 0 0 0 0 0 1 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 8
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 6.349206349206355

## Example 3:
Input:
```
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3
3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3
3 0 2 2 2 2 2 2 2 0 7 7 7 7 7 7 0 3
3 0 2 0 0 0 0 0 2 0 7 0 0 0 0 7 0 3
3 0 2 4 4 4 4 4 2 0 7 0 7 7 7 7 0 3
3 0 2 4 0 0 0 4 2 0 7 0 7 0 7 7 0 3
3 0 2 4 5 5 5 4 2 0 7 0 7 0 7 7 0 3
3 0 2 4 0 0 0 4 2 0 7 0 7 7 7 7 0 3
3 0 2 4 4 4 4 4 2 0 7 0 0 0 0 7 0 3
3 0 2 2 2 2 2 2 2 0 7 7 7 7 7 7 0 3
3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3
3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3
3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 2 0 7 7 7 7 7 7 0 0
0 0 2 0 0 0 0 0 2 0 7 0 0 0 0 7 0 0
0 0 2 4 4 4 4 4 2 0 7 0 7 7 7 7 0 0
0 0 2 4 0 0 0 4 2 0 7 0 7 0 7 7 0 0
0 0 2 4 5 5 5 4 2 0 7 0 7 0 7 7 0 0
0 0 2 4 0 0 0 4 2 0 7 0 7 7 7 7 0 0
0 0 2 4 4 4 4 4 2 0 7 0 0 0 0 7 0 0
0 0 2 2 2 2 2 2 2 0 7 7 7 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 79
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 58.51851851851853
