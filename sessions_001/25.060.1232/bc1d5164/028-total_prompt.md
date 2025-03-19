# bc1d5164 • 028 • example_5 • investigate_coder

---

## train_5

**input:**
```
0 3 0 0 0 3 0
3 0 0 0 0 0 3
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 3
```

<PIL.Image.Image image mode=RGB size=448x320 at 0x7CE41B97A350>

**output:**
```
0 3 0
3 0 3
0 0 3
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7CE41B97B0D0>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Elements:**

The task involves a grid of numbers, representing colors. The primary colors observed are white (0) and green (3). The transformation seems to involve a reduction in the size of the grid, focusing on specific areas containing the green color. The output grid appears to be a compressed or cropped version of the input grid, retaining only the columns and rows that contain the green (3) value.

**YAML Fact Block:**


```yaml
facts:
  - observation: Input grid is a 2D array of integers.
  - observation: Output grid is a 2D array of integers.
  - observation: Input grid dimensions are 7x5.
  - observation: Output grid dimensions are 3x3.
  - observation: Input grid contains values 0 (white) and 3 (green).
  - observation: Output grid contains values 0 (white) and 3 (green).
  - object: Grid
    properties:
      - dimensions: (rows, columns)
      - values: integers representing colors
    actions:
      - cropping: Reducing dimensions based on content.
  - relationship: Output grid retains only rows and columns from the input grid that contain the value 3.
```


**Natural Language Program:**

1.  **Identify Target Rows and Columns**: Examine the input grid to identify all rows and columns that contain at least one cell with the value '3' (green).
2.  **Extract Sub-grid**: Create a new grid (the output grid).
3. Populate output grid: The output grid consists exclusively out of intersecting cells of the previously identified rows and columns.

In essence the program extracts the minimum bounding box in which all instances of a non-zero, non-background, color are contained.

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
