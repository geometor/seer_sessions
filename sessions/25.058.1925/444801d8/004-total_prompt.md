# 444801d8 • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 1 1 0 1 1 0 0 0 0
0 1 0 0 0 1 0 0 0 0
0 1 0 2 0 1 0 0 0 0
0 1 0 0 0 1 0 0 0 0
0 1 1 1 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x78E5F214A3D0>

**output:**
```
0 2 2 2 2 2 0 0 0 0
0 1 1 2 1 1 0 0 0 0
0 1 2 2 2 1 0 0 0 0
0 1 2 2 2 1 0 0 0 0
0 1 2 2 2 1 0 0 0 0
0 1 1 1 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x78E5F21D01D0>
Okay, let's analyze the provided input-output example.

**Perception of Elements:**

The input and output are 10x10 grids. The grids contain numerical values representing colors. The primary colors involved seem to be white (0), blue (1), and red (2). The input grid contains a blue shape surrounding a single red pixel. The output grid retains the blue shape but changes some blue pixels to red, effectively "expanding" or "filling" a region that includes the original red pixel. The overall grid structure seems to remain the same.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    dimensions: 10x10
    elements: pixels
    
  - type: pixel
    properties:
      color:
        values: [0, 1, 2]
        names: [white, blue, red]

  - type: shape
    properties:
      color: blue
      description: encloses a single red pixel

  - type: region
    properties:
        color: red
        description: expands from the original red pixel, contained by the blue shape

actions:
  - name: fill
    agent: region
    target: area enclosed by the shape

relationships:
  - type: contains
    subject: shape
    object: region
```


**Natural Language Program:**

1.  **Identify the blue shape:** Locate the contiguous blue (1) pixels in the input grid.
2.  **Locate the seed:** find the red (2) pixel.
3.  **Expand the red:** change to red (2) all the white (0) pixels inside the blue shape.

Essentially, the transformation identifies a blue shape and replaces all the color inside it with red.

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
