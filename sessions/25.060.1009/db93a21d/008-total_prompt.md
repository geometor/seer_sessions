# db93a21d • 008 • refine_coder

---

Previous Code:
```python
"""
1.  **Identify Maroon Squares:** Find all maroon (9) squares in the input grid. Note their size (which can vary).
2.  **Outline Maroon Squares:** Create a green (3) outline, one pixel thick, around each identified maroon square. The outline should be directly adjacent to the maroon square on all four sides (top, bottom, left, right).
3. **Fill Green outline:** Convert each outlined green area to be a solid green rectangle with the same extent.
4.  **Find Bottom-Most Green Rectangle:** Determine the green rectangle that is positioned lowest in the grid. If there are multiple at the same vertical level, no operation. If no green rectangles are found - no operation.
5.  **Create Blue Rectangle:** Create a 2x6 blue (1) rectangle. Position the top-left corner of this rectangle directly to the right of the *bottom-most* green rectangle.
6. **Output**: output the modified grid.
"""

import numpy as np

def find_squares(grid, color):
    """Finds all squares of a given color, regardless of size."""
    squares = []
    for size in range(1, min(grid.shape) + 1):
        for r in range(grid.shape[0] - size + 1):
            for c in range(grid.shape[1] - size + 1):
                if np.all(grid[r:r+size, c:c+size] == color):
                    squares.append((r, c, size))
    return squares

def outline_square(grid, r, c, size, color):
    """Creates a one-pixel thick outline around a square."""
    # Top
    if r > 0:
        grid[r-1, c:c+size] = color
    # Bottom
    if r + size < grid.shape[0]:
        grid[r+size, c:c+size] = color
    # Left
    if c > 0:
        grid[r:r+size, c-1] = color
    # Right
    if c + size < grid.shape[1]:
        grid[r:r+size, c+size] = color
    return grid

def fill_rectangle(grid, r, c, height, width, color):
    """Fills a rectangular region with a specified color."""
    grid[r:r+height, c:c+width] = color
    return grid

def find_green_rectangle_from_outline(grid, r, c, size):
    """Finds top-left corner of the filled green rect from outlined square."""
    
    outline_r = r - 1
    outline_c = c - 1
    outline_height = size + 2
    outline_width = size + 2
    return (outline_r, outline_c, outline_height, outline_width)
    

def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    output_grid = np.copy(input_grid)

    # 1. Identify Maroon Squares
    maroon_squares = find_squares(output_grid, 9)

    # 2. Outline Maroon Squares
    for r, c, size in maroon_squares:
        output_grid = outline_square(output_grid, r, c, size, 3)

    # 3. Fill Green Outlines
    for r, c, size in maroon_squares:
        green_r, green_c, green_h, green_w = find_green_rectangle_from_outline(output_grid,r,c,size)
        output_grid = fill_rectangle(output_grid, green_r, green_c, green_h, green_w, 3)

    # 4. Find Bottom-Most Green Rectangle
    green_rectangles = []

    for r, c, size in maroon_squares:
        gr, gc, gh, gw = find_green_rectangle_from_outline(output_grid,r,c,size)
        green_rectangles.append((gr,gc,gh,gw))


    if not green_rectangles:
        return output_grid

    bottom_most_y = -1
    bottom_most_rect = None
    
    for r, c, h, w in green_rectangles:
        bottom_y = r + h
        if bottom_y > bottom_most_y:
            bottom_most_y = bottom_y
            bottom_most_rect = (r, c, h, w)
        elif bottom_y == bottom_most_y: # multiple at same level
             return output_grid

    if bottom_most_rect is None: return output_grid

    # 5. Create Blue Rectangle
    blue_r = bottom_most_rect[0]
    blue_c = bottom_most_rect[1] + bottom_most_rect[3]

    if blue_c < output_grid.shape[1]:  # Check for out-of-bounds
       output_grid = fill_rectangle(output_grid, blue_r, blue_c, 6, 2, 1)

    return output_grid
```

Train Set Results:
Here's an analysis of the provided code and results, along with a strategy for improvement:

**General Assessment and Strategy**

The initial code correctly identified the core concept: finding maroon squares, outlining them in green, filling the outlines, and placing a blue rectangle. However, the validation revealed a key flaw in determining the placement of the blue rectangle. It consistently chose the *bottom-most* green rectangle. Examples show that the position of the added rectangle should depend on all others.

**Strategy:**

1.  **Refine Rectangle Selection:** Instead of just looking for bottom most, identify *all* green rectangles formed, and place the blue shape based on the properties of the set of all green shapes.

**Example Metrics and Analysis**

To analyze the examples, I'll manually inspect them (since I can't execute code). I'll focus on:

*   Number of maroon squares.
*   Sizes of maroon squares.
*   Result of outlining and filling.
*   Expected position of the blue rectangle vs. actual (in cases of error).

Here's a summary based on manual inspection and the provided results:

*   **Example 1:** Correct. One 2x2 maroon square, outlined and filled to 4x4 green, blue rectangle placed correctly.
*   **Example 2:** Incorrect. One 3x3 maroon square. Outlined and filled correctly. Blue placed to the right of bottom-most, but should be on *top*.
*  **Example 3:** Incorrect. Two maroon squares, a 2x2 and 1x1. Outlined and correctly. Blue placed to the right of bottom-most, but there are *two* green regions on bottom.

**YAML Facts**

```yaml
example_1:
  input:
    maroon_squares:
      - location: [5, 0]
        size: 2x2
  output:
    green_rectangles:
      - location: [4, -1]
        size: 4x4
    blue_rectangle:
      - location: [4, 3]
        size: 2x6
        relative_position: "right of green rectangle"

example_2:
  input:
    maroon_squares:
      - location: [2, 3]
        size: 3x3
  output:
    green_rectangles:
      - location: [1, 2]
        size: 5x5
    blue_rectangle:
        location: [1,7]
        size: 2x6
        relative_position: "right of green"

example_3:
  input:
    maroon_squares:
      - location: [6, 0]
        size: 2x2
      - location: [3, 4]
        size: 1x1
  output:
    green_rectangles:
      - location: [5, -1]
        size: 4x4
      - location: [2, 3]
        size: 3x3
    blue_rectangle:
      - location: [5,3]
        size: 6x2
        relative_position: "right of bottom-most green, incorrect"
```

**Natural Language Program**

1.  **Identify Maroon Squares:** Locate all maroon (9) squares within the input grid.
2.  **Outline Maroon Squares:** Enclose each maroon square with a one-pixel thick green (3) outline.
3.  **Fill Green outline:** Convert each outlined green area to be a solid green rectangle with the same extent.
4. **Find Green Rectangles:** find *all* green rectangles. If no green, return the input.
5.  **Create Blue Rectangle:**
    - if *one* green rectangle, blue is 2x6 to the right
    - if *two* green rectangles, blue is 6x2 and centered horizontally on right edge of green
    - if more than two, no change (assume)
6. **Output**: return the modified grid.

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
