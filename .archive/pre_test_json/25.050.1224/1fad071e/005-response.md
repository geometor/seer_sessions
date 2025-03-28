# 1fad071e • 005 • example_3 - NLP

---
Okay, let's analyze the third example.

**YAML Observation**

```yaml
input_grid:
  size: [9, 9]
  objects:
    blue:
      - shape: square
        positions: [[0, 3], [0, 4], [1, 3], [1, 4]]
      - shape: square
        positions: [[1, 7], [1, 8], [2, 7], [2, 8]]
      - shape: single
        positions: [[1,1]]
      - shape: square
        positions: [[4,4], [4,5], [5,4], [5,5]]
      - shape: single
        positions: [[4,7]]
      - shape: square
        positions: [[7,1], [7,2], [8,1], [8,2]]
      - shape: single
        positions: [[8,5]]
    red:
      - shape: square
        positions: [[0, 0], [0, 1], [1, 0], [1, 1]]
      - shape: square
        positions: [[3, 1], [3, 2], [4, 1], [4, 2]]
      - shape: single
        positions: [[6,4]]
      - shape: square
        positions: [[7,7],[7,8], [8,7], [8,8]]

    white:
      - shape: background
        positions: all other cells
```

**Natural Language Program**

Here's a step-by-step description of the transformation:

1.  **Identify Objects:** The input grid contains objects of color blue, red, and white. We are only interested in blue objects.

2.  **Predicate:** The predicate of interest is object order based on a top-to-bottom, left-to-right scan.

3. **Filter Objects:**  Select the first two blue objects, scanning the cells from top to bottom and from left to right.
    - [[0, 3], [0, 4], [1, 3], [1, 4]]
    - [[1, 7], [1, 8], [2, 7], [2, 8]]

4.  **Extract a Property:** List the unique x-coordinates occupied by selected blue objects.
      - [3,4]
      - [7,8]

5.  **Build the output:** Create an output of length equal to the double of the previous list plus one. Put 1 in each cell of the output that have index included in the list, and zero otherwise.

**Transformation Rule Summary**

The transformation is identical to the first and second example.
The new rule is:
   - scanning the grid from left to right and from top to bottom.
   - selecting the first two blue objects.
   - extracting the x-coordinates of their cells.
   - removing duplicates,
   - creating a new grid 1 row grid
   - setting its values to 1 when their index exists in the x-coordinates list or 0 otherwise.

```python
"""
The transformation is identical to the first and second example.
The new rule is:
   - scanning the grid from left to right and from top to bottom.
   - selecting the first two blue objects.
   - extracting the x-coordinates of their cells.
   - removing duplicates,
   - creating a new grid 1 row grid
   - setting its values to 1 when their index exists in the x-coordinates list or 0 otherwise.
"""

import numpy as np

def get_objects(grid, color):
    """
    Find objects of a specific color in the grid.
    Returns a list of lists of coordinates.
    """
    objects = []
    visited = set()

    def is_valid(x, y):
        return 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]

    def dfs(x, y, current_object):
        if (x, y) in visited or not is_valid(x, y) or grid[x, y] != color:
            return
        visited.add((x, y))
        current_object.append((x, y))
        
        # Explore adjacent cells
        dfs(x + 1, y, current_object)
        dfs(x - 1, y, current_object)
        dfs(x, y + 1, current_object)
        dfs(x, y - 1, current_object)

    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if grid[x, y] == color and (x, y) not in visited:
                current_object = []
                dfs(x, y, current_object)
                objects.append(current_object)
    return objects

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    # Find blue objects
    blue_objects = get_objects(input_grid, 1)

    # Select the first two blue objects
    selected_objects = blue_objects[:2]

    # Extract x-coordinates
    x_coordinates = []
    for obj in selected_objects:
        for x, y in obj:
            x_coordinates.append(y)

    # Remove duplicates
    unique_x_coordinates = sorted(list(set(x_coordinates)))

    #create output grid
    output_length = len(unique_x_coordinates)*2+1
    output_grid = np.zeros(output_length, dtype=int)

    #set 1
    for x in unique_x_coordinates:
      output_grid[x] = 1

    return output_grid.reshape(1,-1)
```

