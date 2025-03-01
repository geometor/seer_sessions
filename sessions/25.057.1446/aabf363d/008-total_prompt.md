# aabf363d • 008 • example_2 • investigate_coder

---

## Example 2

**input:**
```
0 0 0 0 0 0 0
0 0 0 3 0 0 0
0 0 3 3 3 0 0
0 3 3 3 3 0 0
0 3 3 0 0 0 0
0 0 3 3 0 0 0
6 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x786C54814AD0>

**output:**
```
0 0 0 0 0 0 0
0 0 0 6 0 0 0
0 0 6 6 6 0 0
0 6 6 6 6 0 0
0 6 6 0 0 0 0
0 0 6 6 0 0 0
0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x786C547D3AD0>
Okay, here's my analysis of the provided example, structured as a report:

**Perception of Elements:**

The task involves a grid of colored pixels (represented by numbers 0-9). The primary colors observed are white (0), green (3), and magenta (6).  There's a clear geometric shape formed by the green pixels in the input, which is then mirrored by magenta pixels in the output. The single magenta pixel in the input seems to act as a seed or a replacement key. The grid dimensions remain constant.

**YAML Fact Documentation:**


```yaml
facts:
  - observation: |
      The input grid contains a contiguous shape made of green (3) pixels.
  - observation: |
      There's a single magenta (6) pixel in the input grid, located outside the green shape.
  - observation: |
      The output grid contains a shape that is identical in form to the green shape in the input, but made of magenta (6) pixels.
  - observation: |
      The single magenta pixel in the input is replaced with a white pixel in the output.
  - observation: |
      All white (0) pixels remain unchanged.
  - observation: |
      The dimensions of the grid are the same in both input and output (7x7).
  - relationship: |
     The position of the magenta shape in the output corresponds exactly to the position of the green shape in the input.
  - action: |
      The green shape is replaced with a magenta shape.
  - action:  |
      The seeding magenta pixel is replaced with white.
```


**Natural Language Program:**

1.  **Identify the "seed" pixel:** Locate the single magenta (6) pixel in the input grid.
2.  **Identify the target shape:** Find the contiguous block of green (3) pixels in the input grid.
3. **Replace and replicate:** Create a shape in the output that is the same as the target, but with color magenta.
4.  **Clear seed:** Change the original seed magenta pixel to white (0) in the output.
5.  **Preserve background:** All other white (0) pixels in the input grid remain white (0) in the output grid.

Essentially, the program identifies a shape of one color and replaces it with an identical shape of another color, guided by a seed.

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
