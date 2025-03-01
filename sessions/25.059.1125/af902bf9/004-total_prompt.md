# af902bf9 • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7F4C1A589B50>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 4 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 4 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7F4C1A58B950>
Okay, let's analyze this first example pair.

**Perception of Elements:**

*   The input and output are grids of the same dimensions (10x10).
*   Most of the grid cells are filled with '0' (white).
*   The input grid has two '4's (yellow) that appear to define a rectangular shape (although not filled). It seems the yellow pixels form the corners of the rectangle.
*   The output grid is identical to the input grid, except for a single '2' (red) pixel located at the center point between the two yellow '4's.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      dimensions: 10x10
      elements: integers (0-9)
  - type: pixel
    properties:
      color:
        0: white
        2: red
        4: yellow
      position: (row, column)
  - type: shape
    properties:
      name: rectangle
      corners:
          - pixel1: yellow
            position: (3,3)
          - pixel2: yellow
            position: (3,5)
          - pixel3: yellow
            position: (5,3)
          - pixel4: yellow
            position: (5,5)
actions:
    - Find the set of pixels with the value of 4
    - Define a rectangle using these pixels as opposite corners/vertices.
    - find_center:
        input: rectangle corner coordinates
        output: center coordinate
    - change_color:
        input: pixel at center coordinate, new color (2)
        output: modified grid

relationships:
  -  The red pixel in output is the geometric center of the implied rectangle whose corners are formed by the yellow pixels.

```


**Natural Language Program:**

1.  **Identify Corner Pixels:** Locate all pixels with the value '4' (yellow) in the input grid.
2.  **Form Rectangle:** Consider these yellow pixels as defining the opposite corners of an implied rectangle.
3.  **Calculate Center:** Determine the center point of this rectangle. The center's row is the average of the yellow pixels rows, and its columns are the average of the yellow pixels' columns.
4. **Add center object:** Add a red pixel (value '2') to the output at a position determined by the calculated center point.
5.  **Output:** The output grid is a copy of the input grid, with the addition of the red center pixel.


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
