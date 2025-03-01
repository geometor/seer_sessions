# 54d82841 • 008 • example_2 • investigate_coder

---

## Example 2

**input:**
```
0 3 3 3 0
0 3 0 3 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x7B1DDE7AB850>

**output:**
```
0 3 3 3 0
0 3 0 3 0
0 0 0 0 0
0 0 0 0 0
0 0 4 0 0
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x7B1DE5E217D0>
Okay, here's my analysis of the provided example, focusing on perception, facts, and a natural language program describing the transformation.

**Perception of Elements:**

*   **Grid:** The core structure is a 2D grid (matrix) of pixels.
*   **Colors:** Pixels have colors, represented by integer values. In this example, we see 0 (white), 3 (green), and 4 (yellow).
*   **Shapes:** The green pixels (3) form a distinct shape at the top of the grid in both input and output.
* **Change in color/single pixel**: one of the white pixels is changed to color yellow.

**YAML Block (Facts):**


```yaml
facts:
  - object: grid
    type: 2D array
    properties:
      rows: 5
      columns: 5
      cell_values: integers (0-9)
  - object: green_shape
    type: contiguous_region
    properties:
      color: 3 (green)
      location: top_rows
    actions: []
  - object: changed_pixel
    type: single_cell
    properties:
      initial_color: 0 (white)
      final_color: 4 (yellow)
      location: [4,2] # row, col (zero indexed)

  - transformation:
      description: "A single white pixel at the bottom is recolored to yellow"
```


**Natural Language Program:**

1.  **Identify** the input grid and its dimensions (5x5 in this case).
2.  **Locate** a specific white pixel (value 0). The location of this pixel is on the last row, in the center column.
3. **Change** the color of that specific pixel. The color changes to yellow (value 4).
4.  **Preserve** all other pixels, which remain unchanged. The green shape at the top of both the input and output.
5.  **Output** the modified grid.

In essence, the transformation involves changing a single, strategically-placed white pixel to yellow while keeping the rest of the grid identical. The core logic focuses on identifying the precise coordinates of the pixel to be modified.

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
