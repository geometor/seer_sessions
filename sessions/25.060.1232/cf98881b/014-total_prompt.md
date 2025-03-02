# cf98881b • 014 • refine_coder

---

Previous Code:
```python
"""
1. **Find the Anchor:** Locate the top-leftmost yellow (color value 4) pixel within the input grid. This pixel serves as the anchor point for the transformation.
2.  **Attempt Subgrid Extraction:** Attempt to extract a 4x4 subgrid from the input grid. The top-left corner of this subgrid should be the location of the anchor pixel found in step 1.
3.  **Boundary Check:** Before extracting the subgrid, check if a 4x4 area starting at the anchor point would extend beyond the boundaries of the input grid.
4.  **Conditional Output:**
    *   If the 4x4 subgrid can be extracted without exceeding the input grid's boundaries, the output grid is this extracted subgrid.
    *   If extracting the 4x4 subgrid would exceed the boundaries, the output grid is an empty grid (0x0).
"""

import numpy as np

def find_top_leftmost_color(grid, color):
    # Iterate through the grid to find the top-leftmost occurrence of the specified color.
    for r_idx, row in enumerate(grid):
        for c_idx, pixel in enumerate(row):
            if pixel == color:
                return (r_idx, c_idx)
    return None  # Return None if the color is not found.

def transform(input_grid):
    # Convert input_grid to a NumPy array.
    input_grid = np.array(input_grid)

    # Find the top-leftmost yellow pixel (color 4).
    top_left_corner = find_top_leftmost_color(input_grid, 4)

    # If no yellow pixel is found, return an empty grid.
    if top_left_corner is None:
        return np.zeros((0, 0), dtype=int)

    # Attempt to extract the 4x4 subgrid.
    start_row, start_col = top_left_corner
    end_row = start_row + 4
    end_col = start_col + 4

    # Boundary check: If subgrid exceeds input_grid bounds, return 0x0 grid.
    if end_row > input_grid.shape[0] or end_col > input_grid.shape[1]:
        return np.zeros((0, 0), dtype=int)

    # Extract and return the subgrid.
    output_grid = input_grid[start_row:end_row, start_col:end_col]
    return output_grid.tolist()
```

Train Set Results:
Okay, let's analyze the results of the provided code on the training examples and refine the natural language program accordingly.

**General Assessment and Strategy**

The initial natural language program and the corresponding code focused on finding a yellow pixel as an anchor and extracting a 4x4 subgrid. This approach works for some cases but fails when the 4x4 subgrid exceeds the input grid's boundaries, or more importantly, it is revealed by example 2 that the sub-grid size is flexible. The current strategy is too rigid. We need to adapt the program to handle cases where:

1.  A yellow pixel may not exist.
2.  The size of extracted subgrid is dynamic, not fixed to 4x4. It should be determined by the input, not hardcoded.
3.  Boundary conditions when extracting the grid

The primary strategy is to iteratively refine the observations and hypothesis by examining each example, identifying the shortcomings of the current code, and updating the natural language program to encompass all observed behaviors. We need to determine the subgrid's dimension dynamically, not hardcoded it as 4x4.

**Metrics and Observations**

Here's a breakdown of each training example, the expected output, the actual output from the code, and the resulting assessment:

*   **Example 1:**
    *   Input: 9x9 grid with a yellow pixel at (1, 2).
    *   Expected Output: 4x4 subgrid starting at (1, 2).
    *   Actual Output: 4x4 subgrid starting at (1, 2).
    *   Assessment: Correct. The current code handles this case.

*   **Example 2:**
    *    Input: 8x7 grid with a yellow pixel at (6,1)
    *    Expected Output: 2x5 subgrid, as it is the largest subgrid including the
    *   yellow pixel.
    *    Actual Output: 0x0 empty grid because the selected top left yellow does not have the space for a 4x4 square below and to its right.
    *    Assessment: **Incorrect.** The current logic fails. The size and starting point are not correctly determined, because 4x4 is not appropriate, it does not specify the rule to generate the dimension.

*   **Example 3:**
    *   Input: 3x3 grid with no yellow pixel
    *    Expected Output: An empty grid, shown as 0x0.
    *    Actual Output: 0x0 empty grid.
    *   Assessment: Correct. The current code's `find_top_leftmost_color` will correctly return None.

**YAML Fact Block**

```yaml
facts:
  - object: input_grid
    type: 2D array
    properties:
      - contains: pixels (integers 0-9 representing colors)
      - dimensions: variable (rows x columns)
  - object: output_grid
    type: 2D array
    properties:
      - contains: pixels
      - dimensions: variable, potentially smaller than input_grid or empty (0x0)
  - object: anchor_pixel
    type: pixel
    properties:
      - color: yellow (4)
      - location: top-leftmost occurrence of yellow in input_grid
    actions:
        if anchor exist:
            - description: Extract a subgrid, starting at the anchor pixel.
            - dimensions: Not fixed. It is the largest possible subgrid starting at the anchor pixel.
        if anchor does not exist:
            - description: return an empty grid 0x0.
```

**Natural Language Program**

1.  **Find Anchor:** Search for the top-leftmost yellow (color value 4) pixel within the input grid. This pixel will be the anchor point. If no yellow pixel is found, return an empty (0x0) grid.

2.  **Determine Subgrid Dimensions:** If a yellow pixel is found, determine the largest possible rectangular subgrid that can be formed, where anchor is part of the subgrid.

3.  **Extract Subgrid:** Extract this subgrid from the input grid.

4. **Return the subgrid.**

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
