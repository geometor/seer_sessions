# a79310a0 • 014 • example_3 • investigate_coder

---

## Example 3

**input:**
```
0 0 0 0 0
0 8 8 8 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x74AF1C9C7750>

**output:**
```
0 0 0 0 0
0 0 0 0 0
0 2 2 2 0
0 0 0 0 0
0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x74AF1C9C7050>
Okay, here's my analysis of the example input-output pair:

**Perception:**

The input is a 5x5 grid, and so is the output. The input grid has a horizontal line of three '8's (azure) in the second row. The output grid has a horizontal line of three '2's (red) in the third row. All other cells in both grids are '0' (white). The azure line seems to be replaced with a red line, and moved down by one row.

**YAML Block (Facts):**


```yaml
facts:
  - type: grid
    description: input and output are 5x5 grids
  - type: object
    description: horizontal line of 3 pixels
    input_color: 8 (azure)
    output_color: 2 (red)
    input_row: 2
    output_row: 3
  - type: action
    description: color change
    from: 8 (azure)
    to: 2 (red)
  - type: action
    description: move object
    direction: down
    amount: 1 row
  - type: background
    description: all other cells remain unchanged
    color: 0 (white)

```


**Natural Language Program:**

1.  **Identify:** Find the horizontal line of three connected pixels with color '8' (azure).
2.  **Change Color:** Change the color of these pixels from '8' (azure) to '2' (red).
3.  **Move:** Move the line of three red pixels down by one row.
4. **Preserve**: Keep all the cells that aren't part of the moving line the same (white).

Essentially, the transformation replaces an azure line with a red line, shifts the red line down one row, and leaves the other cells unchanged.

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
