# 6d0160f0 • 026 • example_4 • investigate_coder

---

## train_4

**input:**
```
3 0 0 5 0 1 0 5 0 0 2
0 2 0 5 0 3 0 5 0 6 0
0 0 0 5 0 0 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 1 0 5 0 0 0 5 0 3 0
7 0 6 5 2 0 7 5 0 7 0
0 0 0 5 0 0 0 5 0 6 0
5 5 5 5 5 5 5 5 5 5 5
7 0 0 5 0 4 0 5 0 0 3
0 0 0 5 0 7 0 5 2 0 0
0 3 0 5 0 3 0 5 0 0 6
```

<PIL.Image.Image image mode=RGB size=704x704 at 0x7A174C6BB5D0>

**output:**
```
0 0 0 5 0 4 0 5 0 0 0
0 0 0 5 0 7 0 5 0 0 0
0 0 0 5 0 3 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
```

<PIL.Image.Image image mode=RGB size=704x704 at 0x7A174C702C50>
Okay, let's analyze this input-output example pair to understand the transformation.

**Perception of Elements:**

*   The input and output are grids of the same dimensions (11x11).
*   The grids contain single-digit integers representing colors.
*   The color gray (5) appears to be a significant element, acting as a separator or boundary.
*   The output grid retains the gray (5) elements in the exact same positions as the input.
*    Most non-gray colors are replaced by white (0).
*   There appear to be selected colors which maintain, at least within the gray separators

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      dimensions: 11x11
      elements: integers (0-9)
      color_map: standard ARC color map
  - type: pixel
    properties:
      color: integer (0-9)
      position: (row, column)
  - type: separator
    properties:
       color: 5 (gray)

actions:
  - name: replace_color
    properties:
      original_color: most non-gray
      replacement_color: 0 (white)
  - name: keep_color
    properties:
      colors: [5]

relationships:
  - type: spatial
    description: gray pixels form horizontal and vertical lines, dividing the grid.
```


**Natural Language Program:**

1.  **Identify Separators:** Locate all pixels with the color gray (5).
2.  **Preserve Separators:** Maintain the gray pixels in their original positions in the output grid.
3.  Within the two horizontal gray lines, locate the positions of any colors in the top most segment
4.  If any color exists in that segment between two vertical gray lines, maintain the first occurence of each unique non zero color just below the horizontal divider
5.  **Replace other colors:** Replace all other colored pixels that do not meet the previous condition with white color (0).


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
