# 543a7ed5 • 004 • refine_coder

---

Previous Code:
```python
"""
1.  **Identify Magenta Rectangles:** Locate all rectangular shapes formed by contiguous magenta (6) pixels. These can be either outlines or filled rectangles.

2.  **Outline Modification - color change:** all magenta(6) pixels that are part of rectangles, that do *not* fully enclose azure(8) pixels, become green(3)

3.  **Fill Interior (Conditional):** If a magenta rectangle completely encloses one or more azure(8) pixels, replace azure(8) pixels in its center, with a yellow (4) square. *Center* means the inner object maintains the same rows/cols between all four sides of the outer rectangle.

4. **Background Modification - color change:** all azure(8) pixels adjacent to green(3) and/or yellow(4) pixels, becomes green(3).

5. **No change to azure background**: any azure(8) pixels not adjacent to other colors remain unchanged.
"""

import numpy as np

def find_objects(grid, color):
    objects = []
    visited = set()

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(r, c, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                if current_object:
                    objects.append(current_object)
    return objects

def is_rectangle(obj):
    rows, cols = zip(*obj)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    return len(obj) == (max_row - min_row + 1) * (max_col - min_col + 1)

def get_rectangle_bounds(obj):
    rows, cols = zip(*obj)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    return min_row, max_row, min_col, max_col

def encloses_color(grid, obj, color):
    min_row, max_row, min_col, max_col = get_rectangle_bounds(obj)
    for r in range(min_row + 1, max_row):
        for c in range(min_col + 1, max_col):
            if grid[r,c] == color:
                return True
    return False

def get_center_square(obj):
    min_row, max_row, min_col, max_col = get_rectangle_bounds(obj)
    
    height = max_row - min_row + 1
    width = max_col - min_col + 1

    if height < 3 or width < 3:
        return []  # No center if smaller than 3x3
    
    center_min_row = min_row + 1
    center_max_row = max_row - 1
    center_min_col = min_col + 1
    center_max_col = max_col - 1
    

    # Adjust to the center if there's even size (keep equal size from borders)
    while (center_max_row - center_min_row) > 1:
       center_min_row +=1
       center_max_row -=1
       
    while (center_max_col - center_min_col) > 1:
       center_min_col +=1
       center_max_col -=1

    center_square = []
    for r in range(center_min_row, center_max_row + 1):
        for c in range(center_min_col, center_max_col + 1):
            center_square.append((r, c))
    return center_square

def is_adjacent(grid, r, c, colors):
    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1] and grid[nr, nc] in colors:
            return True
    return False
    

def transform(input_grid):
    output_grid = np.copy(input_grid)
    magenta_objects = find_objects(input_grid, 6)
    rectangles = [obj for obj in magenta_objects if is_rectangle(obj)]
    
    for rect in rectangles:
        #Outline Modification
        if not encloses_color(input_grid, rect, 8):
             for r, c in rect:
                output_grid[r, c] = 3
        #Fill Interior
        if encloses_color(input_grid,rect, 8):
            center_square = get_center_square(rect)
            for r, c in center_square:
                output_grid[r,c] = 4

    #Background Modification
    for r in range(output_grid.shape[0]):
        for c in range(output_grid.shape[1]):
            if output_grid[r,c] == 8:
                if is_adjacent(output_grid, r, c, [3, 4]):
                  output_grid[r,c] = 3

    return output_grid
```

Train Set Results:
Okay, let's analyze the results of the code execution on the training examples and refine the natural language program accordingly.

**General Assessment:**

The initial code and natural language program were a good start, correctly identifying the core concepts of rectangle detection, conditional filling, and adjacency-based color changes. However, the test results reveal some discrepancies, particularly in handling edge cases and the precise definition of "center" and "enclosure," and overlooking that there are rectangle outlines that should not be modified. We need to refine these aspects to achieve perfect matching.

**Strategy for Resolving Errors:**
1.  **Clarify "Enclosure":** Ensure the `encloses_color` function only considers a full enclosure. It must check that azure pixels exist inside the magenta.
2.  **Refine "Center":** It should check for empty space on all four sides.
3. **Preserve Unchanged:** Add an additional check if the magenta rectangle *doesn't* enclose any azure(8).
4.  **Iterative Refinement:** Test the updated code after each modification to isolate the impact of each change.

**Example Analysis and Metrics:**

To understand what's happening, I need to examine the input and output grids and intermediate steps.

```python
def get_grid_string(grid):
    return '\n'.join(''.join(str(cell) for cell in row) for row in grid)

task_data = {
"train": [
    {
      "input": [
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 6, 6, 6, 6, 6, 6, 8, 8, 8],
        [8, 8, 8, 6, 8, 8, 8, 8, 6, 8, 8, 8],
        [8, 8, 8, 6, 8, 8, 8, 8, 6, 8, 8, 8],
        [8, 8, 8, 6, 8, 8, 8, 8, 6, 8, 8, 8],
        [8, 8, 8, 6, 6, 6, 6, 6, 6, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
      ],
      "output": [
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 6, 6, 6, 6, 6, 6, 3, 3, 3],
        [3, 3, 3, 6, 4, 4, 4, 4, 6, 3, 3, 3],
        [3, 3, 3, 6, 4, 4, 4, 4, 6, 3, 3, 3],
        [3, 3, 3, 6, 4, 4, 4, 4, 6, 3, 3, 3],
        [3, 3, 3, 6, 6, 6, 6, 6, 6, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
      ]
    },
    {
      "input": [
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 6, 6, 6, 6, 8, 8, 8, 8],
        [8, 8, 8, 6, 8, 8, 6, 8, 8, 8, 8],
        [8, 8, 8, 6, 8, 8, 6, 8, 8, 8, 8],
        [8, 8, 8, 6, 6, 6, 6, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
      ],
      "output": [
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 3, 3, 3, 3, 8, 8, 8, 8],
        [8, 8, 8, 3, 8, 8, 3, 8, 8, 8, 8],
        [8, 8, 8, 3, 8, 8, 3, 8, 8, 8, 8],
        [8, 8, 8, 3, 3, 3, 3, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
      ]
    },
    {
      "input": [
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 6, 6, 6, 6, 6, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 6, 8, 8, 8, 6, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 6, 8, 8, 8, 6, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 6, 6, 6, 6, 6, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
      ],
      "output": [
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 3, 3, 3, 3, 3, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 3, 8, 8, 8, 3, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 3, 8, 8, 8, 3, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 3, 3, 3, 3, 3, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
      ]
    },
        {
      "input": [
        [6, 6, 6, 6, 6, 6],
        [6, 8, 8, 8, 8, 6],
        [6, 8, 8, 8, 8, 6],
        [6, 8, 8, 8, 8, 6],
        [6, 8, 8, 8, 8, 6],
        [6, 6, 6, 6, 6, 6],
      ],
      "output": [
        [6, 6, 6, 6, 6, 6],
        [6, 4, 4, 4, 4, 6],
        [6, 4, 4, 4, 4, 6],
        [6, 4, 4, 4, 4, 6],
        [6, 4, 4, 4, 4, 6],
        [6, 6, 6, 6, 6, 6],
      ]
    }
  ]
}

import numpy as np

for i in range(len(task_data["train"])):

    input_grid = np.array(task_data["train"][i]["input"])
    expected_output = np.array(task_data["train"][i]["output"])
    predicted_output = transform(input_grid)

    print(f"Example {i+1}:")
    print("Input:")
    print(get_grid_string(input_grid))
    print("Expected Output:")
    print(get_grid_string(expected_output))
    print("Predicted Output:")
    print(get_grid_string(predicted_output))
    print("Match:", np.array_equal(expected_output, predicted_output))
    print("-" * 20)
```

**YAML Facts:**
```yaml
- example_1:
    objects:
        - type: rectangle
          color: magenta (6)
          encloses: azure (8)
          action: fill_center_with_yellow (4)
        - type: background
          color: azure(8)
          adjacent_to: yellow(4), green(3)
          action: change_to_green(3)
- example_2:
  objects:
    - type: rectangle
      color: magenta (6)
      encloses: azure(8)
      action: fill_center_with_yellow(4) #inner part only
      note: center filled based on outline size and maintaining equal padding from the perimeter to inner colors.
    - type: background
      color: azure (8)
      adjacent_to: green(3)
      action: change_color_to_green (3)
    - type: rectangle
      color: magenta(6)
      encloses: nothing
      action: outline changes to green(3)
- example_3:
  objects:
     - type: rectangle
       color: magenta (6)
       encloses: None
       action: change_outline_to_green(3)
     - type: background
       color: azure (8)
       adjacent_to: green(3)
       action: change_color_to_green(3)
- example_4:
    objects:
        - type: rectangle
          color: magenta (6)
          encloses: azure (8)
          action: fill_center_with_yellow (4)
```

**Natural Language Program:**

1.  **Identify Magenta Rectangles:** Locate all rectangular shapes formed by contiguous magenta (6) pixels.

2.  **Conditional Outline Modification:**
    *   If a magenta rectangle *does not* enclose any azure (8) pixels, change all its magenta (6) pixels to green (3).
    *   If a magenta rectangle *does* enclose one or more azure (8) pixels, proceed to step 3, but do not change it's outline to green.

3.  **Conditional Center Filling:** If a magenta rectangle completely encloses one or more azure (8) pixels, replace the "center" azure (8) pixels with a yellow (4) square. The "center" is defined as the largest possible square of azure pixels within the magenta rectangle, maintaining equal distance from all four sides of the outer magenta rectangle. If an equal distance cannot be created because the rectangle's inner area is not large enough, then do not fill.

4.  **Background Color Change:** Any azure (8) pixel that is directly adjacent (horizontally or vertically, not diagonally) to a green (3) or yellow (4) pixel is changed to green (3).

5. **Preserve Unchanged:** any azure(8) pixels not adjacent to other colors remain unchanged, and any magenta(6) rectangles that enclose other colors, remain unchanged.

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
