# 2-0ca9ddb6 • 002 • example_1 - CODE

---

# Example

**input:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=576x576 at 0x75C2E5BFF1C0>

**output:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 4 0 4 0 0 0 0 0
0 0 2 0 0 0 0 0 0
0 4 0 4 0 0 0 0 0
0 0 0 0 0 0 7 0 0
0 0 0 0 0 7 1 7 0
0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=576x576 at 0x75C2E5BFDC60>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Task Elements:**

The task involves transforming a grid of colored pixels (represented by numbers 0-9) into another grid of the same dimensions. The input grid contains a red pixel (2) and a blue pixel (1), while the output grid introduces yellow (4) and orange (7) pixels in specific patterns around the original colored pixels. The background is white (0) and remains unchanged. The key seems to be the spatial relationship between the newly introduced colors and the original colors.

**YAML Fact Block:**


```yaml
facts:
  - object: grid
    description: 2D array of pixels
    properties:
      - dimensions: 9x9
      - values: integers 0-9 (representing colors)

  - object: red_pixel
    color: red (2)
    initial_position: (3, 2) # (row, column), 0-indexed
    actions:
      - creates: yellow_pixels
        relation: adjacent, horizontal and vertical

  - object: blue_pixel
    color: blue (1)
    initial_position: (6, 6)
    actions:
      - creates: orange_pixels
        relation: adjacent, horizontal and vertical

  - object: yellow_pixels
    color: yellow (4)
    pattern: cross shape
    center: red_pixel

  - object: orange_pixels
    color: orange (7)
    pattern: cross shape
    center: blue_pixel

  - object: background
    color: white (0)
    change: none
```


**Natural Language Program:**

1.  **Identify** the location of the red pixel (2) and the blue pixel (1) in the input grid.
2.  **For the red pixel:** Create a cross-shaped pattern of yellow pixels (4) centered on the red pixel's location. This cross extends one pixel horizontally and one pixel vertically from the red pixel.
3.  **For the blue pixel:** Create a cross-shaped pattern of orange pixels (7) centered on the blue pixel's location. This cross extends one pixel horizontally and one pixel vertically from the blue pixel.
4.  **Maintain** all other pixels (background, represented by 0) as they are. The output grid has the same dimensions as the input grid.

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
