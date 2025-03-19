# b9b7f026 • 012 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 0 0 3 3 3 3 3 0 0
0 0 1 1 1 1 1 1 0 0 3 3 3 3 3 0 0
0 0 1 1 1 1 1 1 0 0 3 3 3 3 3 0 0
0 0 1 1 1 1 1 1 0 0 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 2 0 0 7 7 7 7 7 0
0 0 2 2 2 2 2 2 2 0 0 7 7 7 7 7 0
0 0 2 0 0 0 2 2 2 0 0 7 7 7 7 7 0
0 0 2 0 0 0 2 2 2 0 0 7 7 7 7 7 0
0 0 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=1088x1024 at 0x7F4C2318BDD0>

**output:**
```
2
```

<PIL.Image.Image image mode=RGB size=64x64 at 0x7F4C1B75CA50>
Okay, let's analyze this ARC-AGI task example.

**Perception of Elements:**

The input is a grid of colored pixels. The output appears to be a single digit integer. The input grid contains several distinct rectangular blocks of different colors (blue, green, red, and orange). Some rectangles have "holes" in them (the red one). The sizes of these rectangles seem to vary. The key seems to be to relate a characteristic of the colored rectangles in the image to the final output integer, and color alone seems to be a poor choice to start with.

**YAML Block (Facts):**


```yaml
objects:
  - type: rectangle
    properties:
      color: [blue, green, red, orange, ...]
      size: [variable]
      has_hole: [true, false]
  - type: grid
    properties:
      dimensions: [16 x 17] # from the example input grid
      background_color: white #value=0

actions:
  - type: count
    target: object.type # number of occurances of something

relationships:
  - type: contains
    relation: grid contains rectangles
  - type: inside
    relation: hole inside rectangle
```


**Natural Language Program:**

1.  **Identify Rectangles:** Locate all distinct rectangular regions of uniform color within the input grid.
2.  **Check for Holes:** For each rectangle, determine if it contains a region of a different color completely enclosed within its boundaries (a "hole").
3.  **Count Specific Rectangles:** Count the number of rectangles that have a "hole".
4. **Output:** Output the count of the object determined in step 3, as a single integer. In the supplied example, there is only object with a hole - the red rectangle.

In summary, it appears the task involves counting the number of rectangles in the input grid which contain an "inner" rectangle or "hole" of a different color.

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
