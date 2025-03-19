# 6cdd2623 • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 4 4 0 0 0 0 4 0 0 0 0 0 8 0 4 0
0 0 4 0 4 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 0 5
4 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 5 0 0 0 0 0 0 0 5
0 4 0 0 0 5 0 0 0 0 4 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 4
0 0 0 0 0 0 0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 4 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8
4 0 0 0 0 0 0 0 0 0 0 0 0 0 4 0 0
0 5 0 0 0 0 0 0 0 0 0 0 4 0 0 4 0
0 0 0 0 0 0 4 0 4 0 0 0 0 0 0 4 0
4 0 4 0 4 0 0 0 4 5 0 0 0 8 0 0 0
```

<PIL.Image.Image image mode=RGB size=1088x960 at 0x7A43F5EEC950>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0
```

<PIL.Image.Image image mode=RGB size=1088x960 at 0x7A43F558D8D0>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The input grid contains a seemingly random scattering of colored pixels, primarily yellow (4), azure (8), gray (5), and white(0). The output grid appears to retain only the azure (8) pixels, and repositions them in a specific configuration. All other colors are replaced with white (0). The azure pixels form a horizontal line in the center row and vertical line in the center.

**YAML Documentation:**


```yaml
facts:
  - objects:
    - type: pixel
      properties:
        color:
          - white (0)
          - yellow (4)
          - azure (8)
          - gray (5)
          - maroon(9)
        position: [row, column]
  - actions:
    - name: filter_color
      description: Remove pixels of colors other than azure.
    - name: reposition
      description: Move azure pixels to form a cross shape.
  - relationships:
    - type: spatial
      description: The final positions of the azure pixels form intersecting horizontal and vertical lines.
    - type: color_based_selection
      description: Only azure pixels are preserved; others are discarded.
```


**Natural Language Program:**

1.  **Isolate Azure Pixels:** Identify all pixels with the color azure (8) in the input grid.
2.  **Discard Other Colors:** Remove all pixels that are not azure, setting their value to white (0).
3.  **Form Horizontal Line:** Create a horizontal line of azure pixels across the 11th row of the output grid.
4. **Form Vertical Line**: Create a vertical line of azure pixels from top to bottom in the middle of the grid(column 13).
5.  **Combine:** Combine horizontal line and vertical line.

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
