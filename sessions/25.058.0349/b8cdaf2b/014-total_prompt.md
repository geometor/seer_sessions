# b8cdaf2b • 014 • example_3 • investigate_coder

---

## Example 3

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 6 6 6 0
6 1 1 1 6
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x76911E9AEB70>

**output:**
```
0 0 0 0 0
0 0 0 0 0
1 0 0 0 1
0 6 6 6 0
6 1 1 1 6
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x76911EE1F930>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Elements:**

The task involves a grid of colored pixels. The primary colors observed are white (0), magenta (6), and blue (1). The input grid appears to have a pattern involving horizontal lines of magenta and blue, bordered by white. The output grid seems to maintain the bottom two rows (magenta and blue) and modifies the area above. Specifically, it introduces two blue pixels at the corners of the third row from the bottom, leaving the rest of the top part as white.

**YAML Block (Facts):**


```yaml
objects:
  - name: grid
    type: 2D array
    properties:
      rows: 5
      columns: 5
      colors: [0, 1, 6]
  - name: horizontal_line_magenta
    type: object
    properties:
      color: 6
      row_index: 3
  - name: horizontal_line_blue
    type: object
      properties:
          color: 1
          row_index: 4
  - name: border_pixels
    type: object
    properties:
        color: 6
        location: [ (4,0) , (4,4)]
  - name: corner_pixels_1
    type: object
    properties:
        color: 1
        location_input: None
        location_output: [ (2,0) , (2,4)]

actions:
  - name: preserve_bottom_two_rows
    description: The bottom two rows of the input grid are copied to the output grid without changes.
  - name: modify_top_rows
    description: All cells above row index 2 become white (0), except two which are on the third row, and the far left and far right.
  - name: insert_new_color
    description: insert the new color (1) to the locations.

relationships:
  - type: spatial
    description: The magenta and blue lines are adjacent horizontally.
  - type: positional
    description: The modified/new blue pixels are placed in the corners of the third row from the bottom.
```


**Natural Language Program:**

1.  **Preserve Bottom Rows:** Copy the bottom two rows of the input grid directly to the output grid.
2.  **Clear Top Rows:** Set all cells in the top rows of output (rows 0 to height-3) to white (0).
3.  **Insert Corner Blue:** Insert the new blue color (1) to the corners of the third row from the bottom, (row = height -3, column = 0, and column = width -1 ).

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
