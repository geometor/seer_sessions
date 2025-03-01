# 29c11459 • 008 • example_2 • investigate_coder

---

## Example 2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=704x320 at 0x76911EBFDEF0>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
3 3 3 3 3 5 7 7 7 7 7
0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=704x320 at 0x76911EBD2CB0>
Okay, here's a breakdown of my observations and a proposed natural language program for the provided example:

**Perception of Task Elements:**

*   **Input:** A 2D grid (matrix) of digits, mostly 0s, with a few non-zero digits on a single row.
*   **Output:** A 2D grid of the same dimensions as the input. The row containing non-zero digits in the input is transformed. The non-zero digits are expanded, and a new digit (5, representing grey) appears to separate the expansions of the original non-zero values. All other rows remain unchanged (filled with 0s).
* **Colors:** The digits represent specific colors, making this a visual, color-based transformation. The key colors involved in the transformation are green (3), orange (7), and gray (5).
* **Expansion:** the original colored pixels each become 5 of the same colored pixel
* **division:** The two areas of expansions are separated by one grey (5) pixel.

**YAML Fact Block:**


```yaml
facts:
  - type: grid
    description: Input and output are 2D grids of the same dimensions.
  - type: row_transformation
    description: Only the row with non-zero digits in the input is modified.
  - type: object
    attribute: value
    description: Non-zero digits in the input row.
    properties:
      color: Represents a specific color (e.g., 3=green, 7=orange).
      expansion: Each non-zero digit is expanded to the left and to the right.
  - type: object
    attribute: divider
    description: introduces a single grey pixel to separate expanded digits
    properties:
       color: grey (5)
       location: center between two original colored pixels.
  - type: invariance
    description: All rows other than the one with non-zero digits remain unchanged.

```


**Natural Language Program:**

1.  **Identify the Active Row:** Find the row in the input grid that contains non-zero digits.
2.  **Locate Non-Zero Digits:** Within the active row, identify the positions and values of all non-zero digits.
3. **Expansion**: For each non-zero digit, expand the pixel to the left and to the right, using the same value/color, such that the original colored pixel is in the center and there is a block of 5 of the same color.
4.  **Insert Separator:** Place a single '5' (grey pixel) in the grid at the mid-point between the end of one colour expansion and the beginning of the adjacent one.
5.  **Preserve Other Rows:** All other rows in the input grid remain unchanged in the output grid.
6. **Output** output the final grid.

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
