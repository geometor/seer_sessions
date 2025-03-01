# 25d487eb • 004 • refine_coder

---

Previous Code:
```python
"""
1. **Identify the Base Shape:** Locate the largest contiguous, non-rectangular colored shape in the input grid. This is our "base shape". Note its original color or colors.
2. **Determine Extension Direction:**
   - If train example 1, the base_shape has a horizontal shape, extend horizontally.
   - If train example 2, the base_shape has a vertical shape.  Extend vertically.
   -  If train example 3, extend a vertical shape of color 2.
3. **Extend the Shape:**
   - If the base_shape has a horizontal component and does not have a vertical component. Extend the shape horizontally across the entire grid.
   - If the base_shape has a a vertical component and a horizontal component. Add a shape to extend vertically below it.
"""

import numpy as np

def find_base_shape(grid):
    """Finds the 'base shape' in the grid."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    base_shape = []
    max_size = 0

    def dfs(r, c, color, current_shape):
        """Depth-first search to find contiguous shapes."""
        if (
            r < 0
            or r >= rows
            or c < 0
            or c >= cols
            or visited[r, c]
            or grid[r, c] != color
        ):
            return
        visited[r, c] = True
        current_shape.append((r, c))
        dfs(r + 1, c, color, current_shape)
        dfs(r - 1, c, color, current_shape)
        dfs(r, c + 1, color, current_shape)
        dfs(r, c - 1, color, current_shape)

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] != 0:
                current_shape = []
                dfs(r, c, grid[r, c], current_shape)
                if len(current_shape) > max_size:
                    max_size = len(current_shape)
                    base_shape = current_shape
    return base_shape

def has_horizontal_component(shape):
    """Checks if the shape has a horizontal component."""
    if len(shape) < 2:
        return False
    
    rows = [r for r, _ in shape]
    cols = [c for _, c in shape]
    return len(set(cols)) > 1 and len(set(rows)) <= len(set(cols))

def has_vertical_component(shape):
    """Checks if the shape has a vertical component"""
    if len(shape) < 2:
        return False;

    rows = [r for r, _ in shape]
    cols = [c for _, c in shape]
    return len(set(rows)) > 1 and len(set(cols)) <= len(set(rows))

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""
    grid = np.array(input_grid)  # Convert to NumPy array for easier manipulation
    output_grid = grid.copy()
    rows, cols = grid.shape

    base_shape = find_base_shape(grid)

    #Determine Extension Direction and Extend
    if has_horizontal_component(base_shape) and not has_vertical_component(base_shape):
        #horizontal extension
        color = 1 #hard code for now - based on shape, need to improve.
        row_index = base_shape[0][0]
        for c in range(cols):
            output_grid[row_index,c] = color

    elif has_vertical_component(base_shape) or (has_horizontal_component(base_shape) and has_vertical_component(base_shape)):
        #vertical extension
        color = 0
        
        #get color from shape
        for r,c in base_shape:
            if grid[r,c] != 0:
                color = grid[r,c]
                break;

        #find single color shapes
        for r in range(rows):
            for c in range(cols):
                if grid[r,c] != 0:
                    shape = find_base_shape(np.array([[grid[r,c]]]))
                    if len(shape) == 1:
                         color = grid[r,c]

        #extend
        if color > 0:
            min_col = min(c for _, c in base_shape)
            max_col = max(c for _, c in base_shape)

            if color == 8 or color == 3:
                for r in range(rows):
                    output_grid[r,min_col] = color
            elif color == 2:
                for r in range(rows):
                   output_grid[r,min_col] = 2
            elif color == 1:
                row_index = base_shape[0][0]
                for c in range(min_col,cols):
                    output_grid[row_index,c] = 1


    return output_grid.tolist()
```

Train Set Results:
Here's an analysis of the training examples, the code's performance, and a revised natural language program:

**General Assessment:**

The initial code was a good starting point, focusing on identifying a "base shape" and extending it. However, it oversimplified the rules and made incorrect assumptions about color and direction. The results show that the code works for some cases (horizontal extension in the first example) but fails to generalize to other examples.  The key is to correctly identify the object and extension rules.

**Strategy for Resolving Errors:**

1.  **Improve Shape Identification:** The `find_base_shape` function currently just finds the *largest* shape, which isn't always correct. We need to refine the criteria for selecting the shape to be extended and consider other factors, like the object interactions and adjacency of color blocks.
2.  **Conditional Extension:** The extension logic needs to be more sophisticated. It shouldn't always be a full horizontal or vertical extension. The direction and extent of the extension depend on the specific shapes and their relationships.
3.  **Color Handling:**  Hardcoding the color (like `color = 1`) is incorrect.  The output color is often, *but not always*, related to the input shape's color. We need to derive the output color based on the input.

**Example Analysis and Metrics:**

To accurately analyze each example, let's define some helper functions to collect information:

```python
import numpy as np

def grid_to_string(grid):
    return '\n'.join([''.join(map(str, row)) for row in grid])

def analyze_example(input_grid, output_grid, predicted_grid):
    input_str = grid_to_string(input_grid)
    output_str = grid_to_string(output_grid)
    predicted_str = grid_to_string(predicted_grid)

    input_objects = identify_objects(input_grid)
    output_objects = identify_objects(output_grid)
    
    print(f"**Input Grid:**\n{input_str}\n")
    print(f"**Expected Output Grid:**\n{output_str}\n")
    print(f"**Predicted Output Grid:**\n{predicted_str}\n")
    print(f"**Input Objects:**\n{input_objects}\n")
    print(f"**Output Objects:**\n{output_objects}\n")
    print(f"**Correct Prediction:** {np.array_equal(output_grid, predicted_grid)}\n")
    print("---")

def identify_objects(grid):
    """Identifies objects (contiguous blocks of non-zero color) in a grid."""
    grid = np.array(grid)
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []

    def dfs(r, c, color, current_object):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
                visited[r, c] or grid[r, c] != color or color == 0):
            return
        visited[r, c] = True
        current_object.append((r, c))
        dfs(r + 1, c, color, current_object)
        dfs(r - 1, c, color, current_object)
        dfs(r, c + 1, color, current_object)
        dfs(r, c - 1, color, current_object)

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] != 0:
                current_object = []
                dfs(r, c, grid[r, c], current_object)
                if current_object:  # Avoid empty objects
                    objects.append({
                        "color": grid[r, c],
                        "pixels": current_object,
                        "size": len(current_object)
                    })
    return objects

#Example data - from the prompt
train = [
    [
        [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    ],
    [
        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    ],
    [
        [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 8, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 8, 0, 0], [0, 0, 0, 0, 8, 0, 0], [0, 0, 0, 0, 8, 0, 0], [0, 0, 0, 0, 8, 0, 2], [0, 0, 0, 0, 0, 0, 0]]
    ],
    [
       [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 0, 0, 0, 0], [0, 0, 0, 0, 3, 0, 0, 0, 0], [0, 0, 0, 0, 3, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    ]
]

#Iterate and analyze results
for i, (input_grid, output_grid) in enumerate(train):
    predicted_grid = transform(input_grid)  # Use the provided transform function
    print(f"Train Example {i+1}:")
    analyze_example(input_grid, output_grid, predicted_grid)
```
```output
Train Example 1:
**Input Grid:**
000000000
000000000
000000000
000000000
000010000
000000000
000000000
000000000
000000000

**Expected Output Grid:**
000000000
000000000
000000000
000000000
111111111
000000000
000000000
000000000
000000000

**Predicted Output Grid:**
000000000
000000000
000000000
000000000
111111111
000000000
000000000
000000000
000000000

**Input Objects:**
[{'color': 1, 'pixels': [(4, 4)], 'size': 1}]

**Output Objects:**
[{'color': 1, 'pixels': [(4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8)], 'size': 9}]

**Correct Prediction:** True
---
Train Example 2:
**Input Grid:**
000000000000000
000000000000000
000000000000000
000008000000000
000008000000000
000008000000000
000000000000000
000000000000000

**Expected Output Grid:**
000000000000000
000000000000000
000000000000000
000008000000000
000008000000000
000008000000000
000008000000000
000008000000000

**Predicted Output Grid:**
000000000000000
000000000000000
000000000000000
000008000000000
000008000000000
000008000000000
000000000000000
000000000000000

**Input Objects:**
[{'color': 8, 'pixels': [(3, 5), (4, 5), (5, 5)], 'size': 3}]

**Output Objects:**
[{'color': 8, 'pixels': [(3, 5), (4, 5), (5, 5), (6, 5), (7, 5)], 'size': 5}]

**Correct Prediction:** False
---
Train Example 3:
**Input Grid:**
0000000
0000000
0000800
0000000
0000000
0000002
0000000

**Expected Output Grid:**
0000000
0000000
0000800
0000800
0000800
0000802
0000000

**Predicted Output Grid:**
0000000
0000000
0000800
0000800
0000800
0000002
0000000

**Input Objects:**
[{'color': 8, 'pixels': [(2, 4)], 'size': 1}, {'color': 2, 'pixels': [(5, 6)], 'size': 1}]

**Output Objects:**
[{'color': 8, 'pixels': [(2, 4), (3, 4), (4, 4), (5, 4)], 'size': 4}, {'color': 2, 'pixels': [(5, 6)], 'size': 1}]

**Correct Prediction:** False
---
Train Example 4:
**Input Grid:**
000000000
000000000
000000000
000000000
000000000
000030000
000000000
000000000
000000000

**Expected Output Grid:**
000000000
000000000
000000000
000000000
000030000
000030000
000030000
000000000
000000000

**Predicted Output Grid:**
000000000
000000000
000000000
000000000
000000000
000030000
000030000
000030000
000000000

**Input Objects:**
[{'color': 3, 'pixels': [(5, 4)], 'size': 1}]

**Output Objects:**
[{'color': 3, 'pixels': [(4, 4), (5, 4), (6, 4)], 'size': 3}]

**Correct Prediction:** False
---
```

**YAML Facts:**

```yaml
examples:
  - example_id: 1
    input_objects:
      - color: 1
        shape: single_pixel
        location: center
    output_objects:
      - color: 1
        shape: horizontal_line
        location: same_row_as_input
    transformation: extend_horizontally
  - example_id: 2
    input_objects:
      - color: 8
        shape: vertical_line
        location: center_column
    output_objects:
      - color: 8
        shape: vertical_line
        location: same_column_as_input, extended_down
    transformation: extend_vertically_down
  - example_id: 3
    input_objects:
      - color: 8
        shape: single_pixel
        location: center_column
      - color: 2
        shape: single_pixel
        location: bottom_right
    output_objects:
      - color: 8
        shape: vertical_line
        location: same_column_as_input, extended_down
      - color: 2
        shape: single_pixel #remains
        location: bottom_right #remains
    transformation: extend_first_object_vertically_down
  - example_id: 4
    input_objects:
      - color: 3
        shape: single_pixel
        location: center
    output_objects:
      - color: 3
        shape: vertical_line
        location: same_column, extended_vertically
    transformation: extend_vertically

```

**Natural Language Program:**

1.  **Identify Target Object:** Find the *first* non-zero colored object encountered when scanning the grid from top-to-bottom, left-to-right. Consider this object and it's color.
2.  **Determine Extension Direction:**
    *   If the object is a single pixel or a vertical line, extend vertically downwards.
    *   If the object is a horizontal line, extend horizontally.
3.  **Extend:**
    *   **Vertical Extension:** Extend the object downwards, creating a vertical line of the same color. The new line should occupy the same column(s) as the original object, extending to the bottom edge of the grid (if extending down), unless obstructed by another object. If the object has more than one pixel, extend all pixels to the bottom of the grid.
    *   **Horizontal Extension:** Extend the object, creating a horizontal line of the same color across the entire row.
4. **Other Objects** Any objects below the first encountered object remain unchanged.

This improved natural language program considers the object scanning order, clarifies the extension direction, and handles cases where another object might influence the behavior (example 3).

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
