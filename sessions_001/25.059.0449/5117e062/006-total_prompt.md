# 5117e062 • 006 • refine_coder

---

Previous Code:
```python
"""
The transformation rule is to isolate and extract the largest yellow shape from the input grid.
"""

import numpy as np

def find_shapes(grid):
    # Find all contiguous shapes in a grid
    shapes = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, shape_color, current_shape):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != shape_color:
            return
        visited.add((r, c))
        current_shape.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, shape_color, current_shape)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                shape_color = grid[r, c]
                if shape_color != 0: # don't care about blank
                   current_shape = []
                   dfs(r, c, shape_color, current_shape)
                   shapes.append((shape_color, current_shape))
    return shapes

def extract_shape(grid, shape_pixels):
    # Extract a shape defined by its pixels
    min_r = min(r for r, c in shape_pixels)
    max_r = max(r for r, c in shape_pixels)
    min_c = min(c for r, c in shape_pixels)
    max_c = max(c for r, c in shape_pixels)
    extracted_grid = grid[min_r:max_r + 1, min_c:max_c + 1]
    return extracted_grid

def transform(input_grid):
    # Find all shapes in the input grid
    shapes = find_shapes(input_grid)

    # Find yellow shape
    yellow_shapes = [shape for color, shape in shapes if color == 4]

    #select yellow shape
    target_shape_pixels = []
    if (len(yellow_shapes) > 0):
        target_shape_pixels = yellow_shapes[0]  # just select the first one

    if (len(target_shape_pixels) == 0):
        # return zero grid since no yellow
        return np.zeros((1,1), dtype=int)


    # Extract the target shape
    output_grid = extract_shape(input_grid, target_shape_pixels)

    return output_grid
```

Train Set Results:
Okay, let's analyze the results of the previous code execution and refine the natural language program.

**General Assessment:**

The initial code was based on a single example and focused on extracting *a* yellow shape. The results across multiple examples reveal a more specific rule: extracting the *largest* yellow shape. The current code fails when there are multiple yellow shapes or when the yellow shape isn't the largest. It needs to correctly identify and select the largest yellow object, and create a tight bounding box around it.

**Strategy:**

1.  **Improve Shape Selection:** Modify the code to identify all yellow shapes, calculate their sizes (number of pixels), and select the largest one.
2.  **Handle Edge Cases:** Ensure the code gracefully handles cases with no yellow shapes, and ensure return is consistent.
3. **Ensure tight bounding box:** ensure the return grid doesn't include extra rows or columns

**Example and Results Metrics:**

Here's a breakdown of each example, including an assessment of the results:

| Example | Input Shape    | Output Shape   | Expected Shape | Result       | Notes                                                                                                                                        |
| :------ | :------------- | :------------- | :------------- | :----------- | :-------------------------------------------------------------------------------------------------------------------------------------------- |
| 1       | (13, 20)       | (6, 6)       | (6, 6)       | Correct      | The initial example. The largest yellow shape was correctly extracted.                                                                      |
| 2       | (11, 11)       | (1, 1)        | (4, 4)       | Incorrect    | There are two yellow shapes, and the code returned an empty grid. It should have selected and extracted only the largest contiguous yellow object.       |
| 3       | (14, 11)       | (4, 4)         | (4, 4)          | Correct       | Code identifies single yellow object and returns correctly. |

**YAML Facts:**

```yaml
observations:
  - task: "Extract the largest contiguous yellow object from the input grid."
  - objects:
      - name: yellow_shapes
        properties:
          - color: yellow
          - type: contiguous region of pixels
          - size: variable, needs to be determined
      - name: largest_yellow_shape
        properties:
          - derived_from: yellow_shapes
          - selection_criteria: shape with the maximum number of pixels
  - actions:
      - name: find_shapes
        description: Identify all contiguous shapes in the grid, regardless of color.
      - name: filter_yellow_shapes
        description: Select shapes where the color is yellow.
      - name: find_largest_shape
        description: Determine the yellow shape with the maximum number of pixels.
      - name: extract_largest_shape
        description: Create a new grid containing only the pixels of the largest yellow shape, with a tight bounding box.
  - input: 2D grid of colored pixels
  - output: 2D grid containing only the largest contiguous yellow shape from the input, tightly bounding the object.

```

**Natural Language Program:**

1.  **Identify All Shapes:** Scan the input grid to find all contiguous regions of pixels with the same color. Each of these regions is considered a "shape."
2.  **Filter for Yellow Shapes:** From the identified shapes, select only those that are yellow (color value 4).
3. **Find the largest yellow shape** If there are multiple yellow shapes find the one with the largest area (most pixels).
4.  **Extract Largest Shape:** Create a new output grid. Copy *only* the pixels of the largest yellow shape from the input grid to the output grid. Ensure that the output grid tightly bounds the extracted shape, removing any rows or columns that don't contain the yellow shape.
5. **Handle No Yellow:** if no yellow shape is found, return a 1x1 grid with value 0.


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
