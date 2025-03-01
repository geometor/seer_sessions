# 91714a58 • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 1 1 4 0 2 0 0 0 0 2 0 5
0 0 0 3 5 0 0 0 9 9 8 0 4 0 5 8
1 0 8 2 8 0 0 6 0 8 5 0 0 0 8 0
0 0 0 2 2 2 0 0 0 0 0 6 0 0 0 0
0 0 1 2 2 2 0 0 1 9 5 0 0 2 0 4
0 4 0 2 2 2 0 2 0 0 7 0 0 0 0 0
3 0 6 2 2 2 0 0 0 3 5 0 7 0 0 0
7 0 4 6 0 0 4 7 7 3 0 2 0 0 7 1
0 7 0 0 0 0 0 9 7 7 0 0 0 8 5 2
1 5 6 4 9 3 0 3 0 0 0 0 0 9 4 6
0 2 4 0 0 0 0 0 0 0 2 0 1 6 0 0
0 0 0 5 0 0 0 0 0 0 0 0 0 0 2 4
0 0 6 0 0 0 0 0 6 0 0 2 0 0 0 0
0 3 0 0 7 0 2 0 7 9 0 0 0 0 0 0
0 0 5 0 7 0 0 0 0 0 0 0 6 5 3 0
1 0 0 9 0 0 0 2 0 0 0 1 0 0 9 0
```

<PIL.Image.Image image mode=RGB size=1024x1024 at 0x7F2DF795E0D0>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=1024x1024 at 0x7F2DF78BF750>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a grid of colored pixels. The input grid contains various colors, while the output grid seems to retain only a specific shape formed by red (color code '2') pixels, with all other pixels becoming white (color code '0'). The retained red shape appears to be a solid rectangle.

**YAML Block (Facts):**


```yaml
objects:
  - name: input_grid
    type: grid
    properties:
      - colors: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] # All possible colors
      - dimensions: 16x16
  - name: output_grid
    type: grid
    properties:
      - colors: [0, 2] # Only white and red
      - dimensions: 16x16
  - name: red_rectangle
    type: shape
    properties:
      - color: 2 # Red
      - shape: rectangle
      - location:
          start: [3, 3]  #row, col
          end:   [6, 5]  #row, col

actions:
  - name: filter_pixels
    description: "Removes pixels of colors other than red, setting to white and keeps a connected 2 region."
  - name: isolate_rectangle
    description: "Identifies the largest rectangular region of red pixels"

relationships:
  - type: "input_to_output"
    description: "The output grid is derived from the input grid by filtering and isolating a red rectangle."
```


**Natural Language Program:**

1.  **Identify Red Pixels:** Examine the input grid and locate all pixels with the color code '2' (red).
2.  **Isolate Largest Red Rectangle:** Find the largest contiguous rectangular block of red pixels. In this specific example a 3x4 rectangle.
3.  **Clear Other Pixels:** Set all pixels in the output grid to '0' (white), *except* for the pixels within the identified red rectangle.
4.  **Preserve Red Rectangle:** Keep the identified red rectangle in its original position and shape within the output grid.

In short: extract largest red rectangle.

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
