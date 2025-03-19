# 85c4e7cd • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
4 4 4 4 4 4 4 4 4 4 4 4
4 2 2 2 2 2 2 2 2 2 2 4
4 2 1 1 1 1 1 1 1 1 2 4
4 2 1 3 3 3 3 3 3 1 2 4
4 2 1 3 5 5 5 5 3 1 2 4
4 2 1 3 5 8 8 5 3 1 2 4
4 2 1 3 5 8 8 5 3 1 2 4
4 2 1 3 5 5 5 5 3 1 2 4
4 2 1 3 3 3 3 3 3 1 2 4
4 2 1 1 1 1 1 1 1 1 2 4
4 2 2 2 2 2 2 2 2 2 2 4
4 4 4 4 4 4 4 4 4 4 4 4
```

<PIL.Image.Image image mode=RGB size=768x768 at 0x7A1754163150>

**output:**
```
8 8 8 8 8 8 8 8 8 8 8 8
8 5 5 5 5 5 5 5 5 5 5 8
8 5 3 3 3 3 3 3 3 3 5 8
8 5 3 1 1 1 1 1 1 3 5 8
8 5 3 1 2 2 2 2 1 3 5 8
8 5 3 1 2 4 4 2 1 3 5 8
8 5 3 1 2 4 4 2 1 3 5 8
8 5 3 1 2 2 2 2 1 3 5 8
8 5 3 1 1 1 1 1 1 3 5 8
8 5 3 3 3 3 3 3 3 3 5 8
8 5 5 5 5 5 5 5 5 5 5 8
8 8 8 8 8 8 8 8 8 8 8 8
```

<PIL.Image.Image image mode=RGB size=768x768 at 0x7A17541633D0>
Okay, let's analyze this input-output example.

**Perception of Elements:**

*   The input and output are 12x12 grids.
*   The input grid has nested squares of different colors. The colors, from outside in, are yellow (4), red (2), blue (1), green (3), grey (5), and azure (8).
*   The output grid seems to mirror the structure, but the colors change. The new colors are azure (8), grey (5), green(3), blue (1), red(2) and yellow(4)
*   The transformation appears to be a one-to-one color mapping, an inversion or reflection of the input.

**YAML Block (Facts):**


```yaml
objects:
  - name: grid
    type: 2D array
    properties:
      - dimensions: 12x12
      - cell_values: integers (0-9 representing colors)

  - name: color_layer
    type: nested_square
    properties:
      - colors: [yellow, red, blue, green, grey, azure] in input; inverted in output

actions:
   - name: color_inversion
     description: a mapping between the color of the cell in the input to the color of the cell in the output
     map:
       input_color: output_color
       yellow: azure
       red: grey
       blue: green
       green: blue
       grey: red
       azure: yellow
```


**Natural Language Program:**

1.  **Initialization:** Obtain a 12x12 input grid.
2.  **Color Mapping:** Create a corresponding 12x12 output grid by performing a specific color mapping on each cell of the input grid, inverting the color order as follows:
    *   Yellow (4) in the input becomes Azure (8) in the output.
    *   Red (2) in the input becomes Grey (5) in the output.
    *   Blue (1) in the input becomes Green (3) in the output.
    *   Green (3) in the input becomes Blue (1) in the output.
    *   Grey (5) in the input becomes Red (2) in the output.
    *  Azure(8) in the input becomes Yellow(4) in the output.
3. Return the new, color mapped grid

Essentially, the transformation inverts the color layers of the nested squares. The outermost color in the input becomes the outermost color in the output, etc, with the relationship being a shift by +4 steps around the circle [1,2,3,4,5,8].

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
