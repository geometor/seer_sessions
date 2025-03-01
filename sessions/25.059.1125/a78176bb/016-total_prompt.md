# a78176bb • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 0 2 5 5 0 0 0 0 0
0 0 0 2 5 0 0 0 0 0
0 0 0 5 2 0 0 0 0 0
0 0 0 5 5 2 0 0 0 0
0 0 0 5 5 5 2 0 0 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 2 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7F4C1B7DC450>

**output:**
```
0 0 0 2 0 0 0 0 0 0
2 0 0 0 2 0 0 0 0 0
0 2 0 0 0 2 0 0 0 0
0 0 2 0 0 0 2 0 0 0
0 0 0 2 0 0 0 2 0 0
0 0 0 0 2 0 0 0 2 0
2 0 0 0 0 2 0 0 0 2
0 2 0 0 0 0 2 0 0 0
0 0 2 0 0 0 0 2 0 0
0 0 0 2 0 0 0 0 2 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7F4C1B7007D0>
Okay, let's analyze this input-output pair.

**Perception of Elements:**

The task involves a grid of colored pixels. The primary colors present are red (2), grey (5), and white (0).  The input grid contains a diagonal line of red pixels from the top left, extending downwards.  There's also a cluster of grey and red pixels in the center. The output grid seems to be related to the diagonal replication of the red pixels.

**YAML Block (Facts):**


```yaml
objects:
  - name: red_pixels
    color: red
    value: 2
    properties:
      - forms_diagonal: True
      - replicated: True
  - name: grey_pixels
    color: grey
    value: 5
    properties:
      - removed: True
  - name: background
    color: white
    value: 0
    properties:
      - static: True

actions:
  - name: replicate_red
    object: red_pixels
    type: diagonal_replication

relationships:
    - object1: red_pixels
      object2: grey_pixels
      relation: adjacent (input_only)
      
```


**Natural Language Program:**

1.  **Identify** the diagonal line of red pixels starting from the top-left corner of the input grid.
2.  **Replicate** this diagonal line of red pixels across the entire grid. Each successive diagonal line is shifted one position to the right.
3. **Remove** all grey pixels.
4. The white background is unchanged.

In essence, the transformation rule appears to be replicating the initial, top-left to bottom-right, red diagonal line across the grid, effectively creating a repeating diagonal pattern of red pixels and removing the gray pixels.

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
