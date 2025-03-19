# 025d127b • 016 • refine_coder

---

Previous Code:
```python
"""
Identify a connected shape of azure (8) pixels within the input grid.  Preserve a specific part of the outer edge of the shape. Clear all other azure pixels to white (0).
"""

import numpy as np

def get_azure_shape(grid):
    """Finds the connected azure shape and returns its coordinates."""
    azure_pixels = np.argwhere(grid == 8)
    if azure_pixels.size == 0:
        return []

    # Create a set for easier membership checking and to avoid duplicates
    shape_coords = set()

    # Start with the first azure pixel found
    stack = [tuple(azure_pixels[0])]

    while stack:
        current_pixel = stack.pop()
        shape_coords.add(current_pixel)

        # Check neighbors (up, down, left, right)
        row, col = current_pixel
        neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]

        for neighbor_row, neighbor_col in neighbors:
            if (0 <= neighbor_row < grid.shape[0] and
                0 <= neighbor_col < grid.shape[1] and
                grid[neighbor_row, neighbor_col] == 8 and
                (neighbor_row, neighbor_col) not in shape_coords):
                stack.append((neighbor_row, neighbor_col))
    return list(shape_coords)


def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    output_grid = np.copy(input_grid)
    azure_shape_coords = get_azure_shape(output_grid)
    
    # If there's no azure shape, return the input grid as is
    if not azure_shape_coords:
      return output_grid

    # Create a set for quick lookup
    azure_set = set(azure_shape_coords)

    # Iterate through the azure pixels and apply the "preserve edge" rule.
    for r in range(output_grid.shape[0]):
        for c in range(output_grid.shape[1]):
          if (r,c) not in azure_set:
              continue
          #keep one, remove one approach          
          if (r >=1 and c>=1 and c < output_grid.shape[1]-2):
              if(output_grid[r,c] ==8):
                  output_grid[r-1,1] = 8  

    for r in range(output_grid.shape[0]):
        for c in range(output_grid.shape[1]):
          if (r,c) not in azure_set:
            continue
          if (r >=1 and c>=1):
              if output_grid[r,c] == 8 and (r,c) != (r-1,1):
                  output_grid[r,c] = 0


    return output_grid
```

Train Set Results:
Here's an analysis of the provided examples and results, along with a strategy for updating the natural language program and code:

**General Assessment:**

The initial code correctly identifies connected azure (8) shapes. However, the "preserve edge" logic is flawed and doesn't accurately capture the intended transformation. The "keep one, remove one" approach is too simplistic and based on an incorrect assumption about where to keep the azure pixel. The examples show a consistent pattern of preserving a specific *corner* of the azure shape, not just an arbitrary edge pixel. The strategy needs to shift from preserving an arbitrary edge to identifying and preserving the correct corner pixel.

**Strategy:**

1.  **Refine Shape Identification:** The `get_azure_shape` function is working correctly, so we can keep it.
2.  **Corner Identification:** Instead of a generic edge preservation, we need to determine the specific corner pixel to keep. By observing the provided examples, we can discern if a rule will let use determine which corner pixel will be preserved.
3.  **Precise Clearing:** After identifying the corner, clear *all other* azure pixels.
4.  Test and iterate using an improved Natural Language Program.

**Example Analysis and Metrics:**

To understand the pattern, let's analyze each example using a simplified representation focusing on the azure shapes and their transformation. We'll denote the preserved pixel with `[x]`.

*   **Example 1:**

    ```
    Input:       Output:
    8 8 8        0 0 0
    8 8 8  ->    0 0 0
    8 8 8        8 0 0
    ```
*   **Example 2:**

    ```
    Input:       Output:
    8 8          0 8
    8 8    ->    0 0
    ```
*   **Example 3:**

    ```
    Input:       Output:
    8 8 8 8      0 0 0 8
    8 8 8 8  ->  0 0 0 0
    ```
*   **Example 4:**
    ```
    Input:       Output:
        8 8           0 8
        8 8     ->    0 0
    8 8 8 8       0 0 0 0
    ```
*   **Example 5:**
    ```
    Input:       Output:
    8 8 8          0 0 8
      8 8    ->    0 0 0
    ```
From a visual review it appears as if the preserved pixel is the top-right
pixel of the azure colored object.

**YAML Facts:**

```yaml
objects:
  - name: azure_shape
    color: azure (8)
    type: connected_shape
    properties:
      - corners: [top_left, top_right, bottom_left, bottom_right]

actions:
  - name: identify_shape
    description: Locate the connected azure shape in the grid.
  - name: identify_corner
    description: Determine the top-right corner of the azure shape.
  - name: preserve_corner
    description: Keep the identified top-right corner pixel as azure.
  - name: clear_other
    description: Change all other azure pixels within the shape to white (0).
```

**Natural Language Program:**

1.  **Identify:** Find the connected shape of azure (8) pixels in the input grid.
2.  **Locate Top-Right Corner:** Within the identified shape, locate the top-right corner pixel. The top-right corner is defined as the pixel within the shape that has the maximum column index and, among pixels with the same maximum column index, has the minimum row index.
3.  **Preserve:** Keep the color of the top-right corner pixel as azure (8).
4.  **Clear:** Change the color of all other azure pixels in the shape to white (0).

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
