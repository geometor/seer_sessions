# 22168020 • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 3 0
0 0 3 0 0 0 0 3 0 0
0 0 0 3 0 0 3 0 0 0
0 0 0 0 3 3 0 0 0 0
0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C36039E69D0>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 3 3 3 0
0 0 3 3 3 3 3 3 0 0
0 0 0 3 3 3 3 0 0 0
0 0 0 0 3 3 0 0 0 0
0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C36039E4250>
Okay, let's analyze this input-output example pair.

**Perception of Elements:**

The task involves a 2D grid (10x10) of pixels, where each pixel can be one of two colors: white (0) or green (3). The transformation seems to involve expanding or "filling in" the green regions. Specifically, the isolated green pixels in the input become connected horizontally to form a contiguous green region in the output.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    dimensions: [10, 10]
    elements:
      - type: pixel
        color_values: [0, 3]  # 0: white, 3: green
        properties:
          - color
          - position

observations:
  - The input grid contains disconnected green pixels.
  - The output grid contains a connected region of green pixels that are the two center rows.
  - Green pixels can appear with one or two white pixels in between to expand.

actions:
  - fill_horizontally: Connect green pixels horizontally to form a single contiguous block.
  - preserve_color_values: Maintain original color value.

relationships:
  - spatial: Pixels are arranged in a 2D grid.
  - connectivity: Disconnected green pixels in the input become connected in the output.
```


**Natural Language Program:**

1.  **Identify Green Pixels:** Locate all pixels with a value of 3 (green) in the input grid.
2.  **Connect the first two rows**: Connect the first two rows of green to be a solid green.
3.  **Connect the next row**: Connect the green pixels in the third row, maintaining two green pixels in the center.
4. **Connect the bottom rows**: Connect the two green pixels in the fourth and fifth rows.


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
