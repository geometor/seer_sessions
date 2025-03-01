# 22eb0ac0 • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
9 0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 9
0 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C360457AFD0>

**output:**
```
0 0 0 0 0 0 0 0 0 0
9 0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 9
0 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C360457A4D0>
Okay, here's my analysis of the provided input-output example, focusing on perception, factual documentation, and a natural language program description of the transformation.

**Perception of Task Elements:**

The task involves a 10x10 grid of colored pixels. The primary observation is a change in a specific row. The input has a row of zeros and on that same row in the output all the values match the single non-zero value found on each half of that row in the input. It appears the transformation is focused on the row where every other value in the input grid are zeros.

**YAML Documentation of Facts:**


```yaml
facts:
  - observation: |
      The input and output grids are 10x10.
  - object: row
    properties:
      - description: A horizontal line of 10 pixels.
      - characteristic: |
          Most rows are identical in the input and output.
      - special_row: |
          Contains all zeros on every other entry in the input grid.
          Contains a color repetition across it in the output.
  - action: identify_row
    description: |
        Locate row where all other entries are zeros in the input grid.
  - action: get_color
    description: |
        find non zero values in the identfied row, use these values to replace zeros in the same row.
  - relationship:
      - type: spatial
        description: |
          The transformation preserves the grid dimensions and most rows.
      - row_content : left and right values are used
```


**Natural Language Program:**

1.  **Identify the Special Row:** Scan the input grid to find the row where all other values are zero.
2.  **Get Non-Zero Values**: From the special row, save the value of all non-zero entries, moving from left to right, one entry at a time..
3.  **Fill Special Row in Output:** In the identified row, from the input, copy the color found on that to all positions on the same row in the output grid.
4. **Other Rows:** all other rows remain unchanged between input and output.

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
