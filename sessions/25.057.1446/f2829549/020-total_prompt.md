# f2829549 • 020 • example_4 • investigate_coder

---

## Example 4

**input:**
```
7 0 7 1 5 5 0
7 7 0 1 5 5 5
0 7 0 1 0 0 0
0 0 0 1 5 0 5
```

<PIL.Image.Image image mode=RGB size=448x256 at 0x786C548159D0>

**output:**
```
0 0 0
0 0 0
3 0 3
0 3 0
```

<PIL.Image.Image image mode=RGB size=192x256 at 0x786C54817F50>
Okay, here's my analysis of the example input-output pair, structured as a report:

**Perception of Task Elements:**

The task involves transforming a grid of colored pixels (represented by integers 0-9) into another grid of a different size and with different pixel values. The input grid appears to have distinct regions of color, while the output grid seems to highlight a very specific feature or pattern within the input. The crucial element appears to be the vertical blue stripe in the input. The output grid is smaller than the input grid.

**YAML Block - Facts:**


```yaml
objects:
  - type: grid
    properties:
      - dimensions: input (4x7), output (4x3)
      - elements: pixels (integers 0-9)
    relations:
      - input_grid_to_output_grid
      - output is smaller than input
  - type: pixel_group
    properties:
      - color: varies (orange, white, blue, gray)
    relations:
    - input_has_vertical_stripe:
        color: blue
        width: one_pixel
        height: fills_grid_vertical

  - type: output_pattern
    properties:
      - color: green
      - shape: "mirrored L" or '7'
      - location: "mirrored L"
    relations:
      - green pixels in output located around where the vertical blue line is in the input.
      - All other pixels are white.
```


**Natural Language Program:**

1.  **Identify the vertical blue stripe:** Locate the single-pixel-wide, full-height vertical stripe of blue (value 1) pixels in the input grid.

2.  **Determine Output Grid Dimensions:** the output width is 3, the height is the same as the input

3.  **Construct output**: Create an output grid with height equal to the height of the input, and width 3.

4.  **Populate the output grid:**
    - The middle column is all white (0) pixels.
    - Output pixels to the left or the right are green, at row indeces offset by one.
    - if a green pixel would be placed outside the boundaries, do not place a green pixel
    - all other pixels are white (0).

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
