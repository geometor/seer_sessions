# ecdecbb3 • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=832x832 at 0x716635BE9050>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0
0 8 8 8 0 0 0 8 8 8 0 0 0
8 8 2 8 8 8 8 8 2 8 8 8 8
0 8 8 8 0 0 0 8 8 8 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=832x832 at 0x716635C5E750>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves manipulating a 2D grid of colored pixels. The primary colors involved seem to be white (0), red (2), and azure (8). The transformation appears to involve some interaction between the red and azure pixels, possibly extending or replicating the red pixels and changing the color of certain azure pixels.

**YAML Block (Facts):**


```yaml
objects:
  - type: pixel
    properties:
      color:
        - white (0)
        - red (2)
        - azure (8)
      position: [row, column]
  - type: grid
    properties:
      dimensions: [height, width]
      cells: list of pixels

actions:
  - name: extend_red
    description: Red pixels are vertically extended downwards and upwards.
  - name: change_azure
    description: Azure pixels adjacent to the extended red shapes become red,
                 other areas of the azure shape either stay azure or
                 become white (0)

relationships:
  - adjacency: Determines which azure pixels are affected by red pixels.
```


**Natural Language Program:**

1. **Identify Red Pixels:** Locate all red (2) pixels in the input grid.

2. **Vertical Extension:** For each red pixel, extend it vertically upwards and downwards, replacing white pixels with copies of the red one. Do this until the top and bottom edges of the grid are reached by the red shape.

3. **Azure Pixel Modification:**
    * Examine all azure (8) pixels.
    * If an azure pixel is directly adjacent to a vertically extended red pixel created in step 2 (above, below, to the left, or the right, but not diagonal), change its color to red (2).
    * Create white pixels (0) between areas of red and azure, if necessary.

In the ouput, the single horizontal azure line is divided into sections separated by red, and sections of it have been removed/replaced by white (0) pixels.

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
