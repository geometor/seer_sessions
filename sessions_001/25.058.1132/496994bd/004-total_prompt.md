# 496994bd • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
2 2 2
2 2 2
3 3 3
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
```

<PIL.Image.Image image mode=RGB size=192x640 at 0x7F0A59D62A30>

**output:**
```
2 2 2
2 2 2
3 3 3
0 0 0
0 0 0
0 0 0
0 0 0
3 3 3
2 2 2
2 2 2
```

<PIL.Image.Image image mode=RGB size=192x640 at 0x7F0A59D631B0>
Okay, here's my analysis of the first example pair, attempting to discern the transformation rule:

**Perception of Elements:**

The task involves two grids: an input grid and an output grid. Both grids contain single-digit integers (0-9), representing different colors. The input grid has a distinct pattern: the top two rows are red (2), the third row is green (3), and the remaining rows are white (0). The output grid seems to be a modified version of the input grid. The key difference is that the bottom three rows of the output are the reverse of top three rows in the input.

**YAML Block (Facts):**


```yaml
objects:
  - grid:
      type: 2D array
      elements: integers (0-9)
      properties:
        - height: 10
        - width: 3
        - color_distribution:
            0: white
            2: red
            3: green
  - input_grid:
      instance_of: grid
  - output_grid:
      instance_of: grid

actions:
  - copy:
    agent: system
    source: top_3_rows(input_grid)
    destination: temp_copy
  - reverse:
    agent: system
    source: temp_copy
    destination: reversed_copy
  - paste:
      agent: system
      source: reversed_copy
      destination: bottom_3_rows(output_grid)
  - copy_unchanged:
      agent: system
      source: rows_4-7(input_grid)
      destination: rows_4-7(output_grid)

relationships:
  - input_to_output: modified copy with row segment reversal
```


**Natural Language Program:**

1.  **Copy** the top three rows of the input grid.
2.  **Reverse** the order of copied rows.
3.  **Paste** the reversed rows into the bottom three rows of the output grid.
4.  **Copy** the middle four rows (rows 4-7) of input grid to output grid, keeping them in same positions.

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
