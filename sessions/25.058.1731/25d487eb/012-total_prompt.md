# 25d487eb • 012 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 8 8 8 0 0 0 0
0 0 0 0 8 8 8 8 8 0 0 0
0 0 0 8 8 8 3 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=768x768 at 0x7C36044BF750>

**output:**
```
0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 8 8 8 0 0 0 0
0 0 0 0 8 8 8 8 8 0 0 0
0 0 0 8 8 8 3 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=768x768 at 0x7C36044BF550>
Okay, here's my analysis of the provided input-output example, focusing on perception, object identification, and the transformation rule.

**Perception of Elements:**

The input and output are 12x12 grids. The primary colors involved are white (0), azure (8), and green (3). The input grid contains an "arrowhead" or "triangle" shape composed of azure (8) pixels, with a single green (3) pixel at its base, all surrounded by white (0) pixels.  The output grid is identical to the input except with 5 green (3) pixels in a vertical line segment starting above the arrowhead.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    dimensions: 12x12
    elements: pixels
    colors: [white, azure, green]

  - type: shape
    name: arrowhead
    color: azure
    base_color: green
    position: center-left, extends towards the center

  - type: line_segment
    color: green
    start:
        row: 0
        column: 6 # counting from 0
    end:
        row: 4
        column: 6
    length: 5

relationships:
  - type: above
    object1: line_segment
    object2: arrowhead

actions:
  - type: add
    object: line_segment
    properties:
      color: green
      location: above arrowhead, vertically aligned with base

```


**Natural Language Program:**

1.  **Identify the Arrowhead:** Locate the contiguous "arrowhead" shape formed by azure (8) pixels.
2.  **Locate the Base:** Identify the green (3) pixel at the base of the arrowhead.
3. **Determine target column.** The column that intersects with the base of the arrowhead.
4.  **Draw Vertical Line:** Starting from the top row (row 0) of the grid, in target column, replace white (0) pixels with five green (3) pixels, and stop. All other pixels remain the same.

In essence, the transformation adds a vertical green line of 5 pixels extending upwards from above the "arrowhead" shape's base, aligned with the column of that base pixel.

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
