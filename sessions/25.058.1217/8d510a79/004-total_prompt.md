# 8d510a79 • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0
0 2 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 2 0 0 1 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x741F734C5C70>

**output:**
```
0 0 1 0 0 0 1 0 0 0
0 0 0 0 0 0 1 0 0 0
0 2 0 0 0 0 0 0 0 2
0 2 0 0 0 0 0 0 0 2
0 2 0 0 0 0 0 0 0 2
5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 2 0 0 0 0
0 1 0 0 0 2 0 0 1 0
0 1 0 0 0 0 0 0 1 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x741F734C5D10>
Okay, let's analyze the provided input-output example.

**Perception of Elements:**

*   The input and output are 10x10 grids.
*   The grids contain single-digit integers representing colors (0-9).
*   The colors present are white (0), blue (1), red (2), and gray (5).
*   The gray row (5) seems to be a fixed element, acting as a separator.
*    The colored pixels other than gray appear to move or change positions between the input to output.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      rows: 10
      columns: 10
      colors: [0, 1, 2, 5]
  - type: pixel
    properties:
      color:
        - white # 0
        - blue  # 1
        - red   # 2
        - gray  # 5
      position: [row, column]
  - type: horizontal_line
    properties:
      color: gray #5
      position:
          row: 6
          column: all

actions:
  - name: extend_vertically
    object: pixel
    properties:
        color: [blue, red]

relationships:
  - type: spatial
    relation: "blue and red pixels above the gray line extend vertically by repeating their color once downward in the same column"

  - type: spatial
    relation: "blue and red pixels below the gray line extend vertically by repeating their color once *upward* in the same column."
```


**Natural Language Program:**

1.  **Identify the Separator:** Locate the horizontal line of gray (5) pixels.
2.  **Process Above Separator:** For each blue (1) or red (2) pixel *above* the gray line, replicate that pixel's color in the cell immediately *below* it, within the same column. If a cell in between is already occupied skip to the next unoccupied.
3.  **Process Below Separator:** For each blue (1) or red (2) pixel *below* the gray line, replicate that pixel's color in the cell immediately *above* it, within the same column.If a cell in between is already occupied skip to the next unoccupied.
4. White(0) pixels remain unchanged.
5. Gray(5) horizontal line remains unchanged.

In essence, the blue and red pixels are "vertically extended" by one cell, with the gray line acting as a dividing point for the direction of the extension (downwards above the line, upwards below it).

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
