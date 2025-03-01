# a2fd1cf0 • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=1024x640 at 0x7F4C1B6BF450>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0
0 2 8 8 8 8 8 8 8 8 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=1024x640 at 0x7F4C2318BD50>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves two grids: an input grid and an output grid. Both grids are 10x16 and contain single-digit integers representing colors. The input grid appears mostly empty (filled with 0, or white), with a single green pixel (3) and a single red pixel (2) in seemingly arbitrary locations. The output grid retains the green pixel in the same location, expands the red pixel into a horizontal line of azure pixels (8), and adds azure (8) pixels vertically upwards from the horizontal line, until the height of green pixel.

**YAML Block (Facts):**


```yaml
objects:
  - name: green_pixel
    color: green (3)
    location: [1, 11] # row, column (0-indexed) in both input and output
    properties:
      - static: true  # Location does not change

  - name: red_pixel
    color: red (2)
    location: [7, 1] # row, column in input
    properties:
      - static: false # Becomes a line

  - name: azure_line
    color: azure (8)
    location:  # Varies, derived from red_pixel
      start: [7, 1]
    properties:
       - dynamic : true

actions:
  - name: retain_green
    object: green_pixel
    description: The green pixel's position and color are unchanged.

  - name: expand_red
    object: red_pixel
    description:  The red pixel initiate an azure line.

  - name: extend_azure
    object: azure_line
     description: Extends from init point horizontally.

  - name: connect_azure
    object: azure_line
    description: Extends upwards, stopping one row below the green.

relationships:
  - type: positional
    description: The azure line starts at the red pixel's original location and extends right.
  - type: positional
    description:  The azure line extends upward until the row above the green_pixel row.
```


**Natural Language Program:**

1.  **Locate** the green (3) pixel in the input grid and **copy** it to the same location in the output grid.
2.  **Locate** the red (2) pixel in the input grid.
3.  In the output grid, at the same position of red pixel, create horizontal a line of azure (8) pixels extending to the right. The horizontal line ends in the column before the green pixel.
4. Create a vertical line of azure (8) pixel, starting from the position of the last azure pixel of the horizontal line. This line extends vertically upwards until the row above the green pixel.


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
