# 2dd70a9a • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 8
0 3 8 0 0 0 0 0 0 0
0 3 0 0 0 0 0 8 0 0
0 0 0 0 0 0 8 0 0 8
0 8 0 8 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0
0 8 8 0 0 2 0 0 0 0
0 0 8 0 0 2 0 0 0 0
0 0 8 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C36045DD550>

**output:**
```
0 0 0 0 0 0 0 0 0 8
0 3 8 0 0 0 0 0 0 0
0 3 0 0 0 0 0 8 0 0
0 3 3 3 3 3 8 0 0 8
0 8 0 8 0 3 0 0 0 0
0 0 0 8 0 3 0 0 0 0
0 8 8 0 0 2 0 0 0 0
0 0 8 0 0 2 0 0 0 0
0 0 8 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C36044769D0>
Okay, let's analyze this input-output pair.

**Perception of Elements:**

The task involves a 10x10 grid with single-digit integer values representing different colors. The primary colors observed are white (0), blue (8), green (3), and red (2). The transformation seems to involve a selective fill operation, specifically targeting areas with the color blue (8).

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    dimensions: 10x10
    elements: pixels
    properties:
      color:
        values: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        mapping:
          0: white
          1: blue
          2: red
          3: green
          4: yellow
          5: gray
          6: magenta
          7: orange
          8: azure
          9: maroon
  - type: pixel
    properties:
      color: integer (0-9)
      position: (row, column)

actions:
  - name: fill
    target: pixels
    condition:
      color: azure (8)
    transformation: change_color
    new_color: green(3)

relationships:
    - type: adjacency
      description: Pixels can be adjacent horizontally, vertically, or diagonally.
    - type: containment
      description: the grid contains pixels
```


**Natural Language Program:**

1.  **Identify Target Region:** Locate the connected region of azure (8) pixels starting from the fourth row. Specifically, the block of azure (8) pixels on the left half of the grid.
2. **Flood Fill with Green:** Change the color of all the identified azure(8) pixels inside the specified region in step one to green (3).
3.  **Preserve Other Pixels:** All other pixels in the grid, that are not the targeted region of azure(8), should remain unchanged.

In simple words: Find connected set of azure pixels in the region of row 4, left-side, and change it's value (color) to green.

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
