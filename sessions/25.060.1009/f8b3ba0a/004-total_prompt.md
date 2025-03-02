# f8b3ba0a • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 0 1 1 0 1 1 0 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 1 1 0 4 4 0 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 4 4 0 1 1 0 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 1 1 0 1 1 0 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 2 2 0 1 1 0 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 1 1 0 1 1 0 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=832x832 at 0x7FC252BC7C50>

**output:**
```
4
2
3
```

<PIL.Image.Image image mode=RGB size=64x192 at 0x7FC252BC6450>
Okay, let's analyze this input-output pair to understand the transformation.

**Perception of Elements:**

The input is a 13x13 grid containing digits from 0 to 4. The output is a 3x1 grid containing the digits 4, 2, and 3. The input grid seems to have several distinct colored regions (represented by non-zero digits) surrounded by background pixels of color 0 (white). The output grid lists some colors in single cells. The output colors match some of the input colors. The order might matter. Let's check the location of these color regions.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    name: input_grid
    dimensions: 13x13
    elements: integers (0-4)
    description: Contains colored regions surrounded by background (0).
  - type: grid
    name: output_grid
    dimensions: 3x1
    elements: integers (4, 2, 3)
    description: Contains a vertical sequence of color values

  - type: object
    name: yellow_region
    color: 4  #yellow
    input_location: row 4

  - type: object
    name: red_region
    color: 2 # red
    input_location: row 8

  - type: object
    name: green_region
    color: 3  # green
    input_location: row 2
```


**Natural Language Program:**

1.  **Identify Distinct Colored Regions:** Examine the input grid and identify all contiguous regions of non-zero pixels. Consider pixels to be part of the same region if they share a side (not just a corner).
2.  **Extract Specific Colors:** From the identified colored regions, find and take note of the color value of the topmost, leftmost pixel of any region with colors yellow (4), red (2) and green (3).
3. Order the Colors by row: Order the collected color values based on which rows they appear, starting at the top.
4.  **Create Output:** Construct a 3x1 output grid. Fill each cell of the output grid, top to bottom, with each color from the list, starting with the row with smallest number.


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
