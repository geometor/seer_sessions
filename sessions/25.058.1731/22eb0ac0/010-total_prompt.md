# 22eb0ac0 • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 3
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C360455DCD0>

**output:**
```
0 0 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 3
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C360455FCD0>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a 10x10 grid with single-digit integer values (0-9) representing different colors. The transformation seems to selectively fill certain rows based on the presence of non-zero values in the input grid. Specifically, only horizontal lines containing non-zero numbers at the borders get filled with the value of the border number. The interior numbers remain in place as before, unchanged.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    dimensions: 10x10
    elements: integers (0-9)
  - type: row
    property: horizontal
    contains:
      - integers (0-9)

actions:
  - name: fill_row
    condition: row contains non-zero values only on the edges
    operation: replace all 0 values in the row with non zero value

relationships:
    -  non-zero values on the edges of a row, act as a trigger for the fill operation
```


**Natural Language Program:**

1.  **Identify Target Rows:** Examine each row in the input grid.
2.  **Check Border Condition:** Determine if a row contains non-zero values *only* at its leftmost and rightmost positions.
3.  **Fill Row:** If the border condition is met, replace all '0' (white) pixels in that row with the value found in the border pixels. All the numbers in the borders are the same in each horizontal line.
4. **Preserve other numbers**: the pixels that are not on a horizontal line at the edges are not modified.
5. **Other Rows:** Rows that don't meet the border criteria remain unchanged and all other pixels maintain the values as it is.

Essentially, the transformation identifies and "fills" specific rows based on a simple edge condition. The non zero values in the grid that are not on the edges are kept where they are.

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
