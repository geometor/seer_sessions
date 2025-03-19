# beb8660c • 002 • example_3 • investigate_coder

---

## train_1

**input:**
```
0 2 2 0 0 0 0
0 0 0 0 3 0 0
1 1 1 0 0 0 0
0 0 0 0 0 0 0
0 5 5 5 5 5 5
0 0 0 0 0 0 0
6 6 6 6 6 0 0
0 0 0 4 4 4 4
0 0 0 0 0 0 0
8 8 8 8 8 8 8
```

<PIL.Image.Image image mode=RGB size=448x640 at 0x7F4C231A8AD0>

**output:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 3
0 0 0 0 0 2 2
0 0 0 0 1 1 1
0 0 0 4 4 4 4
0 0 6 6 6 6 6
0 5 5 5 5 5 5
8 8 8 8 8 8 8
```

<PIL.Image.Image image mode=RGB size=448x640 at 0x7F4C231A9ED0>

## train_2

**input:**
```
0 0 0 1
0 0 0 0
2 2 2 0
0 0 0 0
0 3 3 0
0 0 0 0
8 8 8 8
```

<PIL.Image.Image image mode=RGB size=256x448 at 0x7F4C231ABC50>

**output:**
```
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 1
0 0 3 3
0 2 2 2
8 8 8 8
```

<PIL.Image.Image image mode=RGB size=256x448 at 0x7F4C231A8E50>

## train_3

**input:**
```
2 2 0
0 4 0
8 8 8
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7F4C231AA8D0>

**output:**
```
0 0 4
0 2 2
8 8 8
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7F4C231AB150>
<PIL.Image.Image image mode=RGB size=1024x1360 at 0x7F4C231AA9D0>Okay, here's my analysis of the provided input-output examples, focusing on perception, object identification, and the transformation rule.

**Perception of Elements:**

The task involves 2D grids of colored pixels. The colors are represented by single-digit integers (0-9). The most prominent feature is the rearrangement of colored horizontal lines.  It appears lines of the same color are being treated as single objects. Empty space (represented by 0) acts as padding/filler. The general layout and sizes of the grids seems variable.

**YAML Fact Documentation:**


```yaml
facts:
  - type: object
    description: Horizontal lines of uniform color.
    properties:
      - color: Integer value (0-9) representing the color.
      - length: Number of pixels in the line.
      - start_position: (row, col) coordinates of the leftmost pixel.

  - type: grid
    description: 2D array of pixels.
    properties:
      - height: Number of rows.
      - width: Number of columns.

  - type: action
    description: Line reordering.
    properties:
      -  reordering_logic: "Lines appear to be stacked from bottom to top in reverse order of initial appearance(or by their top-left coordinate)."

  - type: relationship
    description: Input grid transforms to output grid.
    properties:
        - transformation_type: line_reordering

```


**Natural Language Program:**

1. **Identify Objects:** Find all horizontal lines of contiguous pixels with the same color in the input grid. Treat each of these lines as a single object.
2. **Sort/Reorder:** Sort the identified lines based on the order they appear in the input, processing the grid row by row from top to bottom and moving left to right within each row. Reverse the sorted order
3. **Stack:** Stack the lines on top of each other from bottom to top. Fill empty pixels on top by 0.
4.  **Output Grid:** Create the output grid by arranging these reordered, stacked lines.

In simpler terms: The transformation takes the horizontal colored lines from the input, reverses their order of appearance from top-left to bottom-right, and stacks them at the bottom of the output grid. The remaining space at the top is filled with 0.

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
