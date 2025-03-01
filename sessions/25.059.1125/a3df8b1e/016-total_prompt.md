# a3df8b1e • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
1 0 0 0
```

<PIL.Image.Image image mode=RGB size=256x640 at 0x7F4C1B77A4D0>

**output:**
```
0 0 0 1
0 0 1 0
0 1 0 0
1 0 0 0
0 1 0 0
0 0 1 0
0 0 0 1
0 0 1 0
0 1 0 0
1 0 0 0
```

<PIL.Image.Image image mode=RGB size=256x640 at 0x7F4C1A588E50>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a transformation of a 2D grid of pixels. The input grid is mostly filled with white pixels (0) with a single blue pixel (1) at the bottom-left corner. The output grid has the same dimensions, but the blue pixel has been replaced by white, and a diagonal line of blue pixels extends from the bottom-left to the top-right. The blue pixels seem to be arranged in positions that are symmetric about a diagonal axis.

**YAML Block - Facts:**


```yaml
objects:
  - type: grid
    properties:
      dimensions: 10x4 (rows x columns)
      elements: pixels
      color_map: {0: white, 1: blue}

  - type: pixel
    properties:
      color: integer (0 or 1)
      position: (row, column)

actions:
  - name: replace_color
    description: Change the color of a pixel at a specific position.
  - name: create_diagonal
    description: Create a diagonal line of pixels of a specified color.

relationships:
  - type: spatial
    description: The single blue pixel is transformed into a diagonal set of blue pixels from a corner of the grid, and is replaced with another color
```


**Natural Language Program:**

1.  **Identify the initial blue pixel:** Find the location (row, column) of the single blue pixel (value 1) in the input grid.
2.  **Replace initial blue:** Change this pixel in the input to white (0).
3.  **Create the diagonal:** Create a diagonal line of blue pixels (1) starting at the top right corner of the output grid, such that, for every position in the original grid, swap the row and column to create a pixel in the new grid.


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
