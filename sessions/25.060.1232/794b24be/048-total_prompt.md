# 794b24be • 048 • refine_coder

---

Previous Code:
```python
"""
The transformation rule is as follows:

1.  Identify the top row of the input grid.
2.  Change the color of all pixels in the top row to red.
3. All other pixels not in the top row should stay white.
4.  The output grid is the result of this transformation.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as all white (0) with the same dimensions as the input_grid
    output_grid = np.zeros_like(input_grid)

    # Get the dimensions of the grid
    rows, cols = input_grid.shape

    # Iterate through the columns of the top row (row 0)
    for j in range(cols):
        # Change the color of all pixels in the top row to red (2)
        output_grid[0, j] = 2

    return output_grid
```

Train Set Results:
Okay, let's analyze the results of the previous code execution and refine the natural language program and approach.

**General Assessment and Strategy**

The initial code was too specific, focusing solely on making the top row red. While this worked for the first example, the subsequent examples reveal a more general pattern: a single horizontal line of a specific color is being drawn. The strategy should be to identify the color and row index of this line in the input and replicate it in the output. The rest of the output grid should remain white.

**Metrics and Observations**

Here's an analysis of each example:

*   **Example 1:**
    *   Input: 3x3 grid, various colors.
    *   Output: 3x3 grid, top row is red, rest is white.
    *   Result: **Success**. The code correctly identified the top row and colored it red.
*   **Example 2:**
    *   Input: 5x5 grid, various colors.
    *   Output: 5x5 grid, 3rd row (index 2) is blue, rest is white.
    *   Result: **Failure**. The code incorrectly colored the top row red.
*   **Example 3:**
    *   Input: 6x6 grid, various colors.
    *   Output: 6x6 grid, 4th row (index 3) is green, rest is white.
    *   Result: **Failure**. The code incorrectly colored the top row red.

**YAML Facts**

```yaml
examples:
  - example_1:
      input_objects:
        - object_1: {type: grid, dimensions: 3x3, colors: [various]}
      output_objects:
        - object_1: {type: grid, dimensions: 3x3, colors: [red, white], description: "Top row red, rest white."}
      transformation: "Identify the top row in the input. Change all pixels in the top row to red. Other pixels remain white."
      result: "Success"
  - example_2:
      input_objects:
        - object_1: {type: grid, dimensions: 5x5, colors: [various]}
      output_objects:
         - object_1: {type: grid, dimensions: 5x5, colors: [blue, white], description: "Third row blue, rest white"}
      transformation: "Identify a horizontal line in input by finding the row where all non-white pixels have same color. Recreate single color horizontal line in output, all other pixels are white."
      result: "Failure"
  - example_3:
      input_objects:
       - object_1: {type: grid, dimensions: 6x6, colors: [various]}
      output_objects:
        - object_1: {type: grid, dimensions: 6x6, colors: [green, white], description: "Fourth row green, rest white"}
      transformation: "Identify a horizontal line in input by finding the row where all non-white pixels have same color. Recreate single color horizontal line in output, all other pixels are white."
      result: "Failure"
```

**Natural Language Program**

1.  **Identify the Solid Horizontal Line:** Find the single row in the input grid that contains a contiguous horizontal line of pixels that are a single non-white color. The row can be determined because all pixels that are not white have the same color.
2. **Get Line Attributes**: Note the row index and the non-white color of this line.
3.  **Reconstruct:** Create an output grid of the same dimensions as the input grid, filled entirely with white (color 0).
4.  **Draw Line:** In the output grid, color all pixels in the identified row with the identified color.
5. All other pixels in the output grid remain white.

This revised program accounts for the variations observed across all three training examples. It moves from a specific rule (top row, red) to a more general rule (single-color horizontal line at any row).

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
