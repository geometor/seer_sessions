# d406998b • 014 • example_3 • investigate_coder

---

## Example 3

**input:**
```
0 0 5 0 0 5 0 5 0 0 0 5 0
5 0 0 0 5 0 5 0 0 5 0 0 5
0 5 0 5 0 0 0 0 5 0 5 0 0
```

<PIL.Image.Image image mode=RGB size=832x192 at 0x76911E973930>

**output:**
```
0 0 3 0 0 5 0 5 0 0 0 5 0
3 0 0 0 3 0 3 0 0 5 0 0 3
0 5 0 5 0 0 0 0 3 0 3 0 0
```

<PIL.Image.Image image mode=RGB size=832x192 at 0x76911EB263F0>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Elements:**

The task involves two grids: an input grid and an output grid. Both grids have the same dimensions (3x13 in this example). The grids contain single-digit integer values, which represent colors. The primary colors involved are white (0), gray (5), and green (3). The transformation seems to involve a selective replacement of some gray (5) and some white(0) pixels.

**YAML Block (Facts):**


```yaml
facts:
  - object: input_grid
    type: grid
    dimensions: 3x13
    elements: [0, 5]
  - object: output_grid
    type: grid
    dimensions: 3x13
    elements: [0, 3, 5]
  - relationship: element-wise_correspondence
    between: input_grid, output_grid
  - observation: some_white_to_green:
      where: input is 0, output may be 3
  - observation: some_grey_unchanged:
      where: input is 5, output may be 5
  - observation: some_white_unchanged:
      where: input is 0, output may be 0

```


**Natural Language Program:**

1.  **Initialization:** Start with the input grid.
2.  **Conditional Replacement, phase 1, value 0 to 3:** Iterate through each cell of the input grid. going top to bottom, left to right. If a cell is on the top row and has a value of 0 and is directly to the left of one or more values of 5, change the value to a 3. If a cell is a value of 0, is not on the top row, and is directly above or below a 3, change the value to 3.
3. **Conditional Replacement, phase 2:** After iterating over all the cells, we should have our output grid


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
