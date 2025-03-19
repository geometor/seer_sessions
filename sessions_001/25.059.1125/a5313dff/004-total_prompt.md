# a5313dff • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0
0 2 0 0 0 2 0 0
0 2 0 2 0 2 0 0
0 2 0 0 0 2 0 0
0 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=512x512 at 0x7F4C1B701850>

**output:**
```
0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0
0 2 1 1 1 2 0 0
0 2 1 2 1 2 0 0
0 2 1 1 1 2 0 0
0 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=512x512 at 0x7F4C1B6BCAD0>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a grid of pixels, each represented by a single digit integer (0-9). The input grid contains a hollow square made of red pixels (value 2) on a background of white pixels (value 0). The output grid is identical to the input, except the hollow interior of the red square is filled with blue pixels (value 1).

**YAML Block (Facts):**


```yaml
objects:
  - name: background
    color: white (0)
    shape: rectangle
    size: 8x8
  - name: outer_square
    color: red (2)
    shape: hollow square
    outer_edge: 1 pixel wide
    size: 6x6
  - name: inner_square
    color: blue (1)
    shape: filled square
    size: 4x4 # inner dimension is always 2 smaller

actions:
  - name: fill
    target: inner_square # The area inside the hollow red square.
    color: blue (1)

relationships:
  - outer_square *contains* inner_square
  - outer_square *adjacent_to* background, inner_square *adjacent_to* outer_square.

```


**Natural Language Program:**

1.  **Identify the hollow red square:** Locate the contiguous block of red pixels (value 2) that form a hollow square.
2.  **Define the interior:** Determine the boundaries of the empty space enclosed by the red square.
3. **Fill with blue** Change all of the pixels inside that boundary to blue(value 1).
4.  **Preserve the rest:** All other pixels remain unchanged.

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
