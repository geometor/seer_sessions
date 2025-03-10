# 3-1e0a9b12 • 004 • example_2 - CODE

---

# Example

**input:**
```
0 0 0 0 0 9
0 0 0 8 0 0
0 0 0 0 0 0
4 0 0 0 0 0
4 0 7 8 0 0
4 0 7 0 0 0
```

<PIL.Image.Image image mode=RGB size=384x384 at 0x75C2E5BFE8C0>

**output:**
```
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
4 0 0 0 0 0
4 0 7 8 0 0
4 0 7 8 0 9
```

<PIL.Image.Image image mode=RGB size=384x384 at 0x75C2E5BFDC60>
Okay, here's my analysis of the example input-output pair:

**Perception of Elements:**

*   The input and output are grids of the same dimensions (6x6 in this case).
*   Each cell in the grid contains a single digit integer (0-9), representing a color.
*   Most of the grid cells are '0' (white).
*   There are a few non-zero colored cells, which appear to be the focus of the transformation.
*   The non-zero digits and their relative positions seem to be crucial.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      dimensions: 6x6
      cells: integers (0-9)
  - type: colored_cell
    properties:
      color: determined by integer value
      position: (row, column)

actions:
    - type: move
      description: certain colored cells are moved to different locations in the grid
      details:
        -   maroon(9) moves to the bottom row.
        -   azure(8) does not move
        - yellow(4) does not move
        - orange(7) does not move

relationships:
  - type: spatial
    description: the relative positions of colored cells change.
```


**Natural Language Program:**

1.  Identify all non-zero colored cells in the input grid.
2.  Locate the maroon(9) cell. Move cell to the bottom row of it's original column.
3.  All other cells are unchanged, including all white(0) cells and non-zero cells.

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
