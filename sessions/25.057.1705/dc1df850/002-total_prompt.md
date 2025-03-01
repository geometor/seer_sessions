# dc1df850 • 002 • example_1 • investigate_coder

---

## Example 1

**input:**
```
2 0 0 0 0
0 0 0 2 0
0 0 0 0 0
0 6 0 0 0
0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x777851442A30>

**output:**
```
2 1 1 1 1
1 1 1 2 1
0 0 1 1 1
0 6 0 0 0
0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x7778514432F0>
Okay, I will analyze the provided input-output example and deliver my observations.

**Perception of Elements:**

The task involves a grid of colored pixels. The input grid seems to have some pixels with specific colors (red, magenta, and white), while the output grid introduces a new color (blue) and modifies some of the existing pixels. The positions of the magenta pixel remain unchanged. The red pixels also seem to maintain relative postion.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      - dimensions: 5x5
      - cells: pixels with color values
  - type: pixel
    properties:
      - color:
        - red (2)
        - magenta (6)
        - white (0)
        - blue (1)
      - position: (row, column)

actions:
  - type: color_change
    description: Change the color of specific pixels.
  - type: fill
    description: filling an area

relationships:
  - adjacency: Pixels are adjacent horizontally, vertically, and diagonally.
  - color_context: Blue appears to relate to areas related to red pixels

```


**Natural Language Program:**

1.  **Identify** all red (2) pixels in the input grid.
2.  **Propagate** red: For each red pixel, change all adjacent white cells to blue
3.  **Preserve** other colors: Maintain the color and position of all other non-white pixels (in this example, the magenta pixel).

In summary, the transformation floods a blue color (1) to top part, stopping
where red (2) pixels occur, from left-to-right and top-to-bottom order.

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
