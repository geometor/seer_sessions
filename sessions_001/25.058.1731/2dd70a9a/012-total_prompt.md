# 2dd70a9a • 012 • refine_coder

---

Previous Code:
```python
"""
Find a connected set of azure pixels in the region of row 4, left-side, and change its value (color) to green.
"""

import numpy as np

def find_connected_region(grid, start_row, start_col, color):
    # Find a connected region of a given color, starting from a given cell.
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    region = []

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return
        visited[r, c] = True
        region.append((r, c))

        # Explore adjacent cells
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    dfs(start_row, start_col)
    return region

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find the connected region of azure (8) pixels starting around the fourth row.
    start_row = 3
    start_col = None
    
    #search along row 4 for first azure(8) pixel, to use for recursive search seed.
    for c in range(cols):
        if input_grid[start_row, c] == 8:
            start_col = c
            break
    
    if start_col is None:
        return output_grid #return early if no azure found
    
    connected_region = find_connected_region(input_grid, start_row, start_col, 8)

    # Flood fill the connected region with green (3)
    for r, c in connected_region:
        output_grid[r, c] = 3

    return output_grid
```

Train Set Results:
Okay, let's analyze the results of running the previously generated code on the training examples and refine our natural language program and observations accordingly.

**General Assessment and Strategy**

The initial code was based on the first training example, aiming to find a connected region of azure pixels starting from the fourth row and changing them to green. While this worked for the first example, it failed on the second and third. The primary issue is the assumption that the relevant azure region *always* starts on the fourth row. The second and third examples show this isn't true. The connected component can exist in any area of the input.

The strategy for resolving the errors is to:

1.  **Remove the Row Constraint:** The code incorrectly assumes the azure region starts on row 4. We need to search the *entire* grid for azure pixels, not just row 4.
2.  **Handle Multiple Azure Regions:** There might be multiple disconnected azure regions. The current code only handles the first one found. We must decide if all are changed, only the biggest or smallest, or use another heuristic.
3.  **Handle missing azure:** One example did not have any azure pixels.

**Metrics and Observations from Examples**

Here's a breakdown of each example, including observations:

*   **Example 1:**
    *   Input Shape: (9, 9)
    *   Output Shape: (9, 9)
    *   Transformation: A connected region of azure (8) pixels starting at (3, 0) is changed to green (3). The rest remains the same.
    *   Code Result: **Success**. The code correctly identified and transformed the azure region.
*   **Example 2:**
    *   Input Shape: (7, 7)
    *   Output Shape: (7, 7)
    *   Transformation: A connected region of azure (8) pixels starting at (0, 0) is changed to green (3). The rest remains the same.
    *   Code Result: **Failure**. The code didn't find any azure pixels on the fourth row, so no changes are made to the output.
*   **Example 3:**
    *   Input Shape: (7, 11)
    *   Output Shape: (7, 11)
    *   Transformation: input contains only black and yellow. All azure pixels are changed to green
    *   Code Result: **Failure**. there is no connected region of azure, so no change to green

**YAML Facts**

```yaml
facts:
  - description: |
      The task involves changing the color of a connected region of azure pixels to green.
  - input_objects:
      - object_id: azure_region
        color: azure (8)
        shape: connected region
        properties:
          - can vary in size and location
          - must be contiguous
  - output_objects:
      - object_id: green_region
        color: green (3)
        shape: connected region, same shape as input azure region
        properties:
          - replaces the azure region
  - actions:
      - action_id: find_azure
        description: Locate a connected region of azure pixels. Start point is not fixed to a specific row.
      - action_id: change_color
        description: Change the color of the found azure region to green.
```

**Natural Language Program**

1.  **Search:** Iterate through all pixels of the input grid.
2.  **Identify Azure:** If an azure (8) pixel is found, start a depth-first search (DFS) or breadth-first search (BFS) to find the entire connected region of azure pixels.
3.  **Transform:** Change all pixels within the identified connected region to green (3).
4.  **Repeat or Stop:** If there can be more regions to change, the description needs more information. For now stop.
5.  **Output:** Return the modified grid.
6.  **Edge case - no azure.** If no azure is present, return input grid.

**INSTRUCTIONS**

- generate a Python module to represent the natural language program 
- follow the template below
- all common math and science libraries are available
- create docstring only at top - but comment the workflow in the function
- use helper functions for common operations like finding objects, counting,
  measuring, moving, etc. 

remember - we are working iteratively - so this code will inform your future
self as we converge on the solution

*template:*

```python
"""
{{ natural language description of the transformation rule }}
"""

{{ imports }}

def transform(input_grid):
    # initialize output_grid

    # change output pixels 

    return output_grid

```
