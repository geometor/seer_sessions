# a3325580 • 008 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 8
0 0 4 0 0 0 0 0 0 8
0 0 4 0 0 6 6 0 0 8
0 0 4 4 0 0 6 0 0 0
0 0 4 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7CE41B95CC50>

**output:**
```
4 6 8
4 6 8
4 6 8
4 6 8
4 6 8
```

<PIL.Image.Image image mode=RGB size=192x320 at 0x7CE4233084D0>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The input is a 10x10 grid containing various colored pixels (represented by numbers 0-9). The output is a 5x3 grid containing a subset of the colors from the input. The colors present in the output (4, 6, and 8) appear to be those that form connected shapes within the input grid, specifically excluding colors that border only value 0(white). In addtion, it extracts the non-zero colors that do not touch the edge or corner.

**YAML Block (Facts):**


```yaml
facts:
  - input_grid_size: 10x10
  - output_grid_size: 5x3
  - input_colors: [0, 3, 4, 6, 8]
  - output_colors: [4, 6, 8]
  - input_shapes:
    - color: 4 #yellow
      description: "An L shape composed by four pixels."
    - color: 6 #magenta
      description: "A block composed by four pixels."
    - color: 8 #azure
      description: "A line composed by three pixels."
    - color: 3 #green
      description: "An L shape of four pixels."
  - output_format: "The output grid consists of columns, each representing one of the colors (4, 6, and 8) repeated vertically."
  - selection_criteria: "Colors that form shapes and doesn't have neighbours of just 0(white), and are not on the edge"
```


**Natural Language Program:**

1.  **Identify Target Colors:** Examine the input grid and identify the pixels with colors that form a contiguous shape, excluding those which only neighbour color 0 or edge/corner. In this case, the target colors are 4 (yellow), 6 (magenta), and 8 (azure).
2. **Arrange in Order:** The colors may not be in order. Therefore, once the colors are found, put them in numerical order.
3.  **Construct Output Grid:** Create a 5x3 grid.
4.  **Populate Columns:**  Fill the first column with the color 4, repeated five times. Fill the second column with the color 6, repeated five times. Fill the third column with the color 8, repeated five times.


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
