# 3af2c5a8 • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
3 3 3 3
3 0 0 0
3 0 0 0
```

<PIL.Image.Image image mode=RGB size=256x192 at 0x78E5F99B7850>

**output:**
```
3 3 3 3 3 3 3 3
3 0 0 0 0 0 0 3
3 0 0 0 0 0 0 3
3 0 0 0 0 0 0 3
3 0 0 0 0 0 0 3
3 3 3 3 3 3 3 3
```

<PIL.Image.Image image mode=RGB size=512x384 at 0x78E5F99B70D0>
Okay, here's a report on my perception of the task, including a YAML block documenting facts, and a natural language program describing the transformation.

**Perception of Elements:**

The task involves two grids: an input grid and an output grid. The grids contain numerical values representing colors. The primary colors involved seem to be green (3) and white (0). The output grid appears to be an expanded version of the input grid, with a border of green (3) added around the original shape, effectively increasing both the height and width.

**YAML Block (Facts):**


```yaml
objects:
  - name: input_grid
    type: grid
    properties:
      - colors: [0, 3] # white, green
      - dimensions: [height, width]
  - name: output_grid
    type: grid
    properties:
      - colors: [0, 3] # white, green
      - dimensions: [height, width]
relationships:
  - type: expansion
    from: input_grid
    to: output_grid
    details:
      - height_increase: 2
      - width_increase: 4
actions:
  - type: add_border
    object: input_grid
    color: 3 # green
    thickness:
        top: 1
        bottom: 1
        left: 2
        right: 2

```


**Natural Language Program:**

1.  **Identify the input grid:** Observe the dimensions (height and width) and the arrangement of pixels (colors) within the input grid.

2.  **Create a new, larger grid:** Create output grid
    -   Increase original height by 2.
    -   Increase original width by 4.

3.  **Copy and Translate Inner Grid:** Copy the contents (the white and green pixels) of the input grid into the center of the new, expanded grid. The copied content will sit two cells from the left edge, and one cell from the top edge.

4.  **Fill the border:** Fill all remaining empty cells (the border created by the expansion) in the new grid with the color green (3).

Essentially it is creating a green border around the original grid.

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
