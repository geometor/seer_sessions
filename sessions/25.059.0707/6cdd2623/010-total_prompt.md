# 6cdd2623 • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0 1 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 1 0 0 1 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 8 0 0 0 0 0 0 0 0 8 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 8 0 0 1 0 0 0 0 0 0 0 2
8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0
```

<PIL.Image.Image image mode=RGB size=1280x832 at 0x7A43F558F550>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=1280x832 at 0x7A43F558E3D0>
Okay, here's my analysis of the provided input-output pair:

**Perception of Elements:**

The task involves a grid of colored pixels. The input grid contains a seemingly random distribution of white (0), blue (1), red (2), and azure (8) pixels. The output grid retains only the red (2) pixels from the input, but expands them to fill the entire row they originally appeared in. All other pixels become white (0).

**YAML Documentation:**


```yaml
facts:
  - object: grid
    description: 2D array of pixels
    properties:
      - rows: 13
      - columns: 20
      - values: integers representing colors (0-9)

  - object: pixel
    properties:
      - color:
          - 0: white
          - 1: blue
          - 2: red
          - 8: azure
      - location: (row, column)

  - action: identify_red_rows
    description: Find rows containing at least one red (2) pixel.

  - action: fill_row_with_red
    description: Set all pixels in identified rows to red (2).

  - action: clear_other_pixels
    description: Set all pixels in rows not containing red to white (0)

  - relationship: row_contains_red
    description: Boolean relationship, true if a row contains at least one red pixel.
```


**Natural Language Program:**

1. **Identify Red Rows:** Iterate through each row of the input grid. For each row, check if it contains at least one red (2) pixel.
2. **Fill Identified Rows:** For each row identified in step 1, change the color of *all* pixels in that row to red (2).
3. **Clear Remaining Pixels:** For all other rows (those that *do not* contain any red pixels in the input), set all pixels in the output grid to white (0).

Essentially, the transformation identifies rows with red pixels in the input and then completely fills those same rows with red pixels in the output, while turning all other cells in the grid to white.

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
