# 72ca375d • 002 • example_1 • investigate_coder

---

## Example 1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0
0 0 2 2 2 0 0 7 7 0
0 0 0 0 0 0 7 0 7 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 6 0 0 0
0 0 0 0 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7778514432F0>

**output:**
```
6 6 6 6
0 6 6 0
```

<PIL.Image.Image image mode=RGB size=256x128 at 0x777851442A30>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Task Elements:**

The task involves transforming a larger grid (input) into a smaller grid (output). The input grid contains multiple colored regions (represented by non-zero digits). The output grid seems to be a cropped and possibly filtered portion of the input grid. Specifically, it appears to focus on a single color (magenta, represented by the digit 6) from the input. The white (0) seems to act like a background.

**YAML Fact Documentation:**


```yaml
objects:
  - id: input_grid
    type: grid
    description: 2D array of digits representing colored pixels.
    properties:
      - width: 10
      - height: 10
      - colors: [0, 2, 6, 7]
  - id: output_grid
    type: grid
    description: 2D array of digits, a transformed subset of the input grid.
    properties:
      - width: 4
      - height: 2
      - colors: [0, 6]
  - id: magenta_region
    type: shape
    description: Contiguous block of pixels with value 6 in the input grid.
    properties:
        - color: 6 (magenta)
  - id: background
    type: color
    description: The empty space between colored shapes, denoted by 0.
    properties:
      - color: 0 (white)

actions:
  - name: crop
    description: Extract a rectangular sub-region from the input grid.
  - name: filter
    description: Select only pixels of a specific color.

relationships:
  - type: subset_of
    from: output_grid
    to: input_grid
    description: The output grid is a cropped and filtered region of the input grid.
  - type: contains
    from: input_grid
    to: magenta_region
    description: The input grid contains the magenta colored region.
```


**Natural Language Program:**

1.  **Identify** the largest contiguous region of magenta (color 6) pixels within the input grid.
2.  **Determine** the bounding box of this magenta region.
3.  **Crop** the input grid to the bounding box.
4. **Replace** surrounding white space (0) with magenta.

Essentially, the program isolates and extracts the most prominent magenta region from the input, and presents it as the output, removing any non 6 pixels inside the region.

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
