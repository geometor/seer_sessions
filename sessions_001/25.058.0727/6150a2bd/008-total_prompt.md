# 6150a2bd • 008 • example_2 • investigate_coder

---

## Example 2

**input:**
```
5 5 2
1 0 0
0 0 0
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7545B86D2CB0>

**output:**
```
0 0 0
0 0 1
2 5 5
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7545B872F930>
Okay, here's my analysis of the provided example, focusing on perception, facts, and a natural language program describing the transformation.

**Perception of Elements:**

The task involves a transformation of a 3x3 grid of colored pixels. The colors are represented by single digits (0-9). The transformation seems to involve a rotation and a color swap, specifically, a 90-degree counter-clockwise rotation and change the position of the non-zero numbers.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    dimensions: 3x3
    elements: pixels
    properties:
      - color (represented by digits 0-9)

actions:
  - type: rotation
    direction: counter-clockwise
    degrees: 90

  - type: color_swap
    description: Specific color changes based on original position.

relationships:
  - spatial: grid elements are arranged in rows and columns
  - transformational: input grid transforms to output grid via rotation and color_swap
```


**Natural Language Program:**

1.  **Rotate:** Rotate the entire input grid 90 degrees counter-clockwise.
2.  **Color/value swap:** after rotation:
    *   The element at \[2,0] becomes the element at \[0,2].
    *   The element at \[2,1] becomes the element at \[1,2].
    *   The element at \[2,2] becomes the element at \[2,2].
    *   The element at \[1,0] becomes the element at \[0,1].
3.  All other elements become 0.

Essentially all the non-zero elements switch place with the element on their left, wrapping around the edge. The grid is then rotated.

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
