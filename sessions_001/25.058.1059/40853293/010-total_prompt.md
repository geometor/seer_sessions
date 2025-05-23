# 40853293 • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x1280 at 0x7DBFF1F37890>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 3 4 3 3 3 3 0 0
0 0 0 4 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 7 4 7 7 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 9 0 0 0 0
0 8 8 8 8 9 8 0 0 0
0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x1280 at 0x7DBFF1F36850>
Okay, let's analyze this input-output example to understand the transformation.

**Perception of Elements:**

The input and output are grids of digits (0-9), representing colors. The input grid contains isolated single-pixel colored objects, scattered across the grid, with most of the grid being filled with 0 (white). The output grid seems to expand some of these colored pixels, particularly around other non-zero pixels. There's a sense of "filling in" or "connecting" the colored pixels, with a preference to grow in specific patterns. Yellow (4) seems to be the main instigator, expanding vertically down. The other colors grow horizontally to fill the area created by expansion of color 4.

**YAML Block (Facts):**


```yaml
objects:
  - type: pixel
    properties:
      color: integer (0-9)
      position: (row, column)
  - type: grid
    properties:
      dimensions: (rows, columns)
      cells: list of pixels

actions:
  - name: expand_vertically
    agent: yellow_pixel (4)
    target: empty_cells_below
    condition: until_another_object_or_edge
  - name: expand_horizontally
    agent: other_color_pixels
    target: empty_cells_adjacent
    condition: defined_by_vertical_expansion

relationships:
  - type: adjacency
    description: pixels can be adjacent horizontally, vertically, or diagonally.
  - type: containment
    description: The grid contains pixels.
```


**Natural Language Program:**

1.  **Identify Catalyst:** Locate all yellow (4) pixels in the input grid.

2.  **Vertical Expansion (Yellow):** For each yellow pixel, extend a vertical line of yellow pixels downwards. Stop extending this line when you encounter another non-zero pixel or the bottom edge of the grid.

3. **Horizontal Expansion(other colors):** Identify other colored pixels on same row with Yellow(4) . Expand them horizontally to fill the columns occupied by the yellow pixels in the corresponding rows.

In summary, the transformation rule involves a directional expansion of pixels. Yellow (4) pixels initiate a downward vertical expansion, defining vertical extent and other colors spread horizontally based on vertical expansion.

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
