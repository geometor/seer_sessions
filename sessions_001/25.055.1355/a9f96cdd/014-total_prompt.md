# a9f96cdd • 014 • example_3 • investigate_coder

---

## Example 3

**input:**
```
0 0 2 0 0
0 0 0 0 0
0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=320x192 at 0x7DCBFF212680>

**output:**
```
0 0 0 0 0
0 8 0 7 0
0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=320x192 at 0x7DCBFC2D4790>
Okay, here's my analysis of the provided example, focusing on perception, documented facts, and a natural language program describing the transformation.

**Perception of Elements:**

The input grid contains a single red (2) pixel. The output grid replaces the red pixel with two pixels, azure (8) and orange (7) pixels. The non-zero pixels are in the second row. The azure pixel takes the previous x position, and the orange takes the subsequent position. It also appears all values are on row 2, the row of the original non-zero pixel.

**YAML Block (Facts):**


```yaml
facts:
  - observation: |
      The input grid is a 3x5 matrix of pixels.
  - input_object: |
      A single red (2) pixel at coordinates (0, 2).
  - output_objects:
      - An azure (8) pixel at (1,1)
      - An orange (7) pixel at (1,3)
  - object_relationships: |
      The red pixel in the input is replaced by two pixels in the output in the same row.
  - spatial_relationships: |
    The azure and orange appear to take the place to the left, and the right of the red input pixel respectively.

```


**Natural Language Program:**

1.  **Locate the Red Pixel:** Find the single red (value 2) pixel in the input grid.
2.  **Record Input Position:** Note the row and the column index.
3.  **Create Output Grid:** Initialize an output grid of the same dimensions as the input, filled with zeros (white).
4. **Place Left Pixel**: Place an azure (8) pixel in the same row, in the column to the immediate *left* of the red pixel. If the red is in the first column, wrap it around to the end.
5. **Place Right Pixel**: Place an orange (7) pixel in the same row, in the column of to the right of the red pixel. If the red pixel is the right-most column, then place the orange pixel in the first column (0).
6.  **All other pixels:** Remain unchanged (value 0).

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
