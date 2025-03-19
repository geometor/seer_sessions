# 1bfc4729 • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7EE11FF53110>

**output:**
```
6 6 6 6 6 6 6 6 6 6
6 0 0 0 0 0 0 0 0 6
6 6 6 6 6 6 6 6 6 6
6 0 0 0 0 0 0 0 0 6
6 0 0 0 0 0 0 0 0 6
7 0 0 0 0 0 0 0 0 7
7 0 0 0 0 0 0 0 0 7
7 7 7 7 7 7 7 7 7 7
7 0 0 0 0 0 0 0 0 7
7 7 7 7 7 7 7 7 7 7
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7EE11FF52F30>
Okay, let's analyze this input-output example pair.

**Perception of Elements:**

*   The input is a 10x10 grid of single-digit integers (0-9), representing colors.
*   The output is also a 10x10 grid of single-digit integers.
*   The input grid contains two distinct non-zero values: 6 (magenta) at position (2,2) and 7 (orange) at position (7,7). All other cells are 0 (white).
*   The output grid expands the 6 and 7 values, creating a frame/border effect. The expansion creates a cross shape with color 6 and a cross shape, and the original positions are maintained. The areas are bordered by original colored pixels.

**YAML Block (Facts):**


```yaml
objects:
  - id: grid_input
    type: grid
    dimensions: 10x10
    elements: integers (0-9)
    description: Input grid with two non-zero pixels.

  - id: grid_output
    type: grid
    dimensions: 10x10
    elements: integers (0-9)
    description: Output grid with expanded non-zero pixels.

  - id: pixel_6
    type: pixel
    value: 6
    original_position: (2, 2)
    description: Magenta pixel in the input.

  - id: pixel_7
    type: pixel
    value: 7
    original_position: (7, 7)
    description: Orange pixel in the input.

actions:
  - name: expand_pixel
    agent: system
    target: pixel_6
    result: horizontal and vertical expansion
    notes: creates two lines of the color 6, one horizontal and another one vertical at the original position

  - name: expand_pixel
    agent: system
    target: pixel_7
    result: horizontal and vertical expansion.
    notes: creates two lines of the color 7, one horizontal and another one vertical at the original position

relationships:
  - type: spatial
    relation: between pixel_6 and pixel_7 expansion
    description: expanded lines do not intersect

```


**Natural Language Program:**

1.  Identify all non-zero pixels in the input grid.
2.  For each non-zero pixel:
    *   Create a horizontal line of the same color, extending across the entire row of the pixel's original position.
    *    Create a vertical line of the same color, extending across the entire column of the pixel's original position.
3.  Combine the expanded lines to form the output grid. If a pixel location is altered by more than one expansion, maintain the original non-zero value.

Essentially, each non-zero pixel "projects" a cross of its color onto the output grid, and areas that belong to expansions of two different colors are painted by the color present in the original grid.

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
