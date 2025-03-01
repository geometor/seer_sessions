# 2c608aff • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
1 1 1 1 2 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 4 4 4 4 1 1 1 1 1
1 1 1 4 4 4 4 1 1 1 1 1
1 1 1 4 4 4 4 1 1 1 2 1
1 1 1 4 4 4 4 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 2 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
```

<PIL.Image.Image image mode=RGB size=768x896 at 0x7B4BFE14FF50>

**output:**
```
1 1 1 1 2 1 1 1 1 1 1 1
1 1 1 1 2 1 1 1 1 1 1 1
1 1 1 1 2 1 1 1 1 1 1 1
1 1 1 1 2 1 1 1 1 1 1 1
1 1 1 4 4 4 4 1 1 1 1 1
1 1 1 4 4 4 4 1 1 1 1 1
1 1 1 4 4 4 4 2 2 2 2 1
1 1 1 4 4 4 4 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 2 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
```

<PIL.Image.Image image mode=RGB size=768x896 at 0x7B4BFE14C5D0>
Okay, let's analyze this input-output example.

**Perception of Elements:**

The task involves a 2D grid of single-digit integers, representing colors. The primary colors involved appear to be blue (1), red (2), and yellow (4). There's a large blue background, a central yellow rectangle, and a few isolated red pixels. The transformation seems to involve modifying the red pixels based on their position relative to the yellow rectangle.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      width: 12
      height: 14
      cells: integers (0-9)
  - type: rectangle
    properties:
      color: yellow (4)
      top_left: [3, 4]  # Row, Col
      bottom_right: [6, 7] # Row, Col
  - type: pixel
    properties:
      color: red (2)
      positions:
        input: [[0, 4], [6, 10], [11, 1]] # Row, Column List
        output: [[0, 4], [1, 4], [2, 4], [3, 4], [6, 7], [6, 8], [6, 9], [6, 10]]

actions:
    - name: move_red_pixel
      description:  The Red pixel near the yellow moves to be above the yellow block
    - name: extend_red_pixel
      description: The red pixel at the yellow corner extends to fill the cells next to it.

relationships:
  - type: adjacency
    description: Red pixels are assessed for their proximity to the yellow rectangle.
  - type: inside/outside
    description: We check for pixel location related to rectangle boundary
```


**Natural Language Program:**

1. **Identify the yellow rectangle:** Locate the contiguous block of yellow (4) pixels.
2. **Identify red pixels:** Find all red (2) pixels in the input grid.
3. **Red Pixel Transformation (Above):** Red pixels located above the yellow rectangle are moved down to touch the top border.
4. **Red Pixel Transformation (Corner):** The red pixel to the top right of the yellow box is kept. All other red pixels adjacent to the right border of the yellow rectangle get the value two, converting them to red.
5. **Other pixels stay the same.** All blue and yellow pixels keep the same value.

In essence, the transformation moves red pixels above the block down and extends the right side of the yellow block to be red.

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
