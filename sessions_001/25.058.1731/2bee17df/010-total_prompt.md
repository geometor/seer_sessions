# 2bee17df • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
8 8 8 8 8 8 8 8 8 8 8 8
2 0 0 0 0 0 8 8 8 8 8 8
2 2 0 0 0 0 0 8 8 0 0 8
2 0 0 0 0 0 0 8 0 0 0 8
2 0 0 0 0 0 0 0 0 0 0 8
2 2 2 0 0 0 0 0 0 0 0 8
2 2 0 0 0 0 0 0 0 0 0 8
2 2 0 0 0 0 0 0 0 0 0 8
2 0 0 0 0 0 0 0 0 0 0 8
2 0 0 0 0 0 0 0 0 0 2 2
2 2 0 2 0 0 2 0 0 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2
```

<PIL.Image.Image image mode=RGB size=768x768 at 0x7C36044BF2D0>

**output:**
```
8 8 8 8 8 8 8 8 8 8 8 8
2 0 0 0 3 3 8 8 8 8 8 8
2 2 0 0 3 3 0 8 8 0 0 8
2 0 0 0 3 3 0 8 0 0 0 8
2 3 3 3 3 3 3 3 3 3 3 8
2 2 2 0 3 3 0 0 0 0 0 8
2 2 0 0 3 3 0 0 0 0 0 8
2 2 0 0 3 3 0 0 0 0 0 8
2 3 3 3 3 3 3 3 3 3 3 8
2 0 0 0 3 3 0 0 0 0 2 2
2 2 0 2 3 3 2 0 0 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2
```

<PIL.Image.Image image mode=RGB size=768x768 at 0x7C36044BF550>
Okay, let's analyze this input-output pair to understand the transformation.

**Perception of Elements:**

*   The input and output are grids of the same dimensions (12x12).
*   The grids contain single-digit integers, which we interpret as colors.
*   The input grid has regions of azure (8), red (2), and white (0).
*   The output grid has the same regions of azure (8) and red (2), but some white (0) regions are replaced with green (3).
*    It looks like a connected white region is getting replaced, but not all of them.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    dimensions: 12x12
    elements: integers (0-9 representing colors)
  - type: region
    properties:
      color:
        - azure (8)
        - red (2)
        - white (0)
        - green (3)
      shape: contiguous blocks
actions:
  - type: replace
    from: white (0)
    to: green (3)
    condition: specific white regions
relationships:
  - input_grid: same_dimensions_as: output_grid
  - green_region: replaces: white_region
```


**Natural Language Program:**

1.  **Identify** all contiguous regions of white (0) pixels in the input grid.
2.  **Locate** the largest white area surronded by red color.
3.  **Check** that the large white area stretches between the red lines forming a cross.
4.  **Replace** all pixels within these located white region with green (3).
5.  **Keep** all other pixels (azure and red) the same as in the input grid.

Essentially, a specific set of connected white regions, stretching from the center to the red lines that form a cross, surrounded by red are transformed to green, while all other colors and parts of the grid remain unchanged.

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
