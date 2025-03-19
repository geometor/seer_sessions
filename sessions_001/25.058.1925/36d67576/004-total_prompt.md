# 36d67576 • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 1 2 0 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 0 4 0 0
0 3 0 3 0 3 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 4 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 4 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=832x832 at 0x78E5F21D3950>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 1 2 0 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 3 4 0 0
0 3 0 3 0 3 0 0 0 0 4 1 0
0 0 0 0 0 0 0 0 0 3 4 0 0
0 0 0 0 0 0 0 0 0 0 4 1 0
0 0 0 0 0 0 0 0 0 3 4 2 0
0 0 0 3 0 3 0 3 0 0 0 0 0
0 0 0 4 4 4 4 4 0 0 0 0 0
0 0 0 2 1 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=832x832 at 0x78E5F21D01D0>
Okay, here's my analysis of the provided input-output example pair.

**Perception of Task Elements:**

The task involves manipulating colored pixels within a grid. The input and output grids have the same dimensions (13x13). Several distinct colored objects (contiguous blocks of pixels of the same color) are present. The primary colors observed are blue (1), red (2), green (3), yellow (4), and white (0). Some objects appear to move or change color between the input and output. Specifically, there appears to be some interaction between colors, possibly involving the insertion of another color between two existing pixels. There are also some isolated pixels.

**YAML Block - Facts:**


```yaml
task_elements:
  - type: grid
    dimensions: 13x13
    elements: pixels
    properties:
      color:
        values: [0, 1, 2, 3, 4] # white, blue, red, green, yellow

  - type: object
    definition: contiguous block of pixels of the same color
    properties:
      color:
        values: [0, 1, 2, 3, 4]
      shape: variable
      position: variable

  - type: transformation
    description: color and position changes of objects
    details:
        - object_interaction: color insertion
        - object_position_change: vertical flip for the blue objects
        - isolated_pixel_color_change: some isolated single pixels swap
```


**Natural Language Program:**

1.  **Identify Objects:** Locate all contiguous blocks of pixels of the same color in the input grid.

2.  **Blue Object Mirroring:** Identify the two blue (color 1) objects shaped like an "L", which are at row 2 and at row 10. Mirror the position of the object in row 2, to become row 10. Mirror the blue object in row 10 to become row 2.

3. **Color Insertion near 4,3:** There is a line of yellow(4) pixels and a set of 3 green(3) pixels in a horizontal arrangement. A green pixel appears at the right of this line of yellow pixels, only if there is yellow adjacent to green.

4.  **Color Insertion near 4,2:** There is a line of yellow(4) pixels and one red(2) pixel. A red pixel is placed above the single yellow pixel adjacent to red, only if there is yellow adjacent to red.

5. **Isolated single pixel color swapping**:
    - In the input, there is a green(3) pixel at (4,9) and a yellow(4) pixel at (8,9). Swap their color, the output has the yellow pixel at (4,9), and green pixel at (8,9).
    - In the input, there is a blue(1) pixel at (4,11) and a yellow(4) pixel at (6,10). Swap their color, the output has the yellow pixel at (4,11) and blue pixel at (6,10).

6.  **Preserve Other Colors:** All other pixels retain their original colors and positions.


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
