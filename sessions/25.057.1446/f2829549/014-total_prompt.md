# f2829549 • 014 • example_3 • investigate_coder

---

## Example 3

**input:**
```
0 7 7 1 5 0 0
0 0 7 1 0 5 5
0 7 0 1 5 5 0
0 0 7 1 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x256 at 0x786C548159D0>

**output:**
```
0 0 0
3 0 0
0 0 3
3 3 0
```

<PIL.Image.Image image mode=RGB size=192x256 at 0x786C54814C50>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Elements:**

The task involves transforming a grid of colored pixels (represented by digits 0-9) into another, smaller grid of colored pixels. The colors in the input and output grids seem to follow the standard ARC color mapping. The output grid appears to be related to specific vertical lines detected within the input grid. In this example the line of blue pixels transforms into a line of green pixels at an offset.

**YAML Fact Block:**


```yaml
facts:
  - type: grid
    description: Input grid with dimensions 4x7.
    properties:
      - colors: Contains colors 0 (white), 7 (orange), 1 (blue), and 5 (gray).
      - pattern: Vertical line of 1 (blue).
      - objects: 4 objects are the columns of colors 7, 1, 5, and a two-element
        object of color 5 at (row, col) (1,5) and (2,5)
  - type: grid
    description: Output grid with dimensions 4x3.
    properties:
      - colors: Contains colors 0 (white) and 3 (green).
      - pattern: A vertical column of green appears in columns with alternating green
        and white pixels.
      - objects: 1 column of color 3.
  - type: transformation
    description: The transformation extracts and alters a specific feature from the input grid.
    actions:
      - detect: Identify the vertical line composed of blue(1) pixels.
      - translate:  create new column for each detected column, the new column is
        offset by +1 row
      - recolor: Change the color of the detected line from blue (1) to green (3).

```


**Natural Language Program:**

1.  **Identify Target Line:** Locate the vertical column in the input grid consisting of the color blue (1).

2.  **Create Output Grid:** Initialize a new grid with the same number of rows as the input grid, with a column for each column located and set all values to white (0).

3.  **Translate Column:** For each target, add a new column to the output at a row index +1 from the input.

4.  **Recolor Pixels:** Replace each pixel in the output that came from the target to green (3).

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
