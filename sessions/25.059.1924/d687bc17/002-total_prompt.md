# d687bc17 • 002 • example_3 • investigate_coder

---

## train_1

**input:**
```
0 4 4 4 4 4 4 4 4 4 4 4 4 4 0
2 0 0 0 0 0 0 0 0 0 0 0 0 0 3
2 0 0 0 0 0 0 0 0 0 3 0 0 0 3
2 0 0 2 0 0 0 0 0 0 0 0 0 0 3
2 0 0 0 0 0 0 7 0 0 0 0 0 0 3
2 0 0 3 0 0 0 0 0 0 0 0 0 0 3
2 0 0 0 0 8 0 0 0 0 0 0 0 0 3
2 0 0 0 0 0 0 0 0 4 0 2 0 0 3
2 0 0 0 0 0 0 0 0 0 0 0 0 0 3
0 8 8 8 8 8 8 8 8 8 8 8 8 8 0
```

<PIL.Image.Image image mode=RGB size=960x640 at 0x716635BBBC50>

**output:**
```
0 4 4 4 4 4 4 4 4 4 4 4 4 4 0
2 0 0 0 0 0 0 0 0 4 0 0 0 0 3
2 0 0 0 0 0 0 0 0 0 0 0 0 3 3
2 2 0 0 0 0 0 0 0 0 0 0 0 0 3
2 0 0 0 0 0 0 0 0 0 0 0 0 0 3
2 0 0 0 0 0 0 0 0 0 0 0 0 3 3
2 0 0 0 0 0 0 0 0 0 0 0 0 0 3
2 2 0 0 0 0 0 0 0 0 0 0 0 0 3
2 0 0 0 0 8 0 0 0 0 0 0 0 0 3
0 8 8 8 8 8 8 8 8 8 8 8 8 8 0
```

<PIL.Image.Image image mode=RGB size=960x640 at 0x716635BBB450>

## train_2

**input:**
```
0 1 1 1 1 1 1 1 1 1 1 0
2 0 0 0 0 0 0 0 0 0 0 4
2 0 0 0 0 0 0 0 0 7 0 4
2 0 0 0 0 0 0 2 0 0 0 4
2 0 0 0 3 0 0 0 0 0 0 4
2 0 0 0 0 0 0 0 0 0 0 4
2 0 0 0 0 0 0 0 4 0 0 4
2 0 0 0 0 0 0 0 0 0 0 4
2 0 0 8 0 0 0 0 0 0 0 4
2 0 0 0 0 1 0 0 7 0 0 4
2 0 0 0 0 0 0 0 0 0 0 4
0 7 7 7 7 7 7 7 7 7 7 0
```

<PIL.Image.Image image mode=RGB size=768x768 at 0x716635BBB550>

**output:**
```
0 1 1 1 1 1 1 1 1 1 1 0
2 0 0 0 0 1 0 0 0 0 0 4
2 0 0 0 0 0 0 0 0 0 0 4
2 2 0 0 0 0 0 0 0 0 0 4
2 0 0 0 0 0 0 0 0 0 0 4
2 0 0 0 0 0 0 0 0 0 0 4
2 0 0 0 0 0 0 0 0 0 4 4
2 0 0 0 0 0 0 0 0 0 0 4
2 0 0 0 0 0 0 0 0 0 0 4
2 0 0 0 0 0 0 0 0 0 0 4
2 0 0 0 0 0 0 0 7 7 0 4
0 7 7 7 7 7 7 7 7 7 7 0
```

<PIL.Image.Image image mode=RGB size=768x768 at 0x716635BB8B50>

## train_3

**input:**
```
0 6 6 6 6 6 6 6 6 6 0
4 0 0 0 0 0 0 0 0 0 8
4 0 2 0 0 0 0 0 0 0 8
4 0 0 0 0 0 0 0 6 0 8
4 0 0 0 8 0 0 0 0 0 8
4 0 0 0 0 0 0 0 0 0 8
4 0 0 0 0 0 0 0 0 0 8
4 0 0 4 0 0 0 0 0 0 8
4 0 0 0 0 0 0 0 0 0 8
4 0 0 0 0 0 8 0 0 0 8
4 0 8 0 0 0 0 0 0 0 8
4 0 0 0 0 0 0 0 0 0 8
4 0 0 0 0 0 0 0 0 0 8
0 3 3 3 3 3 3 3 3 3 0
```

<PIL.Image.Image image mode=RGB size=704x896 at 0x716635BBB5D0>

**output:**
```
0 6 6 6 6 6 6 6 6 6 0
4 0 0 0 0 0 0 0 6 0 8
4 0 0 0 0 0 0 0 0 0 8
4 0 0 0 0 0 0 0 0 0 8
4 0 0 0 0 0 0 0 0 8 8
4 0 0 0 0 0 0 0 0 0 8
4 0 0 0 0 0 0 0 0 0 8
4 4 0 0 0 0 0 0 0 0 8
4 0 0 0 0 0 0 0 0 0 8
4 0 0 0 0 0 0 0 0 8 8
4 0 0 0 0 0 0 0 0 8 8
4 0 0 0 0 0 0 0 0 0 8
4 0 0 0 0 0 0 0 0 0 8
0 3 3 3 3 3 3 3 3 3 0
```

<PIL.Image.Image image mode=RGB size=704x896 at 0x716635C4F950>
<PIL.Image.Image image mode=RGB size=2560x1872 at 0x71663577F750>Okay, here's a breakdown of my observations and a proposed natural language program for the transformation:

**Perception of Elements:**

*   **Grids:** The input and output are both rectangular grids of colored pixels.
*   **Colors:**  Multiple colors are present, represented by single-digit integers. The colors appear to have significance in the transformation.
*   **Borders:** The top and bottom rows of the input grids often contain a single, distinct color, forming a kind of "border." The border colors can vary between examples.
*   **Inner Pixels:** Inside the borders, there are scattered pixels of various colors, including white (0).
* **Sparsity**: the inner pixels are sparse, there aren't many non-white pixels

**YAML Fact Documentation:**


```yaml
objects:
  - type: grid
    properties:
      - name: input_grid
        shape: rectangular
        elements: pixels (integers 0-9 representing colors)
      - name: output_grid
        shape: rectangular
        elements: pixels (integers 0-9 representing colors)
  - type: pixel
    properties:
      - color: integer (0-9)
      - location: (row, column)
  - type: border
    properties:
       - location: top or bottom
       - color: integer (0-9)
actions:
  - type: find_color_changes
    description: Identify pixels in input that do not match the background and is not part of a border.
  - type: move_or_duplicate
      description: move or duplicate the identified non border, and non-background pixels
relationships:
  - input_grid contains borders
  - input_grid contains inner_pixels
  - output_grid contains borders (same as input)
  - output_grid contains modified_inner_pixels
```


**Natural Language Program:**

1.  **Identify Borders:** Locate the top and bottom rows of the input grid. Note their colors, as these "border" rows remain unchanged in the output.
2.  **Isolate Interior:** Consider the region of the grid excluding the top and bottom border rows.
3.  **Background**: Inside the grid (excluding borders), the output grid contains large areas of white (0).
4. **Identify Significant Pixels**: find any non-white pixel in the interior.
5.  **Transformation Rule:**
   For each non-white pixel inside the grid,
    * If the identified color is in the same column as a border color, duplicate it.
    * If the pixel's color in the same row as the border color, move it to the right
    * All other identified pixels should be removed, being converted to the background.

This program attempts to capture the visual logic of "copying" or "shifting" certain colored pixels while preserving the borders. The concept of background pixels is important.

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
