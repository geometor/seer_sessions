# 5117e062 • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 3 0 0 0 0 0 0 0 4 0 0
0 3 3 3 0 0 0 0 0 4 8 4 0
0 3 3 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 6 0 6 0 0
0 0 0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=832x832 at 0x744070718050>

**output:**
```
0 4 0
4 4 4
0 4 0
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x744068E01BD0>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves transforming a larger grid (input) into a smaller grid (output). The input grid contains several colored shapes (contiguous blocks of pixels with the same color). The output grid seems to focus on a single color from the input grid. Specifically it shows a yellow shape.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      dimensions: [large, small] # Relative sizes
      elements: [pixels]
  - type: pixel
    properties:
      color: [white, blue, green, red, yellow, gray, magenta, azure, maroon]
  - type: shape
    properties:
      color: [single color]
      form: [contiguous block]

actions:
  - type: select
    target: shape
    criteria:
      color: yellow

  - type: extract
      shape: target
      
  - type: resize

relationships:
  - input_grid contains multiple shapes
  - output_grid contains one shape
  - output_shape is derived from input_shape

```


**Natural Language Program:**

1.  **Identify** all contiguous shapes within the input grid. A shape is defined as a block of one or more pixels of the same color.
2.  **Select** the shape with all pixels of color yellow (value 4).
3. **Extract** the selected yellow shape.
4.  **Resize**; The selected object is presented on it's own with no surrounding whitespace.

Essentially, the transformation isolates and extracts the largest yellow shape from the input grid.

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
