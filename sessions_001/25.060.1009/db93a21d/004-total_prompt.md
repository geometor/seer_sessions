# db93a21d • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 9 9 0 0
0 0 0 0 0 0 9 9 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 9 9 0 0 0 0 0 0 0
0 9 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7FC252BC7CD0>

**output:**
```
0 0 0 0 0 3 9 9 3 0
0 0 0 0 0 3 9 9 3 0
0 0 0 0 0 3 3 3 3 0
0 0 0 0 0 0 1 1 0 0
0 0 0 0 0 0 1 1 0 0
0 0 0 0 0 0 1 1 0 0
3 3 3 3 0 0 1 1 0 0
3 9 9 3 0 0 1 1 0 0
3 9 9 3 0 0 1 1 0 0
3 3 3 3 0 0 1 1 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7FC252B98250>
Okay, here's my analysis of the first example pair, including my perception of the elements, a YAML block documenting facts, and a natural language program describing the transformation.

**Perception of Elements:**

The task involves transforming a grid of colored pixels. The primary colors involved are white (0), maroon (9), green (3), and blue (1). There are distinct rectangular shapes formed by the maroon pixels. The transformation seems to involve outlining, expanding, and introducing new colors based on relative positions.

**YAML Block (Facts):**


```yaml
objects:
  - name: maroon_square_1
    type: rectangle
    color: maroon (9)
    initial_position: top-right corner
    dimensions: 2x2
  - name: maroon_square_2
    type: rectangle
    color: maroon (9)
    initial_position: bottom-left corner
    dimensions: 2x2
  - name: background
    type: grid
    color: white (0)
    initial_position: all cells
    dimensions: 10x10

actions:
- object: maroon_square_1
  action: outline
  outline_color: green(3)
- object: maroon_square_2
  action: outline
  outline_color: green(3)
- object: background
  action: create rectangle
  new_color: blue (1)
  relative_location: center_right
  dimensions: 6x2

relationships:
  - object1: maroon_square_1
    object2: maroon_square_2
    relation: diagonal_opposite_corners
  - object1: green_outline_1
    object2:  green_outline_2
    relation: parallel and of same dimension

```


**Natural Language Program:**

1.  **Identify Maroon Squares:** Locate all 2x2 maroon (9) squares in the input grid. In this case we have two of such squares.

2.  **Outline Maroon Squares:** For each identified maroon square, create a green (3) outline. The green outline replaces the white(0) pixels that are directly adjacent (up, down, left and right, not diagonally) to the maroon square, and maintains the original dimensions, hence the outline will be inside the grid and will be one pixel thick.

3.  **Create Blue Rectangle:** Create a 2x6 blue (1) rectangle in the center-right portion of the grid. This blue block should start directly adjacent/to the right of the outline of the lower maroon block, spanning vertically six cells down.

4. **Extend Green outline:** expand the green outlines created in step 2, so it become a filled rectangle of the same dimensions.

5.  **Output:** The final output grid combines all these transformations.

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
