# d4a91cb9 • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=768x640 at 0x71663D5355D0>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 4 4 4 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=768x640 at 0x71663D535C50>
Okay, let's analyze this first example pair.

**Perception of the Elements:**

The input and output are grids of digits, representing colored pixels. The most obvious change is the appearance of yellow (4) pixels in the output where there were only white (0) pixels in the input. The azure (8) and red (2) pixels remain in their original positions. The yellow pixels seem to form a connected path, or line, originating from the azure pixel and extending towards, and connecting with, the red pixel. The yellow path consists of a vertical segment down from the azure pixel, and then a horizontal segment rightwards to the red pixel.

**YAML Block (Facts):**


```yaml
objects:
  - type: pixel
    properties:
      color:
        - white (0)
        - azure (8)
        - red (2)
        - yellow (4)
      position: (row, column)
  - type: grid
    properties:
      dimensions: (rows, columns)

actions:
  - type: draw_path
    parameters:
      start_color: azure (8)
      end_color: red (2)
      path_color: yellow (4)
      path_type: L-shaped # Observation: It's an L, not a general shortest path.

relationships:
  - type: connected
    description: Yellow pixels connect the azure and red pixels.
  - type: spatial
    description:  The yellow path moves vertically down first, then horizontally.
```


**Natural Language Program:**

1.  **Identify** the location of the azure (8) pixel and the red (2) pixel within the input grid.
2.  **Draw** a vertical line of yellow (4) pixels downwards, starting from the row immediately below the azure pixel, and stopping at the row where we must then move horizontally to get to the same row that the red pixel is in.
3. Draw a horizontal line of yellow (4) pixels, connecting the bottom end of the vertical line and moving right, to the column of the red pixel. The end result is that the yellow (4) pixels connect, forming an "L" shaped path from azure to red.
4.  **Preserve** the azure (8) and red (2) pixels in their original locations in the output grid. All other pixels remain as white (0).

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
