# 8403a5d5 • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7D67CBE7AA50>

**output:**
```
0 0 0 0 0 3 5 3 0 3
0 0 0 0 0 3 0 3 0 3
0 0 0 0 0 3 0 3 0 3
0 0 0 0 0 3 0 3 0 3
0 0 0 0 0 3 0 3 0 3
0 0 0 0 0 3 0 3 0 3
0 0 0 0 0 3 0 3 0 3
0 0 0 0 0 3 0 3 0 3
0 0 0 0 0 3 0 3 0 3
0 0 0 0 0 3 0 3 5 3
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7D67CBE7A950>
Okay, here's my analysis of the provided input-output example pair.

**Perception of Elements:**

The input is a 10x10 grid mostly filled with white (0) pixels, except for a single green (3) pixel near the bottom. The output grid maintains the same dimensions but has a more complex structure. It seems to be based on the location of the original green pixel. Specifically a vertical and horizontal lines of '3' pixels. Some of cells are '5'

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    dimensions: 10x10
    elements: pixels
    properties:
      - color:
          values: [0, 3, 5]
          mapping:
            0: white
            3: green
            5: gray

  - type: pixel
    properties:
      - color
      - position (row, column)

actions:
  - name: locate_green_pixel
    input: input_grid
    output: (row, column) of green pixel
    
  - name: draw_vertical_line
    input: output_grid, column, color (green=3)
    behavior: draw a filled vertical line green at a fixed column

  - name: draw_horizontal_line
    input: output_grid, row, color
    behavior: draw a filled horizontal line green at a fixed row

  - name: replace_pixel
    input: position, color
    behavior: set position pixel

relationships:
  - type: spatial
    description: The green pixel in the input grid determines the intersection point of the lines in the output grid.
```


**Natural Language Program:**

1.  **Find the green pixel:** Locate the single green (3) pixel in the input grid. Note its row and column.
2.  **Draw green lines**: In the output grid, draw a vertical line and a horizontal line of green (3) pixels.
    *   The vertical line is at the same column as the original green pixel in
        the input.
    *   The Horizontal line is at the same row as the original green pixel in
        the input.
    *   All cells of lines will have value of 3, no empty values.
3.  **Add Gray Highlights**: Add gray (5) pixels in two location:
    *   replace original green pixel location with '5'
    *   replace cell at (row, column) where column = original_column - 1


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
