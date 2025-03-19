# 3ac3eb23 • 008 • example_2 • investigate_coder

---

## Example 2

**input:**
```
0 4 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x384 at 0x7778516D1450>

**output:**
```
0 4 0 0 0 0 0
4 0 4 0 0 0 0
0 4 0 0 0 0 0
4 0 4 0 0 0 0
0 4 0 0 0 0 0
4 0 4 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x384 at 0x7778516D1810>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Elements:**

The task involves a grid of pixels, initially mostly white (0) with a single yellow (4) pixel in the top row. The transformation seems to involve creating a vertical, alternating pattern of yellow and white pixels, originating from the initial yellow pixel. The output grid has a repeating pattern of yellow and white, with yellow appearing every other row in the same column as the original yellow pixel.

**YAML Block - Facts:**


```yaml
objects:
  - type: grid
    properties:
      dimensions: [7x7]
      elements: pixels
      default_color: white (0)

  - type: pixel
    properties:
      color:
        - white (0)
        - yellow (4)
      position: [row, column]

actions:
  - name: alternate_color
    description: Changes pixel color in an alternating fashion vertically.
    parameters:
      start_pixel: The initial yellow pixel.
      alternating_colors: [yellow, white]

relationships:
  - type: vertical_alternation
    description:  Yellow pixels appear every other row, directly below the initial yellow pixel.
    involved_objects: [pixels]
```


**Natural Language Program:**

1.  **Identify the initial yellow pixel:** Find the single yellow (4) pixel in the input grid.
2.  **Vertical Alternation:** Starting from the row immediately below the initial yellow pixel, and for every alternate row afterwards, change the color of the pixel in that column to yellow (4). All the way down to the bottom row of the grid.
3. **All other pixels:** All other cells remain the same color (white).

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
