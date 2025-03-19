# 54d82841 • 008 • example_2 • investigate_coder

---

## Example 2

**input:**
```
0 3 3 3 0
0 3 0 3 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x777851601BD0>

**output:**
```
0 3 3 3 0
0 3 0 3 0
0 0 0 0 0
0 0 0 0 0
0 0 4 0 0
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x777869E5D450>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Elements:**

The task involves a grid of colored pixels. The primary colors observed are white (0), green (3), and yellow (4). The input grid appears to be transformed into the output grid with minimal changes. The most notable change is the introduction of a single yellow pixel in the bottom row of the output grid, while the green pixels in the input grid remain unchanged.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      rows: 5
      columns: 5
      colors: [white, green, yellow]
  - type: pixel
    properties:
      color:
        - white (0)
        - green (3)
        - yellow (4)
      position:
        row: [0-4]
        column: [0-4]

actions:
  - type: change_color
    properties:
      from: white
      to: yellow
    constraints:
      row: 4
      column: 2

relationships:
    - type: contains
      subject: grid
      object: pixel
```


**Natural Language Program:**

1.  **Copy the Input:** The output grid starts as an exact copy of the input grid.
2.  **Locate Target:** Find the cell at the last row (row index 4) and at a particular column (column index 2).
3. **Change the target:** If there aren't non-white colored cell at last row, find the cell at the last row (row index 4) and the middle column (column index 2), change its color to yellow (4).
4.  **Preserve others:** All other pixels remain with their original color.

In essence, the transformation adds a single yellow pixel to the bottom center if there aren't any non-white colored cell at the bottom, leaving the rest of the grid untouched.

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
