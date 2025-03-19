# 8731374e • 018 • refine_coder

---

Previous Code:
```python
"""
Extract a cross-shaped subgrid from a larger input grid. The cross is formed by red (2) pixels, and the background is azure (8).
"""

import numpy as np

def find_cross_center(grid):
    # Find the center of the cross pattern
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r,c] == 2:
              if is_cross_center(grid, r, c):
                return (r, c)
    return None

def is_cross_center(grid, r, c):
    # check cross pattern existence with current center
    rows, cols = grid.shape
    
    # Check horizontal
    if not (0< c < cols -1 and grid[r,c-1] == 2 and grid[r, c+1] == 2):
        return False
        
    # Check vertical
    if not (0 < r < rows - 1 and grid[r-1,c] == 2 and grid[r+1, c] == 2):
        return False    
    
    return True

def get_cross_dimensions(grid, center_row, center_col):
    # get full dimensions of the cross

    rows, cols = grid.shape
    
    # Horizontal
    left = center_col
    while left >= 0 and grid[center_row, left] == 2:
        left -= 1
    right = center_col
    while right < cols and grid[center_row, right] == 2:
        right += 1
        
    # Vertical
    up = center_row
    while up >= 0 and grid[up, center_col] == 2:
        up -= 1
    down = center_row
    while down < rows and grid[down, center_col] == 2:
        down += 1

    return (up, down, left, right)

def transform(input_grid):
    # Convert input to numpy array
    grid = np.array(input_grid)

    # Find the center of the cross
    center = find_cross_center(grid)
    if center is None:
        return [[]] # Return empty grid if no cross is found

    center_row, center_col = center

    # Get cross boundaries
    up, down, left, right = get_cross_dimensions(grid, center_row, center_col)

    # Determine output grid size, adding the surrounding 8s
    out_up = up -1
    out_down = down + 1
    out_left = left - 2
    out_right = right + 2
    
    
    # boundary checks
    out_up = max(0, out_up)
    out_left = max(0, out_left)
    out_down = min(grid.shape[0], out_down)
    out_right = min(grid.shape[1], out_right)
   

    # Extract subgrid
    output_grid = grid[out_up:out_down, out_left:out_right]

    return output_grid.tolist()
```

Train Set Results:
Okay, let's analyze the provided code, training results, and examples to refine the natural language program and address the discrepancies.

**General Assessment and Strategy**

The current code focuses on identifying a red (2) cross within an azure (8) background and extracting a subgrid around it. The code does a pretty good job on the example it was designed for and captures subsequent examples well, with some small errors. The strategy to resolve these is to:

1.  **Analyze the Boundary Conditions:** The main area of focus for improvement lies in the boundary conditions of the extracted subgrid. The current code uses hard coded offset, but some examples need different offsets.
2. **Dynamic offsets** Update the code to adjust offsets dynamically

**Metrics and Observations**

Here's a breakdown of each example, focusing on what the code *currently* does and how it relates to the expected output.

**Example 1**

*   **Input:** 9x11 grid.
*   **Expected Output:** 5x7 grid.
*   **Actual Output:** 5x7 grid.
*   **Observation:** The code correctly identifies and extracts the cross, including the immediate azure border and an additional column of azure on the left.

**Example 2**

*   **Input:** 11x15 grid.
*   **Expected Output:** 7 x 9 grid.
*   **Actual Output:** 7x9 grid
*   **Observation:** No issues found.

**Example 3**

*   **Input:** 10x13 grid.
*   **Expected Output:** 5x7 grid.
*    **Actual Output:** 5x7 grid
*   **Observation:** No issues found.

**Example 4**

*   **Input:** 8x9 grid.
*   **Expected Output:** 7x9 grid
*    **Actual Output:** 7x8
*   **Observation:** It appears there is a consistent off-by-one error in output grid width

**YAML Fact Documentation**

```yaml
facts:
  - object: cross
    color: red (2)
    shape: cross-shaped, defined by connected red pixels
    properties:
      - has_center: True
      - center_pixel_value: 2
  - object: background
    color: azure (8)
    shape: rectangular
    properties:
      - surrounds: cross
  - action: extract
    subject: cross
    object: subgrid
    precondition:
        - background of azure surrounding the cross
    properties:
      - includes_border: True
      - border_color: azure (8)
      - border_size: "variable, at least one azure pixel on the top, bottom and left"
      - "left_border: two azure pixels"

```

**Natural Language Program**

1.  **Identify the Cross:** Locate the red (2) cross-shaped object within the input grid. A cross is defined as a central red pixel with directly adjacent red pixels to its top, bottom, left, and right, forming a '+' shape.

2.  **Find the Center:** Determine the center of the cross, which is the red pixel with four adjacent red neighbors.

3. **Determine cross boundaries:** Get the coordinates of the cross boundaries.

4.  **Determine Output Grid Size:** The output grid should include the entire cross and a border of azure (8) pixels.
    *   The border will include at least one pixel on the top, bottom, and right.
    *   The left border should extend to include at least 2 pixels.

5.  **Extract Subgrid:** Extract the subgrid from the input grid based on calculated dimensions.

6.  **Handle Missing Cross:** If no cross is found, return an empty grid.

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
