# 834ec97d • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=576x576 at 0x7D67CBE7A850>

**output:**
```
4 0 4 0 4 0 4 0 4
4 0 4 0 4 0 4 0 4
4 0 4 0 4 0 4 0 4
4 0 4 0 4 0 4 0 4
4 0 4 0 4 0 4 0 4
0 0 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=576x576 at 0x7D67CBE7A050>
Okay, let's analyze this input-output pair.

**Perception of Elements:**

*   The input is a 9x9 grid with a single maroon (9) pixel near the center. The rest of the pixels are white (0).
*   The output is a 9x9 grid. It retains the maroon (9) pixel in the same location. Above the maroon pixel are five rows that alternate between yellow (4) and white(0).

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    dimensions: 9x9
    elements: pixels
  - type: pixel
    color: maroon
    value: 9
    location: (2, 4) # (column, row) - zero-indexed
  - type: pixel
    color: white
    value: 0
  - type: pixel
    color: yellow
    value: 4

actions:
  - type: retain
    object: maroon pixel
    description: The maroon pixel remains unchanged in its original location.
  - type: add
    object: rows
    description: Five rows of alternating yellow and white pixels are present above original maroon pixel.
    pattern: 4 0 4 0 4 0 4 0 4
             4 0 4 0 4 0 4 0 4
             4 0 4 0 4 0 4 0 4
             4 0 4 0 4 0 4 0 4
             4 0 4 0 4 0 4 0 4

relationships:
    - type: above
      subject: added rows
      object: maroon pixel
```


**Natural Language Program:**

1.  **Locate** the maroon (9) pixel in the input grid.
2.  **Retain** the maroon (9) pixel in the same location in the output grid.
3.  **Add** rows above the maroon pixel, where each row alternates between yellow (4) and white (0), starting and ending with yellow, and having as many rows to occupy the space above, leaving the rest as white pixels.

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
