# 963e52fc • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
2 3 3 2 3 3 2
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x320 at 0x7F4C1B67F8D0>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 3 3 2 3 3 2 3 3 2 3 3 2 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=896x320 at 0x7F4C1B67E450>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves two grids: an input grid and an output grid. Both grids contain single-digit integers (0-9), representing different colors. The primary colors observed are white (0), red (2), and green (3). The input grid appears to have a single horizontal line of alternating red and green pixels, while the surrounding pixels are white. The output grid seems to be an expansion of this line.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      - name: input_grid
      - dimensions: 5x7
      - colors: [0, 2, 3]
  - type: grid
    properties:
      - name: output_grid
      - dimensions: 5x14
      - colors: [0, 2, 3]
  - type: line
    properties:
      - color_sequence: [2, 3, 3, 2, 3, 3, 2]
      - orientation: horizontal
      - row: 3
      - start_column: 1 # 0 indexed
      - end_column: 7 # exclusive

actions:
  - type: expand
    object: line
    properties:
      - factor: 2
      - direction: horizontal

relationships:
  - type: contains
    from: input_grid
    to: line
  - type: corresponds_to
    from:  input_grid
    to: output_grid
```


**Natural Language Program:**

1.  **Identify the colored line:** Locate the single horizontal line of non-white pixels in the input grid. Note its row index, starting and ending column indices, and the sequence of colors.
2.  **Expand the line:** Duplicate the line's color pattern horizontally to the right by repeating the entire sequence.
3.  **Construct the output grid:** Create a new grid with double the width of original line, while the vertical dimension and other lines with color white (0) remains the same. Copy expanded pattern onto the output grid in the same row as the input grid.

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
