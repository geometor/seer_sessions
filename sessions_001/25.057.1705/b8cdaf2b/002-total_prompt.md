# b8cdaf2b • 002 • example_1 • investigate_coder

---

## Example 1

**input:**
```
0 0 0
0 2 0
2 4 2
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x777851601D10>

**output:**
```
4 0 4
0 2 0
2 4 2
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x777851601DB0>
Okay, here's my analysis of the example input-output pair, structured as requested:

**Perception of Elements:**

The task involves a 3x3 grid of single-digit integers, representing colors.  The input grid appears to be transformed into a modified output grid. The central element (2) and bottom-middle (4) element seems untouched. The top row changes, while other elements remain. The transformation involves some kind of change the values in the top row based on values in the bottom row.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    dimensions: 3x3
    elements:
      - type: cell
        value: integer (0-9)
        color: mapped from value (see COLOR_MAP)

properties:
  - grid:
    - has_rows: true
    - has_columns: true
  - cell:
    - has_value: true
    - has_color: true
    - has_position: (row, column)

actions:
    - type: modify_cell
      agent: transformation_rule
      details: changes top row values conditionally

relationships:
    - type: spatial
      relation: element position within grid (row, column)
      relation_element: adjacency and same value
    - type: transformation
      relation: input grid to output grid
      rule: changes to top row
```


**Natural Language Program:**

1.  **Identify the top row and bottom row of the input grid.**
2. **For each cell in top row**
   1.  **if the cell is not white(0)**
      1.  **do nothing**.
   2.  **if the cell is white(0)**
       1. **find the cell in the bottom row in same column**.
       2. **if the cell in the bottom row is 2(red)**
          1.   **Change the top row to yellow(4)**
       3. **if the cell in bottom row is 4(yellow)**
          1.  **Change the top row to yellow (4)**
       4. **if cell in the bottom row is 0 (white)**
            1. **change the top row cell to a 0(white)**.
3.  **All other cells remain unchanged.**

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
