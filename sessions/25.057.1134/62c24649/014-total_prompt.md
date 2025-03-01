# 62c24649 • 014 • example_3 • investigate_coder

---

## Example 3

**input:**
```
2 1 0
0 2 3
0 3 0
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x74AF1C9C7ED0>

**output:**
```
2 1 0 0 1 2
0 2 3 3 2 0
0 3 0 0 3 0
0 3 0 0 3 0
0 2 3 3 2 0
2 1 0 0 1 2
```

<PIL.Image.Image image mode=RGB size=384x384 at 0x74AF1C9EDC50>
Okay, here's my analysis of the provided example, structured as requested:

**Perception of Task Elements:**

The task involves transforming a smaller grid (input) into a larger grid (output). The input grid seems to be embedded within the center of the output grid, and then mirrored outwards both horizontally and vertically. The colors (represented by numbers) in the original input grid are preserved in the output. The output grid essentially creates a symmetrical pattern based on the input grid. The outside border appears to be a reflection of the inside.

**YAML Block (Facts):**


```yaml
facts:
  - type: grid
    description: Input grid, 3x3
    properties:
      - cells: contain color values (0-9)
  - type: grid
    description: Output grid, 6x6
    properties:
      - cells: contain color values (0-9)
      - structure: symmetrical, based on input grid
  - type: transformation
    description: Input grid is embedded and mirrored
    actions:
      - embed: input grid placed at center of output grid
      - mirror_horizontal: input grid mirrored horizontally
      - mirror_vertical: input grid mirrored vertically
  - type: objects
    description: individual cells within grids
    properties: color value, position (row, column)
```


**Natural Language Program:**

1.  **Embed:** Place the input grid in the center of the output grid. In this example, the 3x3 input is placed within a 6x6 output grid, meaning the top-left corner of input is moved to output\[0,0].
2.  **Mirror Horizontally:** Duplicate the input grid to the right in output\[0:3, 3:6], and make them mirrored by column, swap col 0 with col 2.
3.  **Mirror Vertically:** Duplicate the existing rows, input\[0:3, 0:6], mirror them by row, to create output rows at output\[3:6, 0:6].
4. The result is the mirrored image of the input.


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
