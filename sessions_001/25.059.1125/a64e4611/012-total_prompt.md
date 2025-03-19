# a64e4611 • 012 • refine_coder

---

Previous Code:
```python
"""
The transformation rule identifies a rectangular region of white (0) pixels enclosed by a rectangular boundary of blue (1) pixels within the input grid. It then replaces the enclosed white pixels with green (3) pixels in the output grid. The blue boundary pixels, and any other pixels outside this boundary, remain unchanged.
"""

import numpy as np

def get_objects(grid, color):
    """
    Find contiguous regions (objects) of a specific color in the grid.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(row, col):
        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or visited[row, col]
            or grid[row, col] != color
        ):
            return []

        visited[row, col] = True
        object_pixels = [(row, col)]

        object_pixels.extend(dfs(row + 1, col))
        object_pixels.extend(dfs(row - 1, col))
        object_pixels.extend(dfs(row, col + 1))
        object_pixels.extend(dfs(row, col - 1))
        return object_pixels

    for row in range(rows):
        for col in range(cols):
            if grid[row, col] == color and not visited[row, col]:
                objects.append(dfs(row, col))

    return objects

def get_bounding_box(obj):
    """
    Returns the bounding box (min_row, min_col, max_row, max_col) of an object or list of pixels.
    """
    min_row = min(pixel[0] for pixel in obj)
    max_row = max(pixel[0] for pixel in obj)
    min_col = min(pixel[1] for pixel in obj)
    max_col = max(pixel[1] for pixel in obj)
    return (min_row, min_col, max_row, max_col)

def is_rectangular_boundary(blue_pixels, rows, cols):
    """
    Checks if the given blue pixels form a complete rectangular boundary.
    """
    if not blue_pixels:
        return False

    min_row, min_col, max_row, max_col = get_bounding_box(blue_pixels)

    # Check if the number of blue pixels matches the perimeter of the rectangle
    expected_count = 2 * (max_row - min_row + 1) + 2 * (max_col - min_col + 1) - 4
    if len(blue_pixels) != expected_count:
        return False
    
    # check the boundary condition
    for r in range(rows):
        for c in range(cols):
            if (r == min_row or r == max_row) and min_col <= c <= max_col:
                if (r,c) not in blue_pixels:
                    return False
            elif (c == min_col or c == max_col) and min_row <= r <= max_row:
                if (r,c) not in blue_pixels:
                    return False

    return True

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find blue pixels
    blue_pixels = []
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 1:
                blue_pixels.append((r, c))

    # Check if blue pixels form a rectangular boundary
    if is_rectangular_boundary(blue_pixels, rows, cols):
        # Get the bounding box of the enclosed region
        min_row, min_col, max_row, max_col = get_bounding_box(blue_pixels)

        # Fill the enclosed white region with green
        for r in range(min_row + 1, max_row):
            for c in range(min_col + 1, max_col):
                if output_grid[r, c] == 0:
                    output_grid[r, c] = 3

    return output_grid
```

Train Set Results:
Okay, let's analyze the results of the code execution on the training examples and refine the natural language program accordingly.

**General Assessment:**

The initial code and natural language program were based on the first training example, which involved a simple rectangular blue boundary enclosing white pixels that were changed to green. The subsequent examples reveal that this initial assumption is too narrow. There are cases with incomplete boundaries, multiple potential boundaries and boundaries within boundaries. The code needs to correctly identify the *outermost* valid, complete rectangular blue boundary and fill only the white pixels enclosed by *that* boundary. The current code doesn't handle incomplete or nested boundaries properly, it fails to handle edge cases.

**Strategy for Resolving Errors:**

1.  **Improve Boundary Detection:** The `is_rectangular_boundary` function needs to be more robust. It should prioritize the *outermost* complete rectangle.
2.  **Handle Incomplete Boundaries:** The logic should not perform any replacement if a complete, rectangular blue boundary is not found.
3.  **Handle Nested Boundaries:** consider only the outermost.
4. **Prioritize outermost boundry**

**Example Analysis and Metrics:**

To understand what went wrong, it is useful to check each of the examples and
compare with the results.

*   **Example 1:** (Correct) The code correctly identified the blue boundary and filled the enclosed white pixels with green.
*   **Example 2:** (Incorrect) There's an incomplete blue rectangle. The current code incorrectly fills a region.
*   **Example 3:** (Incorrect) There are nested blue rectangles. The current program must consider the outer rectangle.
*   **Example 4:** (Incorrect) There is an incomplete outer blue rectangle, with two inner ones.
*   **Example 5:** (Incorrect) There are blue pixels not forming a rectangle and no action should be taken.

**YAML Facts:**

```yaml
examples:
  - example_1:
      status: correct
      objects:
        - type: rectangle
          color: blue
          boundary: complete
          encloses: white pixels
        - type: region
          color: white
          enclosed_by: blue rectangle
      action: replace enclosed white pixels with green
  - example_2:
      status: incorrect
      objects:
        - type: rectangle
          color: blue
          boundary: incomplete
      action: none
  - example_3:
      status: incorrect
      objects:
        - type: rectangle
          color: blue
          boundary: complete
          outermost: true
          encloses: white pixels and another blue rectangle
        - type: rectangle
            color: blue
            boundary: complete
            outermost: false
        - type: region
          color: white
          enclosed_by: outer blue rectangle
      action: replace white pixels enclosed by outermost blue rectangle with green
  - example_4:
      status: incorrect
      objects:
        - type: rectangle
          color: blue
          boundary: incomplete
          outermost: true
      action: none
  - example_5:
      status: incorrect
      objects:
        - type: scattered_pixels
          color: blue
      action: none
```

**Natural Language Program:**

1.  Identify all blue (1) pixels in the input grid.
2.  Determine if the blue pixels form one or more complete rectangles. A complete rectangle has a continuous blue border with no gaps.
3.  If multiple complete blue rectangles are present, select the outermost rectangle. The outermost rectangle is the one that is not contained within any other rectangle.
4. If no or incomplete rectangle are present, do nothing.
5.  If a single, complete, outermost blue rectangle is found, identify the white (0) pixels enclosed within this rectangle.
6.  Replace the enclosed white pixels with green (3) pixels.
7.  Pixels outside the outermost blue rectangle, including the blue pixels forming the rectangle, remain unchanged.

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
