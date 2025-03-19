# 90c28cc7 • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 2 2 2 2 2 2 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 2 2 2 2 2 2 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 2 2 2 2 2 2 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 2 2 2 2 2 2 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 2 2 2 2 2 2 0 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 1 1 1 1 1 1 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 1 1 1 1 1 1 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 1 1 1 1 1 1 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 1 1 1 1 1 1 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 1 1 1 1 1 1 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 1 1 1 1 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=1344x1344 at 0x7F2DF787A050>

**output:**
```
8 2
3 3
4 1
```

<PIL.Image.Image image mode=RGB size=128x192 at 0x7F2DF7900050>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The input is a large grid (21x21) filled with colored squares. The output is a much smaller grid (3x2) or a list of pairs of numbers. The input grid appears to be composed of four distinct rectangular blocks of color arranged in a 2x2 pattern. Each block has a unique color (azure, red, green, yellow, blue). The output seems to represent a summary of the input, distilling each colored block into a pair of numbers. The key is that each colored rectangle is represented by its colors. It appears that the upper left corner colors are listed, followed by the upper right, then the lower left, etc.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    name: input_grid
    dimensions: 21x21
    elements: colored_blocks
  - type: block
    name: azure_block
    color: azure (8)
    dimensions: 6x6
    position: top-left
  - type: block
    name: red_block
    color: red (2)
    dimensions: 6x6
    position: top-right
  - type: block
    name: green_block
    color: green (3)
    dimensions: 6x6
    position: middle-left
 - type: block
    name: green_block_2
    color: green (3)
    dimensions: 6x6
    position: middle-right
  - type: block
    name: yellow_block
    color: yellow (4)
    dimensions: 6x6
    position: bottom-left
  - type: block
    name: blue_block
    color: blue (1)
    dimensions: 6x6
    position: bottom-right
  - type: grid
    name: output_grid
    dimensions: 3x2
    elements: number_pairs

actions:
  - type: summarize
    input: input_grid
    output: output_grid
    method: extract_color_pairs

relationships:
  - type: spatial
    description: colored blocks are arranged in a 2x2 grid within the input_grid.
  - type: correspondence
    description: each colored block in the input corresponds to a number pair in the output.
```


**Natural Language Program:**

1.  **Identify Colored Blocks:** Divide the input grid into four equally sized, contiguous rectangular blocks of color, positioned in a 2x2 arrangement.
2.    **List Block Colors:** Iterate through the blocks in a specified order: top-left, top-right, middle-left, middle-right, bottom-left, bottom-right, and output each blocks color value.


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
