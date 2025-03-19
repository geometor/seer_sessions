# fcb5c309 • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 1 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 1 0 0 3 0 0 1 0
0 3 0 0 0 3 0 0 1 0 0 0 0 0 1 0
0 0 0 0 0 0 3 0 1 3 0 3 0 0 1 0
0 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0
0 1 1 1 1 1 1 0 1 1 1 1 1 1 1 0
0 1 0 0 0 0 1 0 0 0 0 0 0 0 0 0
0 1 0 0 0 3 1 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 1 0 0 0 0 0 0 0 0 0
3 1 1 1 1 1 1 0 0 0 0 3 0 0 0 0
3 0 0 0 0 0 0 3 0 0 3 3 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=1024x832 at 0x71663D5B23D0>

**output:**
```
3 3 3 3 3 3 3
3 0 0 3 0 0 3
3 0 0 0 0 0 3
3 3 0 3 0 0 3
3 0 0 0 0 0 3
3 3 3 3 3 3 3
```

<PIL.Image.Image image mode=RGB size=448x384 at 0x71663D5B1F50>
Okay, let's analyze this ARC-AGI task example.

**Perception of Elements:**

The input is a grid of colored pixels (represented by digits 0-9). The output is a significantly smaller grid, also of colored pixels. The dominant colors in the input are white (0), blue (1), and green (3). The output grid consists primarily of green (3) with some white (0). It appears that the output grid is derived from a compressed or summarized version of the input grid, focusing on the green (3) pixels. The shape of the output grid seems to be determined by an outline, possibly the convex hull, of the green pixels in the input.

**YAML Block (Facts):**


```yaml
task: train_2
objects:
  - id: input_grid
    type: grid
    properties:
      colors: [0, 1, 3]  # white, blue, green
      dimensions: [13, 16]
  - id: output_grid
    type: grid
    properties:
      colors: [0, 3]  # white, green
      dimensions: [6, 7]
  - id: green_pixels
    type: object_group
    properties:
      color: 3  # green
      location: scattered in input_grid
      outline: forms a boundary
  - id: white_pixels
       type: object_group
       properties:
        color: 0
        location: fill empty space
relationships:
  - type: derives_from
    subject: output_grid
    object: input_grid
  - type: contains
    subject: input_grid
    object: green_pixels
actions:
 - type: compression
   input: input_grid
   description: creates a smaller grid from the larger grid
 - type: boundary extraction
   input: green pixels
   description: finds boundary of green pixels

```


**Natural Language Program:**

1.  **Identify Green Pixels:** Locate all pixels in the input grid with the value '3' (green).
2.  **Determine Boundary:** Find the bounding box, or outline, around *all* the green pixels in the input grid. The green pixels don't need to be contiguous, but they define the external shape.
3. **Create Output:** Create output grid from identified boundary.
4. **Fill Outline:** Set all pixels within and on the outline to the color green (3).
5. **Fill Inside** Set all pixels within the outline, to the color white (0)

In simple terms, the transformation identifies all green pixels in the input, creates an outline that contains them, and then creates a new grid filled with green, with the inside area of the outline as white.

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
