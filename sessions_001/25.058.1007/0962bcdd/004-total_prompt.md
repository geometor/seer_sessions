# 0962bcdd • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0
0 7 2 7 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 7 2 7 0 0
0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=768x768 at 0x7EE1209CA350>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
2 0 7 0 2 0 0 0 0 0 0 0
0 2 7 2 0 0 0 0 0 0 0 0
7 7 2 7 7 0 0 0 0 0 0 0
0 2 7 2 0 0 0 0 0 0 0 0
2 0 7 0 2 0 2 0 7 0 2 0
0 0 0 0 0 0 0 2 7 2 0 0
0 0 0 0 0 0 7 7 2 7 7 0
0 0 0 0 0 0 0 2 7 2 0 0
0 0 0 0 0 0 2 0 7 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=768x768 at 0x7EE1209CA030>
Okay, let's analyze this input-output pair.

**Perception of Elements:**

*   The input and output are both 12x12 grids.
*   The grids contain numerical values representing colors (0-9, though only 0, 2, and 7 are present).
*   The input grid has two distinct "shapes" or "objects" formed by the 7s and 2. The first shape consists of 7s surrounding a single 2, the whole shaped like a plus. It's on the upper left. The other shape is the same pattern but located in the bottom right.
*   The output grid seems to expand these original shapes, with some additional 0 and 2 pixels. The 7s expand into the shape of an open rectangle/square, and the 2's seem to form connections.

**YAML Block (Facts):**


```yaml
facts:
  - task_type: grid_transformation
  - grid_size: 12x12
  - colors:
      - 0: white
      - 2: red
      - 7: orange
  - input_objects:
      - object1:
          shape: plus_sign
          color: orange (7)
          center_color: red (2)
          location: top_left
      - object2:
        shape: plus_sign
          color: orange (7)
          center_color: red (2)
          location: bottom_right
  - output_objects:
      - object1:
          shape:  hollow_rectangle/square
          color: orange(7)
          location: top-left
      - object2:
          shape: hollow_rectangle/square
          color: orange(7)
          location: bottom_right
      - color_2_pattern:
          description: red pixels (2) connecting both top-left object and bottom-right object.
```


**Natural Language Program:**

1.  **Identify "plus-shaped" objects:** Find connected components of 'orange' (7) pixels in the input grid that form a plus shape, with a single 'red' (2) pixel in the center.

2.  **Expand the plus-shapes:** For each identified plus-shaped object, transform the orange (7) pixels into a hollow rectangle or square shape. The shape should expand outwards.

3.  **Connect the expanded shapes** Place 'red' (2) pixels between two shapes. These red pixels form two separate diagonals connecting all 4 corners of the original shapes.

4. Fill in the area between plus-shaped objects with lines of "red" (2). The "red" (2) lines fill the two newly formed diagnols.

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
