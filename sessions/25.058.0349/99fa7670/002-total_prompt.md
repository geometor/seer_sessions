# 99fa7670 • 002 • example_1 • investigate_coder

---

## Example 1

**input:**
```
0 0 0 0 0 0
0 0 2 0 0 0
0 0 0 0 0 0
0 3 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=384x384 at 0x76911E9AEA30>

**output:**
```
0 0 0 0 0 0
0 0 2 2 2 2
0 0 0 0 0 2
0 3 3 3 3 3
0 0 0 0 0 3
0 0 0 0 0 3
```

<PIL.Image.Image image mode=RGB size=384x384 at 0x76911E9AE170>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Elements:**

The task involves two grids: an input grid and an output grid. Both grids are 6x6 and contain numerical values representing colors. The input grid has two distinct non-zero values (2 and 3, corresponding to red and green) placed in seemingly arbitrary positions, while the rest of the grid is filled with zeros (white). The output grid expands these non-zero values into rectangular blocks.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      dimensions: 6x6
      elements: integers (0-9)
    instances:
      - name: input_grid
      - name: output_grid

  - type: pixel
    properties:
      color:
        mapping: {0: white, 2: red, 3: green}
      position: (row, column)

actions:
  - name: expand_color
    description: Replaces a pixel's value with a rectangular block of the same color.
    parameters:
      color: integer
      start_position: (row, column)
      end_position: (row, column)

relationships:
  - type: transformation
    description: The input grid is transformed into the output grid by expanding the non-zero pixels.
    input: input_grid
    output: output_grid
```


**Natural Language Program:**

1.  **Identify non-zero pixels:** Locate all pixels in the input grid that have a value other than zero.

2.  **Expand each non-zero pixel:** For each non-zero pixel:

    *   Create a rectangle filled with the pixel's color. The original pixel serves as the rectangle start.
    *   The rectangle expands to the right edge of the grid.
    *   The rectangle extend downwards until either, another rectangle exists or the edge of the grid.

3.  **Output:** The resulting grid, after all non-zero pixels have been expanded, is the output grid.

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
