# 234bbc79 • 002 • example_4 • investigate_coder

---

## train_1

**input:**
```
0 5 0 0 0 0 0 0 0
2 2 0 5 1 0 5 2 2
0 0 0 0 5 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=576x192 at 0x716635C5DC50>

**output:**
```
0 2 1 1 0 0 0
2 2 0 1 2 2 2
0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x192 at 0x716635C5CD50>

## train_2

**input:**
```
0 0 0 5 1 5 0 0 0 0 0
2 2 0 0 0 0 0 0 3 3 3
0 5 0 0 0 0 0 5 3 0 0
```

<PIL.Image.Image image mode=RGB size=704x192 at 0x716635C5CED0>

**output:**
```
0 0 0 0 0 0 0 0 0
2 2 0 0 0 0 3 3 3
0 2 1 1 1 3 3 0 0
```

<PIL.Image.Image image mode=RGB size=576x192 at 0x716635C5CA50>

## train_3

**input:**
```
0 0 0 0 0 0 5 0 0 0 0
2 2 2 0 5 8 8 0 0 0 0
0 0 5 0 0 0 0 0 5 6 6
```

<PIL.Image.Image image mode=RGB size=704x192 at 0x716635C5DD50>

**output:**
```
0 0 0 0 0 0 0 0 0
2 2 2 0 0 8 6 6 6
0 0 2 8 8 8 0 0 0
```

<PIL.Image.Image image mode=RGB size=576x192 at 0x716635C5FDD0>

## train_4

**input:**
```
0 1 5 0 0 0 0 0 2 2 0
1 1 0 0 5 2 0 5 2 0 0
0 0 0 0 0 5 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=704x192 at 0x716635C5CAD0>

**output:**
```
0 1 1 2 2 0 2 2
1 1 0 0 2 2 2 0
0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=512x192 at 0x716635C5CDD0>
<PIL.Image.Image image mode=RGB size=2848x464 at 0x716635B762D0>Okay, let's analyze the provided input-output pairs to discern the underlying transformation rule.

**Perception of Elements:**

The task involves 2D grids of single-digit integers (0-9), representing different colors. The transformation seems to involve a selective replacement or filtering of certain colors/numbers based on their neighbors, particularly the color gray (5). The output grids generally have fewer distinct colors than the input grids. The overall shape/dimension of the grid stays the same. It looks like the transformation depends on a "center" object with color gray(5), and objects around it.

**YAML Fact Documentation:**


```yaml
facts:
  - type: grid
    description: 2D array of integers (0-9)
  - property: color
    description: Each number represents a color.
  - object: gray_pixel
    value: 5
    description: Pixels with the value 5 (gray).
  - object: non_gray_pixel
    description: Pixels with values other than 5.
  - relation: adjacency
    description:  Pixels can be adjacent horizontally or vertically.
  - action: replace_color
    description: Certain non-gray pixels are changed.
  - condition: center
    description: find the object(5) in the middle row.
  - condition: neighbor_horizontal
    description: Check if the horizontal neighbors of 'center' have the same color.
  - condition: neighbor_diagonal
      description: Check if the diagonal neighbors of 'center' have the same color.
```


**Natural Language Program:**

1.  **Identify Gray Pixels:** Locate all pixels with the value 5 (gray) in the input grid.
2.  **Focus on Central Gray:** If more than one exists, determine the one is at the "center"
    in the following way: find the gray(5) in the input grid on the middle row
3.  **Horizontal Neighbors:** If horizontal neighbors of the 'center' are non-gray,
    and have the *same* value, extend those horizontally until you reach the edges of the grid or another color.
4. **Propagate Change:** Propagate this process to other object(5) on the center row.
5. **Diagonal:** From the *other* objects(5) on the original center row, if the diagonal neighbors have the same value, extend it until you reach the edges of the grid.
6.  **Replace:** Replace all the object(5) with 0.
7.  **Output:** Return the resulting modified grid.


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
