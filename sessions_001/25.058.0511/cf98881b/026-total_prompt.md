# cf98881b • 026 • example_5 • investigate_coder

---

## Example 5

**input:**
```
4 0 4 0 2 0 0 0 0 2 0 0 0 1
4 4 4 4 2 0 0 0 9 2 1 1 0 0
0 4 4 4 2 0 9 9 0 2 1 1 0 1
0 4 4 0 2 0 0 9 0 2 0 1 0 1
```

<PIL.Image.Image image mode=RGB size=896x256 at 0x7B1DDE4F86D0>

**output:**
```
4 0 4 1
4 4 4 4
1 4 4 4
0 4 4 1
```

<PIL.Image.Image image mode=RGB size=256x256 at 0x7B1DDE6A0A50>
Okay, here's my analysis of the provided example, focusing on perception, documented facts, and a natural language program describing the transformation.

**Perception of Elements:**

The primary element is a grid of colored pixels. The transformation significantly reduces the size of the grid. Colors other than yellow (4) seem to be removed, with the arrangement of yellow pixels being the primary feature retained. It seems to be a form of simplification or extraction of the core yellow structure. Blue and White on the border is preserved.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      rows: [integer]
      columns: [integer]
      cells: [integer] # Represents color values
    relationships:
      - contains: [pixel]

  - type: pixel
    properties:
      color: [integer] # 0-9, representing colors
      row: [integer]
      column: [integer]
    actions:
      - retained: [boolean] # Whether the pixel is kept in the output
      - moved: [boolean] # Whether the pixel changes position

transformations:
  - type: reduction
    description: "The grid is significantly reduced in size."
    actions:
    - remove_non_yellow: "Pixels that are not yellow are generally removed"
    - keep_border_colors: "The pixels on the border of original grid, are preserved with their color."
    - preserve_yellow_structure: "the arrangement of yellow pixels is somehow maintained"
```


**Natural Language Program:**

1.  **Identify Border:** Locate the outermost rows and columns of the input grid.
2.  **Preserve Border Colors:** Maintain the colors from those positions.
3.  **Identify Yellow:** Locate all yellow (4) pixels within the input grid.
4.  **Reduce Grid:** Create a new, smaller grid.
5.  **Reconstruct Yellow:** Place the yellow pixels in the new grid, maintaining the original relative positions.
6.  **Fill the rest**: Fill any gaps on the border with colors based on input.


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
