# e40b9e2f • 002 • example_3 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0
0 0 0 4 7 4 0 0 0 0
0 0 0 7 4 7 0 0 0 0
0 0 0 4 7 4 0 0 0 0
0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x716635C7ACD0>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 7 0 4 0 0 0
0 0 0 4 7 4 0 0 0 0
0 0 7 7 4 7 7 0 0 0
0 0 0 4 7 4 0 0 0 0
0 0 4 0 7 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x716635C7ADD0>

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x716635C7AFD0>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 3 6 0 3 0 0 0 0 0
0 0 6 6 6 0 0 0 0 0
0 6 6 6 0 0 0 0 0 0
0 3 0 6 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x716635C4F8D0>

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 0 0 0
0 0 0 8 8 8 0 0 0 0
0 0 0 8 8 8 0 0 0 0
0 0 0 8 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x716635C7A4D0>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 9 0 0 0
0 0 0 8 8 8 0 0 0 0
0 0 0 8 8 8 0 0 0 0
0 0 0 8 8 8 0 0 0 0
0 0 9 0 0 0 9 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x71663D5355D0>
<PIL.Image.Image image mode=RGB size=2048x1360 at 0x716635B76450>Okay, let's analyze the provided input-output examples to understand the transformation.

**Perception of Elements:**

The task involves 2D grids with single-digit integer values (0-9) representing different colors. The primary elements appear to be colored "objects" formed by contiguous blocks of non-zero pixels. The transformation seems to involve modifying these objects, potentially based on their shape, color, and surrounding pixels. There's a concept of mirroring or extending object boundaries. The background is always white (0).

**YAML Fact Block:**


```yaml
objects:
  - name: object1
    type: contiguous_block
    properties:
      colors: [7, 4] #orange, yellow
      shape: irregular, enclosed

  - name: object2
    type: contiguous_block
    properties:
       colors: [6,3] #magenta, green
       shape: irregular, enclosed

  - name: object3
      type: contiguous_block
      properties:
          colors: [8,9] #azure, maroon
          shape: irregular, enclosed

actions:
  - type: extend_boundary
    description:  Expands the original object's boundary based upon neighboring pixels that are 0 valued
    parameters:
      direction:  symmetric

relationships:
  - type: adjacency
    description: The existing objects have non-zero neighboring pixels on opposite sides.

```


**Natural Language Program:**

1.  **Identify Objects:** Locate contiguous blocks of non-zero pixels within the input grid. These form the initial objects.
2.  **Symmetric Expansion:** For the existing colored object in the input array, perform an operation of extending the shape outwards, one unit in cardinal directions.
3. For each pixel of the existing object, examine the neighbors on direct opposite sides, above/below or left/right.
4.  If the object's pixel borders two 0-value pixels, copy that object's pixel to those 0-valued pixels.
5. If the object's pixel *does not* border two 0-valued pixels in opposite directions, there is no change.
6. No other transformation.

In summary the existing object in the input array is "mirrored" across its boundary wherever there are "empty" (0 valued) pixels directly across from each other.

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
