# aabf363d • 002 • example_1 • investigate_coder

---

## Example 1

**input:**
```
0 0 0 0 0 0 0
0 2 2 2 0 0 0
0 0 2 0 0 0 0
0 2 2 2 2 0 0
0 0 2 2 2 0 0
0 0 0 2 0 0 0
4 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x786C5497D8D0>

**output:**
```
0 0 0 0 0 0 0
0 4 4 4 0 0 0
0 0 4 0 0 0 0
0 4 4 4 4 0 0
0 0 4 4 4 0 0
0 0 0 4 0 0 0
0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x786C546B7350>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves two 7x7 grids. The input grid contains pixels of colors white (0), red (2), and yellow (4). The output grid contains only white (0) and yellow (4) pixels. The primary change seems to be a color replacement within a specific shape. The yellow pixel in the input at the bottom left, seems to be a 'seed color' which gets used to replace the red objects.

**YAML Block - Facts:**


```yaml
observations:
  - type: grid
    description: Input and output are 7x7 grids.
  - type: object
    description: A contiguous block of red (2) pixels forms a distinct shape in the input.
  - type: color_change
    description: Red (2) pixels in the input are replaced with yellow (4) pixels in the output.
  - type: location
    description: other than the replacement area, the rest of the grids are white.
  - type: single_color
    description: The input contains an isolated yellow (4) pixel at the bottom left (0,6)
  - type: color_seed
    description: color (4) at (0,6) seems to determine the replacement color
```


**Natural Language Program:**

1.  Identify the single yellow pixel (value 4) in the input grid.
2.  Identify all pixels that belong to the shape with at least on pixel having color red (value 2).
3.  Change the color of all of the pixels identified in step two to yellow (value 4).
4.  Leave all the other colors intact
5.  The resulting grid is the output.

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
