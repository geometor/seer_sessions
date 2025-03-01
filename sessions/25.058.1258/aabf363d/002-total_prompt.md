# aabf363d • 002 • example_2 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0
0 2 2 2 0 0 0
0 0 2 0 0 0 0
0 2 2 2 2 0 0
0 0 2 2 2 0 0
0 0 0 2 0 0 0
4 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x7E120E39E530>

**output:**
```
0 0 0 0 0 0 0
0 4 4 4 0 0 0
0 0 4 0 0 0 0
0 4 4 4 4 0 0
0 0 4 4 4 0 0
0 0 0 4 0 0 0
0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x7E120E3C5A90>

## train_2

**input:**
```
0 0 0 0 0 0 0
0 0 0 3 0 0 0
0 0 3 3 3 0 0
0 3 3 3 3 0 0
0 3 3 0 0 0 0
0 0 3 3 0 0 0
6 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x7E120E3C5C70>

**output:**
```
0 0 0 0 0 0 0
0 0 0 6 0 0 0
0 0 6 6 6 0 0
0 6 6 6 6 0 0
0 6 6 0 0 0 0
0 0 6 6 0 0 0
0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x7E120E3C5BD0>
<PIL.Image.Image image mode=RGB size=956x946 at 0x7E120E3C6170>Okay, let's analyze this ARC task example.

**Perception of Elements:**

The task involves 2D grids (matrices) where each cell contains a single digit representing a color. The primary element is a contiguous shape of a single, non-zero color within each input grid. There's also a single, isolated, different-colored pixel in the bottom-left corner of the input that appears to relate to the color of the shape in the output. The background is always white (0). The output grid has the same dimensions as the input grid, and the main shape's color changes, but the shape stays constant.

**YAML Block (Facts):**


```yaml
objects:
  - name: main_shape
    type: contiguous_region
    properties:
      color: variable # The color changes
      shape: constant  # The shape remains the same between input and output
      position: variable # remains constant relative to itself
  - name: color_indicator
    type: single_pixel
    properties:
      color: variable
      position: bottom_left # Always in the bottom-left corner
  - name: background
    type: fill
    properties:
      color: 0 # Always white (0)
      
relationships:
  - type: color_change
    from: main_shape.color (input)
    to: main_shape.color (output)
    rule: input.color_indicator.color == output.main_shape.color

actions:
   - type: recolor
     target: main_shape
     parameters: [input.color_indicator]
```


**Natural Language Program:**

1.  **Identify** the contiguous shape of non-zero pixels in the input grid. This is the `main_shape`.
2.  **Identify** the single pixel in the bottom-left corner of the input grid. This is the `color_indicator`.
3.  **Note** the `color` of `color_indicator`.
4.  **Create** an output grid with same dimensions as the input.
5. **Copy** `main_shape` from input to output.
6.  **Change** the `color` of all pixels in the `main_shape` in output to the `color` of `color_indicator` in input.
7. **Fill** background of output with `0`.

In simpler terms: The color of the shape in the output grid is determined by the color of the pixel in the bottom-left corner of the input grid. The shape itself is preserved, only the color changes.

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
