# d406998b • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 5 0 5 0 0 5 0 5 0 0 0
5 0 0 0 5 0 0 5 0 0 5 0
0 0 5 0 0 5 0 0 0 5 0 5
```

<PIL.Image.Image image mode=RGB size=768x192 at 0x7FC253D0F4D0>

**output:**
```
0 3 0 3 0 0 5 0 5 0 0 0
5 0 0 0 5 0 0 3 0 0 5 0
0 0 5 0 0 3 0 0 0 3 0 3
```

<PIL.Image.Image image mode=RGB size=768x192 at 0x7FC253D5CC50>
Okay, here's my analysis of the provided input-output pair.

**Perception of Elements:**

The task involves a transformation of a 2D grid of single-digit integers (representing colors). The input and output grids have the same dimensions (3x12). The primary colors involved seem to be white (0), gray (5), and green (3). The transformation appears to selectively change some gray (5) pixels to green (3), while other pixels remain unchanged. It's likely that a spatial pattern or rule dictates which gray pixels are changed.

**YAML Block (Facts):**


```yaml
facts:
  - type: grid
    description: 2D array of integers
    dimensions: 3x12
    input_colors: [0, 5]  # white, gray
    output_colors: [0, 5, 3] # white, gray, green
  - type: transformation
    description: Selective color change
    details: Some gray (5) pixels become green (3), others and white pixels are unchanged.
  - type: objects
    description: individual pixels with color values
    properties:
       color: integer value from 0-9
       position: (row, column) coordinates

```


**Natural Language Program:**

1.  **Iterate** through each pixel of the input grid.
2.  **Identify** gray (5) pixels.
3.  **Check** location of gray pixel against this pattern
    *   If the gray pixel is in the **first** row and it's the **second or fourth** gray pixel of the row, change it to green (3).
    *   If the gray pixel is in the **second** row, and it's the **third** gray pixel of the row, change it to green (3).
    *   If the gray pixel is in the **third** row, and it's the **second or fourth** gray pixel of the row, change it to green (3).
4.  **Leave** all other pixels (white or already green) unchanged.

In other words, counting only the gray(5) pixels in each row, change the second and fourth of first and third row to green (3). Also change third gray pixel of second row to green (3).

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
