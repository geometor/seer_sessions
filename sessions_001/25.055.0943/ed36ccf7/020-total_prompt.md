# ed36ccf7 • 020 • example_4 • investigate_coder

---

## Example 4

**input:**
```
2 0 2
0 0 2
0 2 2
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7297AE864460>

**output:**
```
2 2 2
0 0 2
2 0 0
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7297AE865990>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Task Elements:**

The task involves a 3x3 grid of pixels. Each pixel has a color value, represented by an integer (0 for white, 2 for red). The transformation seems to involve rearranging the red pixels within the grid while keeping the white pixels in their original positions. The change in the arrangement of red pixels suggests a rotation or reflection.

**YAML Block - Facts:**


```yaml
objects:
  - type: grid
    dimensions: 3x3
    elements: pixels
    properties:
      - color:
        type: integer
        values: [0, 2]
  - type: pixel
    properties:
      - color:
          type: integer
          values: [0,2] #white, red

actions:
    - name: re_arrange_red
      description: reposition red pixels based on rules, keeps white pixels
      parameters: none

relationships:
  - type: spatial
    description: pixels are arranged in a 2D grid.
  - type: unchanged
    description: white pixel remain in the same positions, red pixels are
    repositioned.

```


**Natural Language Program:**

1.  **Identify:** Recognize the input as a 3x3 grid of pixels with values 0 (white) and 2 (red).
2.  **Preserve White:** Maintain the positions of all white pixels (0) in the output grid.
3.  **Transform Red:** The output is created by rotating the input 90 degrees clockwise.


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
