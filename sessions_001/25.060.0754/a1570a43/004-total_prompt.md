# a1570a43 • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
3 0 2 0 0 0 3
0 2 2 0 0 0 0
2 2 2 2 2 0 0
0 2 0 0 0 0 0
0 2 2 0 0 0 0
0 0 0 0 0 0 0
3 0 0 0 0 0 3
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x7A17541634D0>

**output:**
```
3 0 0 0 0 0 3
0 0 0 2 0 0 0
0 0 2 2 0 0 0
0 2 2 2 2 2 0
0 0 2 0 0 0 0
0 0 2 2 0 0 0
3 0 0 0 0 0 3
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x7A174C75DD50>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a grid of colored pixels. The primary colors observed are green (3), white (0), and red (2). The input grid contains a cross-shaped object composed of red pixels, surrounded by white pixels and bordered by green pixels in the corners. The output grid shows the red cross rotated 90 degrees clockwise. The corner green pixels remain unchanged.

**YAML Block (Facts):**


```yaml
objects:
  - name: red_cross
    type: shape
    color: red (2)
    initial_orientation: vertical
    final_orientation: horizontal
    description: A cross-shaped object formed by connected red pixels.
  - name: corner_pixels
    type: static
    color: green (3)
    positions:
      - top_left
      - top_right
      - bottom_left
      - bottom_right
    description: Green pixels located at the four corners of the grid, these do not change.
  - name: background
    type: static
    color: white (0)
    description: fills all empty areas not corner or object

actions:
  - name: rotate
    object: red_cross
    type: transformation
    description: Rotates the red_cross object 90 degrees clockwise.

relationships:
  - type: spatial
    description: The red_cross is surrounded by white pixels. The green pixels are at fixed corner locations.
```


**Natural Language Program:**

1.  **Identify Objects:** Locate the cross-shaped object formed by contiguous red (2) pixels. Also, identify the green (3) pixels at the four corners of the grid.
2.  **Background:** Note the white color of the background
3.  **Rotation:** Rotate the red cross 90 degrees clockwise.
4. **Corner Invariance:** the corner green color does not change
5.  **Output:** Construct the output grid with the rotated red cross, maintaining the original positions of the corner green pixels and the background.

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
