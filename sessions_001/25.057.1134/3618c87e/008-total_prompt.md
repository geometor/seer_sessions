# 3618c87e • 008 • example_2 • investigate_coder

---

## Example 2

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 1 0 1 0
0 5 0 5 0
5 5 5 5 5
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x74AF1CB17250>

**output:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 5 0 5 0
5 1 5 1 5
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x74AF1CB16550>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a grid of single-digit integers, representing colors. The transformation seems to involve a swap of color, based on the location.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      rows: 5
      columns: 5
      cells: integers (0-9) representing colors

  - type: cell
    properties:
       color: integer values from input

actions:
  - type: swap
    description: Changes the color values of 2 specific colors from position to position.

relationships:
  - adjacency: Cells are adjacent horizontally and vertically.
  - row_position: relationship of cell position within a row
  - col_position: relationship of cell position within a column
```


**Natural Language Program:**

1.  **Identify Key Colors:** The input grid has two colors which change values, blue (1) and gray (5). All the cells containing white (0) remain unchanged.

2. **Color swap:** Swap blue (1) and gray (5) in the input grid, the output grid will be changed.

In simple terms the location of 1 and 5 from the input will be where 5 and 1 in the output appear.

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
