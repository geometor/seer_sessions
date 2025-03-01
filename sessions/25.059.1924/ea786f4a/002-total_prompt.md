# ea786f4a • 002 • example_3 • investigate_coder

---

## train_1

**input:**
```
1 1 1
1 0 1
1 1 1
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x716635C7ACD0>

**output:**
```
0 1 0
1 0 1
0 1 0
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x716635C7A4D0>

## train_2

**input:**
```
2 2 2 2 2
2 2 2 2 2
2 2 0 2 2
2 2 2 2 2
2 2 2 2 2
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x716635C7A3D0>

**output:**
```
0 2 2 2 0
2 0 2 0 2
2 2 0 2 2
2 0 2 0 2
0 2 2 2 0
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x716635BBB2D0>

## train_3

**input:**
```
3 3 3 3 3 3 3
3 3 3 3 3 3 3
3 3 3 3 3 3 3
3 3 3 0 3 3 3
3 3 3 3 3 3 3
3 3 3 3 3 3 3
3 3 3 3 3 3 3
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x716635BBB450>

**output:**
```
0 3 3 3 3 3 0
3 0 3 3 3 0 3
3 3 0 3 0 3 3
3 3 3 0 3 3 3
3 3 0 3 0 3 3
3 0 3 3 3 0 3
0 3 3 3 3 3 0
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x716635BBB4D0>
<PIL.Image.Image image mode=RGB size=1088x976 at 0x716635BE8650>Okay, here's a breakdown of my observations and a proposed natural language program for the transformation:

**Perception of Elements:**

*   **Input Grids:** Square grids of varying sizes, with each cell containing a single digit (0-9). These digits correspond to colors.
*   **Output Grids:** Square grids of the same size as their corresponding input grids. The output grids retain the original digit in the center, while some of the other digits are replaced by 0.
*    **Center Pixel:** The central pixel (where the '0' is initially located in the input) is always preserved.
*   **Transformation Rule:** A consistent pattern of replacing the input color with '0' (white), while the center pixel keeps it's input value.

**YAML Block (Facts):**


```yaml
objects:
  - name: InputGrid
    type: 2D Array
    properties:
      - width: int
      - height: int
      - cells: list[int] # 0-9 representing colors
  - name: OutputGrid
    type: 2D Array
    properties:
      - width: int
      - height: int
      - cells: list[int]

actions:
  - name: ReplaceColor
    description: Replaces specific cell values in the InputGrid with 0, based on their position relative to the center.
    parameters:
      - target_value: int # The value to be replaced (original color)
      - replacement_value: int # The value to replace with (0)

relationships:
    - InputGrid and OutputGrid have the same dimensions.
    - The center cell of InputGrid retains its value in OutputGrid.
    - Cells in InputGrid are replaced with 0 in a cross/plus-shaped pattern centered on the original '0' cell.

```


**Natural Language Program:**

1.  **Identify the Center:** Locate the cell with the value '0' in the input grid. This is the center point of the transformation.
2.  **Preserve Center**: Copy the value of the *center* pixel of the input grid to the corresponding *center* position on the output grid.
3.  **Invert Colors (Cross Pattern):**
    *   All the values on the input grid are inverted.
    *   A value on the input grid is replaced with 0 on the output grid if and only if:
        *   It is at the top or bottom row, and an odd column number.
        *   It is on the left or right most column, and an odd row number.

In other words, imagine an "X" shape of 0's, and the input number in the center.

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
