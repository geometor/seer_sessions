# b2862040 • 020 • example_3 • investigate_coder

---

## train_3

**input:**
```
9 9 9 9 9 1 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 1 9 9 9 9
9 9 1 9 9 9 9 1 1 1 1 9 9
9 1 1 1 1 9 9 9 1 9 9 9 9
9 1 9 9 1 9 9 9 1 9 9 9 9
9 1 1 1 1 9 9 9 1 1 1 9 9
9 9 9 9 1 9 9 9 9 9 9 9 9
9 9 9 9 1 9 9 9 9 9 9 9 9
9 1 9 9 9 9 9 1 1 1 9 9 9
1 1 1 9 9 9 9 9 9 1 9 9 9
9 1 9 9 9 9 1 9 1 1 9 9 9
1 1 9 9 9 9 1 1 1 9 9 9 9
```

<PIL.Image.Image image mode=RGB size=832x768 at 0x7FC253CC7850>

**output:**
```
9 9 9 9 9 1 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 1 9 9 9 9
9 9 8 9 9 9 9 1 1 1 1 9 9
9 8 8 8 8 9 9 9 1 9 9 9 9
9 8 9 9 8 9 9 9 1 9 9 9 9
9 8 8 8 8 9 9 9 1 1 1 9 9
9 9 9 9 8 9 9 9 9 9 9 9 9
9 9 9 9 8 9 9 9 9 9 9 9 9
9 1 9 9 9 9 9 1 1 1 9 9 9
1 1 1 9 9 9 9 9 9 1 9 9 9
9 1 9 9 9 9 1 9 1 1 9 9 9
1 1 9 9 9 9 1 1 1 9 9 9 9
```

<PIL.Image.Image image mode=RGB size=832x768 at 0x7FC253CC7D50>
Okay, here's a breakdown of my observations and a proposed natural language program for the transformation:

**Perception of Elements:**

*   **Input:** A 2D grid of pixels, primarily maroon (9) and blue (1). There are distinct shapes formed by the blue pixels.
*   **Output:** The same grid as the input, but with some of the maroon (9) pixels adjacent to blue (1) pixels changed to grey(8).
*    The shapes are maintained.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      - colors: [maroon, blue, grey]
      - dimensions: [12, 13]
  - type: shape
    properties:
      - color: blue
      - composition: contiguous blue pixels
  - type: pixel
    properties:
      - color: [maroon, blue, grey]
      - position: [row, column]

actions:
  - name: change_color
    agent: system
    target: pixel
    precondition:
      - target.color == maroon
      - adjacent.color == blue #at least one adjacent
    postcondition:
      - target.color == grey

relationships:
  - type: adjacency
    between: [pixel, pixel]
    definition: pixels sharing a side (not diagonal)
```


**Natural Language Program:**

1.  **Identify** all maroon (9) pixels in the input grid.
2.  **For each** maroon (9) pixel, **check** if it is directly adjacent (above, below, left, or right, *not* diagonally) to at least one blue (1) pixel.
3. **If** a maroon pixel is adjacent to a blue pixel, **change** its color to grey (8).
4.  **Otherwise**, leave the maroon pixel's color unchanged.
5. All blue pixels remain unchanged.
6.  The output grid is the result of these color changes.

Essentially it's drawing an outline around the shapes in a different color.

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
