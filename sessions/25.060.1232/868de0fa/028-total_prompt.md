# 868de0fa • 028 • example_5 • investigate_coder

---

## train_5

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 1 0 0 0 0 0 0 0
0 1 0 0 0 0 0 1 0 0 0 0 0 0 0
0 1 0 0 0 0 0 1 0 0 0 0 0 0 0
0 1 0 0 0 0 0 1 0 0 0 0 0 0 0
0 1 0 0 0 0 0 1 0 0 0 0 0 0 0
0 1 0 0 0 0 0 1 0 0 0 0 0 0 0
0 1 1 1 1 1 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 1 1 1 1 0 0 0
0 0 0 0 0 0 1 0 0 0 0 1 0 0 0
0 0 0 0 0 0 1 0 0 0 0 1 0 0 0
0 0 0 0 0 0 1 0 0 0 0 1 0 0 0
0 0 0 0 0 0 1 0 0 0 0 1 0 0 0
0 0 0 0 0 0 1 1 1 1 1 1 0 0 0
```

<PIL.Image.Image image mode=RGB size=960x960 at 0x7CE41B97AD50>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 1 0 0 0 0 0 0 0
0 1 7 7 7 7 7 1 0 0 0 0 0 0 0
0 1 7 7 7 7 7 1 0 0 0 0 0 0 0
0 1 7 7 7 7 7 1 0 0 0 0 0 0 0
0 1 7 7 7 7 7 1 0 0 0 0 0 0 0
0 1 7 7 7 7 7 1 0 0 0 0 0 0 0
0 1 1 1 1 1 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 1 1 1 1 0 0 0
0 0 0 0 0 0 1 2 2 2 2 1 0 0 0
0 0 0 0 0 0 1 2 2 2 2 1 0 0 0
0 0 0 0 0 0 1 2 2 2 2 1 0 0 0
0 0 0 0 0 0 1 2 2 2 2 1 0 0 0
0 0 0 0 0 0 1 1 1 1 1 1 0 0 0
```

<PIL.Image.Image image mode=RGB size=960x960 at 0x7CE41B9798D0>
Okay, here's a breakdown of my observations and proposed transformation rule for the provided input-output example:

**Perception of Elements:**

The task involves two grids of colored pixels. The input grid contains two distinct shapes formed by blue (1) pixels against a white (0) background. These blue shapes seem to be "filled in" with different colors in the output grid. The upper blue shape is filled with orange (7), and the lower blue shape is filled with red (2). The outlines remain blue.

**YAML Documentation:**


```yaml
facts:
  - objects:
      - type: shape
        color: blue (1)
        description: outline of a closed area
      - type: background
        color: white (0)
      - type: fill
        color:
          - orange (7)
          - red (2)
        description: colors used to fill the blue outlines
  - actions:
      - name: fill_shape
        description:  Fill the interior of a closed shape defined by a blue outline.
  - relationships:
     - description: The upper blue shape is filled with orange.
     - description: The lower blue shape is filled with red.
     - description:  Blue pixel outlines remains unchanged

```


**Natural Language Program:**

1.  **Identify Shapes:** Locate all closed shapes formed by contiguous blue (1) pixels on the input grid.
2.  **Determine Fill Color:**
    *   If the shape is the *upper* shape, the fill color is orange (7).
    *   If the shape is the *lower* shape, the fill color is red (2).
3.  **Fill Shapes:** For each identified shape, replace all interior white (0) pixels with the designated fill color determined in step 2.
4. **Preserve outlines:** Keep the original blue pixels unchanged.

This program accounts for identifying shapes based on color and connectivity, selecting a fill color based on shape's vertical position, and performing the fill operation while keeping the outlines.

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
