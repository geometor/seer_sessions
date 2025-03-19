# 7ddcd7ec • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0
0 0 0 0 4 4 0 0 0 0
0 0 0 0 4 4 0 0 0 0
0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x70A2EC7D7ED0>

**output:**
```
0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 4 0 0 0
0 0 0 0 4 4 0 0 0 0
0 0 0 0 4 4 0 0 0 0
0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x70A2F47C6350>
Okay, let's analyze this input-output pair.

**Perception of Elements:**

*   The input and output are both 10x10 grids.
*   The grids contain mostly 0s (white pixels), with some 4s (yellow pixels).
*   The yellow pixels in the input appear to form a connected "blob" or object, although it's not a simple, regular shape.
*   The yellow pixels in the output seem to have shifted diagonally downwards and to the right.
*   There appears to be wrapping or reflection involved because output extends the yellow pixels in a regular pattern to the edge of the grid.

**YAML Block (Facts):**


```yaml
objects:
  - id: yellow_object
    type: connected_component
    color: yellow (4)
    initial_position: varies
    shape: irregular

actions:
  - type: diagonal_translation
    direction: down_and_right
    object: yellow_object
  - type: replicate_to_edge
    direction: down_and_right
    object: yellow_object

relationships:
  - type: spatial
    relation: above_and_left_of
    object1: yellow_object (input)
    object2: yellow_object (output)
```


**Natural Language Program:**

1.  **Identify** the connected component of yellow (4) pixels in the input grid. This is the "yellow object."

2.  **Translate** the yellow object diagonally downwards and to the right. The amount of shift is the minimum needed to achieve a repeating pattern.

3.  **Replicate** the resulting translated component to the edge of the grid in a pattern of down and to the right. The translation continues, adding a yellow pixel diagonally down and to the right for the rows that follow the last row that contains a yellow pixel.

Essentially, the transformation takes a connected "blob" of yellow pixels and shifts it to be repeated to the grid edge.

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
