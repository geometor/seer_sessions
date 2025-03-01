# 11852cab • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 0 3 0 0 0 0 0
0 0 0 4 0 4 0 0 0 0
0 0 3 0 4 0 3 0 0 0
0 0 0 4 0 4 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7A608C34A350>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 0 3 0 2 0 0 0
0 0 0 4 0 4 0 0 0 0
0 0 3 0 4 0 3 0 0 0
0 0 0 4 0 4 0 0 0 0
0 0 2 0 3 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7A608C34AAD0>
Okay, let's analyze this input-output pair to understand the transformation.

**Perception of Elements:**

The input and output are 10x10 grids. The grids contain digits from 0 to 4, where 0 represents white and 2, 3, and 4 represent red, green, and yellow, respectively. The main feature is a cross-shaped arrangement of non-zero pixels in the input. The output seems to modify this cross. Specifically it looks like additional red pixels are added.

**YAML Block (Facts):**


```yaml
observations:
  - type: grid
    size: 10x10
    elements: digits 0-4
    color_mapping:
      0: white
      2: red
      3: green
      4: yellow

  - object: cross
    description: A cross shape formed by contiguous non-zero pixels.
    input_location: Centered in the grid.
    colors: red, green, yellow

  - transformation: addition
    description: Red (2) pixels are added to the grid.
    location:  Adjacent to the existing red pixel, extending it outwards horizontally.
```


**Natural Language Program:**

1.  **Identify the Cross:** Locate the cross shape formed by the colored pixels (2, 3, and 4) in the input grid.
2.  **Locate Red:** Find the red pixel (value 2) within the cross.
3. **Extend red horizontally**: Add new red pixels to the left and right side of the existing red, only extending it by one cell in each direction.
4. **Preserve other colors**: All other colors and their arrangement is preserved.

Essentially it is taking the red element and extending it one pixel horizontally in both directions.

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
