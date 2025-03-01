# 952a094c • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 0 0 0
0 0 0 8 4 3 8 0 0 0
0 0 0 8 0 0 8 0 0 0
0 0 0 8 2 6 8 0 0 0
0 0 0 8 8 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7F4C1B6BFD50>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 2 0 0
0 0 0 8 8 8 8 0 0 0
0 0 0 8 0 0 8 0 0 0
0 0 0 8 0 0 8 0 0 0
0 0 0 8 0 0 8 0 0 0
0 0 0 8 8 8 8 0 0 0
0 0 3 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7F4C1B6BF2D0>
Okay, I'm ready to analyze this input-output pair and try to discern the transformation rule. Here's my report:

**Perception of Elements:**

*   **Input:** A 10x10 grid with a central "cross" or "plus" shape formed by azure (8) pixels. Inside the cross, there are four pixels of different colors (yellow=4, green=3, red=2, magenta=6). The rest of the grid is filled with white (0) pixels.
*   **Output:** A 10x10 grid similar to the input. The azure (8) cross remains the same. The colored pixels inside the cross are gone (replaced by 0),. There are single color pixels present in the rows just above and below the central cross in the output: magenta(6), red(2), green(3), and yellow(4).
* The transformation involves the internal colored pixels to the border and the azure cross remains unchanged.

**YAML Block (Facts):**


```yaml
objects:
  - id: cross
    color: azure (8)
    shape: plus
    position: center
    property: static

  - id: inner_pixels
    colors: [yellow (4), green (3), red (2), magenta (6)]
    shape: individual
    position: inside_cross
    property: dynamic, removable

  - id: border_pixels
    colors: [magenta (6), red (2), green (3), yellow(4)]
    shape: individual
    position: top_and_bottom_border
    property: added

  - id: background
    color: white(0)
    shape: grid
    position: all
    property: static
```


**Natural Language Program:**

1.  **Identify** the azure (8) "cross" shape in the center of the grid. This shape does not change.
2.  **Identify** the four colored pixels (yellow, green, red, magenta) located *inside* the azure cross.
3.  **Remove** those four inner colored pixels, by replacing with white (0).
4.  **Recreate** single pixels of magenta(6) and red(2) in the second row from the top of the grid.
5.  **Recreate** single pixels of green(3) and yellow(4) in the second row from the bottom of the grid.
6. The created pixels will need to align with the columns of the original inner colors.


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
