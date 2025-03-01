# f8ff0b80 • 012 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 1 0 0 0
0 2 2 2 0 0 0 0 1 1 0 0
0 0 0 0 0 0 0 0 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 4 0 0 0 0
0 0 0 4 4 4 4 4 0 0 0 0
0 0 0 4 4 4 4 4 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=768x768 at 0x716635B765D0>

**output:**
```
4
2
1
```

<PIL.Image.Image image mode=RGB size=64x192 at 0x716635C7ADD0>
Okay, here's my analysis of the provided input-output pair:

**Perception of Elements:**

The input is a grid of colored pixels. There are distinct colored regions (objects): red (2), blue (1), and yellow (4). The output is a sequence of numbers, vertically stacked, each corresponding to a color in the input grid. The order seems significant, as does the absence of the background color (0, or white).

**YAML Block - Facts:**


```yaml
objects:
  - type: region
    color: red
    value: 2
    shape: irregular
    size: 7
  - type: region
    color: blue
    value: 1
    shape: irregular
    size: 3
  - type: region
    color: yellow
    value: 4
    shape: irregular
    size: 9
  - type: background
    color: white
    value: 0

output:
  type: sequence
  format: vertical stack
  elements:
    - value: 4
    - value: 2
    - value: 1
```


**Natural Language Program:**

1.  **Identify Regions:** Find all contiguous regions of the same color (excluding the background color white/0) in the input grid.
2. **Determine Order**: Order the identified colored regions by their values in descending order.
3.  **Output Sequence:** Create a vertical sequence of single-pixel colored blocks. Each block in sequence represents the color value from the sorted list of regions.

In summary: the program identifies colored regions in the input, sorts the color *values* in descending order, and outputs these sorted values as a vertical sequence of pixels.

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
