# 72ca375d • 002 • example_1 • investigate_coder

---

## Example 1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0
0 0 2 2 2 0 0 7 7 0
0 0 0 0 0 0 7 0 7 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 6 0 0 0
0 0 0 0 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7B1DDE699850>

**output:**
```
6 6 6 6
0 6 6 0
```

<PIL.Image.Image image mode=RGB size=256x128 at 0x7B1DDE6E0C50>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Task Elements:**

The task involves transforming a larger grid (input) into a smaller grid (output). The input grid contains various colored squares (represented by digits 0-9). The output grid seems to be a specific extraction or summary of a particular color/object within the input grid. In this example, the focus appears to be on the magenta (6) colored object.

**YAML Block - Facts:**


```yaml
objects:
  - name: input_grid
    type: grid
    properties:
      - dimensions: 10x10
      - values: [0, 2, 6, 7]
      - description: Contains multiple colored regions.
  - name: output_grid
    type: grid
    properties:
      - dimensions: 2x4
      - values: [0, 6]
      - description: Contains a subset of a single color from the input grid.
  - name: magenta_region
    type: object
    properties:
      - color: magenta (6)
      - shape: irregular rectangle
      - location:
        - row_start: 6
        - row_end: 7
        - col_start: 3
        - col_end: 6
    relationships:
        contains:  The relationship between what determines what is in the output
            and the colors or positions of the elements
actions:
  - name: extract
    description: Isolates a specific region/object from the input grid.
    parameters:
      - color: magenta (6)
```


**Natural Language Program:**

1.  **Identify the Target Object:** Locate the largest contiguous block of magenta (6) colored pixels in the input grid.
2.  **Determine Bounding Box:** Find the minimum and maximum row and column indices that completely enclose the magenta pixels.
3.  **Extract Sub-grid:** Create a new grid (the output grid) consisting of all the magenta pixels.
4. **Fill Surrounding Area:** Add white (0) to the grid, surrounding any cells that are empty.

In essence, the program extracts the largest magenta (6) object from the input, and represents a rectangle of where it was on the screen.

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
