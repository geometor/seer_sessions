# d631b094 • 014 • example_3 • investigate_coder

---

## Example 3

**input:**
```
0 7 0
0 0 0
0 0 0
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x71BF73D1FBB0>

**output:**
```
7
```

<PIL.Image.Image image mode=RGB size=64x64 at 0x71BF73D1FA70>
Okay, here's my analysis of the example input-output pair, presented as a report:

**Perception of Task Elements:**

The input is a 3x3 grid. Most cells are white (0), but there's a single orange (7) cell in the top-middle position. The output is a 1x1 grid containing only the orange (7) cell. The task appears to involve extracting a specific, non-white cell from the input grid. The background is white, making the colored pixels more prominent.

**YAML Fact Block:**


```yaml
facts:
  - object: input_grid
    type: grid
    dimensions: 3x3
    elements:
      - color: white
        value: 0
        count: 8
      - color: orange
        value: 7
        count: 1
        position: [0,1] #row, col
  - object: output_grid
    type: grid
    dimensions: 1x1
    elements:
      - color: orange
        value: 7
        count: 1
  - transformation: extraction
  - rule: "extract the non-zero cell"

```


**Natural Language Program:**

1.  Examine the input grid.
2.  Locate the single cell that has color orange, which means a pixel value that is not 0.
3.  Create a 1x1 output grid.
4.  Place the value of the non-white cell into the output grid.

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
