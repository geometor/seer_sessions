# 2c608aff • 002 • example_4 • investigate_coder

---

## train_1

**input:**
```
8 8 8 8 8 8 8 8 8 8 8 8
8 8 3 3 3 8 8 8 8 8 8 8
8 8 3 3 3 8 8 8 8 8 8 8
8 8 3 3 3 8 8 8 8 4 8 8
8 8 3 3 3 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 4 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8
```

<PIL.Image.Image image mode=RGB size=768x576 at 0x7B4BFDB42950>

**output:**
```
8 8 8 8 8 8 8 8 8 8 8 8
8 8 3 3 3 8 8 8 8 8 8 8
8 8 3 3 3 8 8 8 8 8 8 8
8 8 3 3 3 4 4 4 4 4 8 8
8 8 3 3 3 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 4 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8
```

<PIL.Image.Image image mode=RGB size=768x576 at 0x7B4C05B57B50>

## train_2

**input:**
```
2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 1 1 1 2 2 2 2 2 2
2 2 2 1 1 1 2 2 2 2 2 2
2 2 2 1 1 1 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 8 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2
```

<PIL.Image.Image image mode=RGB size=768x640 at 0x7B4BFE1DC9D0>

**output:**
```
2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 1 1 1 2 2 2 2 2 2
2 2 2 1 1 1 2 2 2 2 2 2
2 2 2 1 1 1 2 2 2 2 2 2
2 2 2 8 2 2 2 2 2 2 2 2
2 2 2 8 2 2 2 2 2 2 2 2
2 2 2 8 2 2 2 2 2 2 2 2
2 2 2 8 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2
```

<PIL.Image.Image image mode=RGB size=768x640 at 0x7B4C05B57650>

## train_3

**input:**
```
1 1 1 1 2 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 4 4 4 4 1 1 1 1 1
1 1 1 4 4 4 4 1 1 1 1 1
1 1 1 4 4 4 4 1 1 1 2 1
1 1 1 4 4 4 4 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 2 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
```

<PIL.Image.Image image mode=RGB size=768x896 at 0x7B4C05B576D0>

**output:**
```
1 1 1 1 2 1 1 1 1 1 1 1
1 1 1 1 2 1 1 1 1 1 1 1
1 1 1 1 2 1 1 1 1 1 1 1
1 1 1 1 2 1 1 1 1 1 1 1
1 1 1 4 4 4 4 1 1 1 1 1
1 1 1 4 4 4 4 1 1 1 1 1
1 1 1 4 4 4 4 2 2 2 2 1
1 1 1 4 4 4 4 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 2 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
```

<PIL.Image.Image image mode=RGB size=768x896 at 0x7B4C05B574D0>

## train_4

**input:**
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 4 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 4 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 4 1 1
1 1 4 1 1 1 1 5 5 5 5 5 1 1 1 1 1 1
1 1 1 1 1 1 1 5 5 5 5 5 1 1 1 1 1 1
1 1 1 1 1 1 1 5 5 5 5 5 1 1 1 1 1 1
1 1 1 1 1 1 1 5 5 5 5 5 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 4 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```

<PIL.Image.Image image mode=RGB size=1152x896 at 0x7B4C05B56650>

**output:**
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 4 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 4 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 4 1 1 4 1 1 1 1 1 1
1 1 1 1 1 1 1 1 4 1 1 4 1 1 1 4 1 1
1 1 4 4 4 4 4 5 5 5 5 5 1 1 1 1 1 1
1 1 1 1 1 1 1 5 5 5 5 5 1 1 1 1 1 1
1 1 1 1 1 1 1 5 5 5 5 5 1 1 1 1 1 1
1 1 1 1 1 1 1 5 5 5 5 5 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 4 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```

<PIL.Image.Image image mode=RGB size=1152x896 at 0x7B4C05B578D0>
<PIL.Image.Image image mode=RGB size=3616x1872 at 0x7B4BFD16ACD0>Okay, let's analyze the provided input-output pairs to understand the transformation rule.

**Perception of Elements:**

The task involves 2D grids (matrices) where each cell contains a single digit integer representing a color. The input grids transform into output grids of the same dimensions. The transformation seems to involve modifying specific colored regions based on their surroundings. It appears that isolated, single-pixel objects of certain colors are extended if near other objects, possibly dependent on size.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      - dimensions: variable (rows x columns)
      - cells: integer values (0-9), representing colors
  - type: object
    properties:
      - shape: contiguous block of same-colored pixels
      - color: integer value (0-9)
      - size: number of pixels
      - isolated: boolean (true if no adjacent pixels of different colors, except background)

actions:
  - extend_object:
      condition: object is isolated and adjacent to another object
      operation: change neighboring background pixels to the object's color, possibly dependent on relative size, extending horizontally

relationships:
    - adjacency:  pixels sharing an edge or corner.
    - background: large area of single color, usually azure (8)
    - containment: objects are contained within the grid

```


**Natural Language Program:**

1.  **Identify Objects:** Scan the input grid to identify all contiguous blocks of pixels with the same color. These are the objects.
2.  **Identify Background:** The background is considered to be the most frequent color present in the input, forming a connected component.
3.  **Check for Isolated Single Pixels**: Iterate through each identified object. Determine if it has only one pixel, if so, check if it is *isolated*. An isolated, single-pixel object is one whose neighboring pixels, using 8-connectivity (including diagonals), are only background pixels.
4. **Extend Isolated Pixels Adjacent to Objects**: If an *isolated, single pixel object* has a neighbor (8-connectivity) which is not the background color, then extend the single pixel object, *horizontally* towards (in the direction of) the neighboring non-background pixels. The neighboring object remains intact.
5. **Repeat Step 4**: Iterate through all the isolated single-pixel objects and repeat step 4.

In summary, the transformation extends isolated single-pixel objects horizontally towards nearby objects. The nearby object isn't changed. The extension occurs only horizontally. The background stays unchanged otherwise.

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
