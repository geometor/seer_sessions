# d4a91cb9 • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=704x768 at 0x716635B76B50>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 2 0 0
0 0 4 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=704x768 at 0x71663D5355D0>
Okay, let's analyze this input-output pair to understand the transformation.

**Perception of Elements:**

*   The input and output are grids of numbers, representing colors.
*   The input grid primarily consists of 0 (white), with a single 2 (red) pixel and a single 8 (azure) pixel.
*    The output grid also has the 8 (azure) and 2 (red) in the same locations.
*   A vertical line of 4s (yellow) extends upwards from the 8 (azure) pixel until the row below the 2 (red)
* A horizontal line of 4's (yellow) extends to the right of where that vertical line stopped, ending just below the 2 (red) pixel.

**YAML Block (Facts):**


```yaml
objects:
  - id: red_pixel
    color: red (2)
    type: pixel
    initial_position: [1, 8]
    final_position: [1, 8]
  - id: azure_pixel
    color: azure (8)
    type: pixel
    initial_position: [10, 2]
    final_position: [10, 2]
  - id: yellow_line
    color: yellow (4)
    type: line
    start: azure_pixel
    end_x: column of red_pixel
    end_y: row above red_pixel
    orientation: vertical then horizontal

actions:
  - type: draw_line
    object: yellow_line
    parameters:
       color: 4
```


**Natural Language Program:**

1.  **Identify Key Pixels:** Locate the azure (8) pixel and the red (2) pixel within the input grid.
2. **Preserve Key Pixels:** The positions of the azure and red pixels are unchanged in the output grid.
3.  **Draw Vertical Segment:** Starting from the azure pixel, draw a vertical line upwards using yellow (4) pixels.
4. **Determine Line Length/Stop condition**: Stop the yellow line one row above the row the red is on.
5. **Draw horizontal segment**: Draw a horizontal line, extending right, from the end of the vertical segment. Stop at the same column where the red pixel is.

In essence, a "L" shaped yellow line connects the azure pixel to a point adjacent to the red pixel, without overlapping it. The order is a vertical line, followed by a horizontal line.

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
