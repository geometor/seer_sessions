# bda2d7a6 • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
8 8 8 8 8 8 8 8
8 0 0 0 0 0 0 8
8 0 5 5 5 5 0 8
8 0 5 8 8 5 0 8
8 0 5 8 8 5 0 8
8 0 5 5 5 5 0 8
8 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8
```

<PIL.Image.Image image mode=RGB size=512x512 at 0x7F4C1B6BF1D0>

**output:**
```
5 5 5 5 5 5 5 5
5 8 8 8 8 8 8 5
5 8 0 0 0 0 8 5
5 8 0 5 5 0 8 5
5 8 0 5 5 0 8 5
5 8 0 0 0 0 8 5
5 8 8 8 8 8 8 5
5 5 5 5 5 5 5 5
```

<PIL.Image.Image image mode=RGB size=512x512 at 0x7F4C23110350>
Okay, here's my analysis of the provided input-output example, focusing on perception, object identification, and the transformation rule.

**Perception of Elements:**

The task involves a grid of colored pixels. The primary colors involved are azure (8), gray (5), and white (0). The input and output grids are of the same dimensions (8x8). The transformation appears to involve a color swap and maintain the overall structure and shape of the objects. The outside edge swap, and an inner cross shaped object exists in the original that swaps as well.

**YAML Block (Facts):**


```yaml
objects:
  - name: outer_border
    type: border
    color:
      input: azure (8)
      output: gray (5)
    shape: square
    attribute: static

  - name: inner_square
    type: object
    color:
        input: gray (5)
        output: azure(8)
    shape: square
    attribute: static

  - name: background
    type: background
    color:
      input: white (0)
      output: white (0)
    attribute: static
```


**Natural Language Program:**

1.  **Identify Objects:** Find the outer border of the grid, which is the outermost layer of pixels. Also locate inner square-like object of different color than background.
2.  **Swap Colors**: outer border color swaps with inner object color
3.  **Maintain other colors**: any color other than the border and inner object remain.

In simpler terms, the transformation swaps the colors of the outer border and the inner square, leaving the background (white pixels) unchanged. The positions and shapes of the objects remain constant.

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
