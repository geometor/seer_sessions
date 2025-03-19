# cf98881b • 008 • example_2 • investigate_coder

---

## Example 2

**input:**
```
4 4 4 4 2 9 0 9 0 2 0 0 0 1
4 4 0 0 2 9 9 0 0 2 1 0 0 0
4 0 4 4 2 0 0 0 9 2 0 1 0 1
0 0 0 0 2 0 0 9 0 2 1 0 1 0
```

<PIL.Image.Image image mode=RGB size=896x256 at 0x7B1DDE6E0C50>

**output:**
```
4 4 4 4
4 4 0 0
4 1 4 4
1 0 9 0
```

<PIL.Image.Image image mode=RGB size=256x256 at 0x7B1DDE6E04D0>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves transforming a grid of colored pixels (represented by digits 0-9) into another, smaller grid of colored pixels. The colors appear to be selectively extracted and repositioned. The input grid seems to contain more variety of colors than the output grid.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      - name: input_grid
        dimensions: [4, 14]
        elements: [0, 1, 2, 4, 9]  # Unique colors present
      - name: output_grid
        dimensions: [4, 4]
        elements: [0, 1, 4, 9] # Unique colors present
  - type: pixel
    properties:
      - color:
        mapping: {0: white, 1: blue, 2: red, 4: yellow, 9: maroon}
      - position: [row, column]

actions:
  - type: extraction
    description: Selects specific pixels from the input_grid.
  - type: repositioning
    description: Places the selected pixels into the output_grid at new locations.

relationships:
  - input_grid contains multiple pixel objects.
  - output_grid contains a subset of pixel colors from the input_grid.
  - pixel colors determine their visual representation.
```


**Natural Language Program:**

1.  **Identify Target Colors:** The output grid consists of pixels with colors 4 (yellow), 0 (white), 1 (blue) and 9 (maroon).

2.  **Column Selection:** From the original image, select columns that begins, at the top (row 1), with the target colors.

3.  **Construct Output:** Create a new grid, filling each column, from top to bottom, with all the values of the selected columns.

4.  **Result:** The transformed output is created.

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
