# 8e1813be • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 0 5 5 5 5 0 2
0 0 0 0 0 0 5 5 5 5 0 0
0 0 0 0 0 0 5 5 5 5 0 0
8 8 8 8 8 0 5 5 5 5 0 8
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=768x768 at 0x7F2DF67FC850>

**output:**
```
2 2 2 2
8 8 8 8
4 4 4 4
1 1 1 1
```

<PIL.Image.Image image mode=RGB size=256x256 at 0x7F2DF79008D0>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves transforming a larger grid of colored pixels into a smaller grid. The larger grid seems to have distinct horizontal bands of colors, with a central grey (5) block surrounded by other colors. The output grid appears to be a condensed representation, retaining only specific colored bands and omitting others, specifically the white (0) and gray (5) areas. It appears that only non-zero, and non-five, colored, horizontal lines are represented.

**YAML Block (Facts):**


```yaml
facts:
  - observation: |
      The input grid is 12x12.
  - observation: |
      The output grid is 4x4.
  - observation: |
      The input grid contains horizontal bands of colors: red (2), grey (5), azure (8), yellow (4), and blue (1), separated and surrounded by white (0)
  - observation: |
      The output grid contains horizontal bands of colors, in the sequence from top to bottom: red (2), azure (8), yellow(4), blue (1).
  - observation: |
      The white (0) and gray (5) colors do not appear.
  - object: input_grid
    type: 2D array
    properties:
      - dimensions: 12x12
      - colors: 0, 1, 2, 4, 5, 8
  - object: output_grid
    type: 2D array
    properties:
      - dimensions: 4x4
      - colors: 1, 2, 4, 8
  - action: selection
    description: |
      Specific rows from the input grid are selected to form the output grid.
  - relationship: input_to_output
    description: |
      The output grid is derived from the input grid by selecting rows where the first element is not 0 or 5, and keeping all of the elements of those rows.
```


**Natural Language Program:**

1.  **Identify Rows:** Examine each row in the input grid.
2.  **Select Rows:** select the rows that does not start with 0, and not 5.
3.  **construct new 2d array:** extract all of the rows, forming the new 2d array that makes up the output.


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
