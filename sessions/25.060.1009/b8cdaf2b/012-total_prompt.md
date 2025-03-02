# b8cdaf2b • 012 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 8 0 0
8 8 3 8 8
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x7FC253C82750>

**output:**
```
0 0 0 0 0
3 0 0 0 3
0 3 0 3 0
0 0 8 0 0
8 8 3 8 8
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x7FC253D0F850>
Okay, let's analyze this input-output pair.

**Perception of Elements:**

The task involves two 5x5 grids. The input grid contains zeros (white), eights (azure), and a single three (green). The output grid introduces threes (green) in a seemingly symmetrical pattern around the existing three, while keeping the original elements (8 and 3) in the bottom two rows unchanged. The zeros in the top 3 rows are locations that may change.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    dimensions: 5x5
    elements:
      - value: 0
        color: white
      - value: 3
        color: green
      - value: 8
        color: azure

  - type: pixel
    properties:
      - color
      - coordinates

actions:
  - type: add_object
    description: Places new green (3) pixels in the output grid.
    constraints: Based on position relative original green pixel in top three rows

  - type: copy_row
    description: copy the bottom 2 rows from original grid to the transformed one.
    constraints: row index > 2

relationships:
  - type: symmetry
    description: New green pixels are placed symmetrically with respect to the center of the grid, if any.
  - type: contains
    description: The grids contain pixels.
  - type: adjacent
    description: Pixels can be horizontally, vertically, or diagonally adjacent.
```


**Natural Language Program:**

1.  **Copy Bottom Rows:** Copy the bottom two rows (rows 4 and 5) of the input grid directly to the output grid, preserving all pixel values and positions.

2.  **Identify Center and Non Zero pixels in top rows:**
    *   Find the center cell of the entire grid (row 3, column 3).
    *   Find any non-zero pixels that are present in the top 3 rows.

3. **Add Mirrored Pixels based on top rows:** In the top three rows, for any existing non-zero pixel, add a corresponding pixel of same color in the mirrored location. For a pixel is at (r,c) a mirrored position would be also found at (r, 6-c).

4. **Fill the rest with 0:** All other cells that weren't affected are filled with 0 (white)

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
