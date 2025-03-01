# ef135b50 • 014 • refine_coder

---
```python
"""
1.  **Identify Red Objects:** Locate all contiguous regions (objects) of red (2) pixels in the input grid.
2.  **Identify Concavities:** Inspect the non-red pixels adjacent to each red object. A concavity is identified when a non-red pixel is orthogonally adjacent to at least three red pixels of a single object.
3.  **Fill Concavities with Maroon:** Change the color of the identified non-red pixels within identified concavities to maroon (9).
4. **Preserve All Other Pixels** Ensure all other pixels retain their original values.
"""

import numpy as np

def get_objects(grid, color):
    """
    Find connected regions of a specific color.
    Returns a list of sets, where each set contains the (row, col) coordinates of a connected region.
    """
    visited = set()
    objects = []

    def dfs(row, col, current_object):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or (row, col) in visited
            or grid[row, col] != color
        ):
            return
        visited.add((row, col))
        current_object.add((row, col))
        # Check adjacent cells (up, down, left, right)
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and (row, col) not in visited:
                current_object = set()
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def identify_concavities(grid, red_objects):
    """
    Identifies concavities within red objects.
    A concavity is a non-red pixel orthogonally adjacent to at least three red pixels of the same object.
    """
    concavities = []
    for obj in red_objects:
        # Create a set for faster lookup
        obj_set = set(obj)
        for row in range(grid.shape[0]):
            for col in range(grid.shape[1]):
                if grid[row, col] != 2:  # Check non-red pixels
                    neighbors = 0
                    # Count red neighbors belonging to the current object
                    if (row - 1, col) in obj_set:
                        neighbors += 1
                    if (row + 1, col) in obj_set:
                        neighbors += 1
                    if (row, col - 1) in obj_set:
                        neighbors += 1
                    if (row, col + 1) in obj_set:
                        neighbors += 1
                    if neighbors >= 3:
                        concavities.append((row, col))
    return concavities

def transform(input_grid):
    # Initialize output grid
    output_grid = np.copy(input_grid)

    # Find red objects
    red_objects = get_objects(input_grid, 2)

    # Identify concavities
    concavities = identify_concavities(output_grid, red_objects)

    # Fill concavities with maroon
    for row, col in concavities:
        output_grid[row, col] = 9

    return output_grid
```

