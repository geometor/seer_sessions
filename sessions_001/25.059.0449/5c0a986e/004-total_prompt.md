# 5c0a986e • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 0 0 0
0 0 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 0 0 0 0
0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x744068CB76D0>

**output:**
```
1 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 0 0 0
0 0 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 0 0 0 0
0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 2 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x744068CB40D0>
Okay, let's analyze this input-output pair.

**Perception of Elements:**

The input and output are 10x10 grids. The input grid contains two 2x2 squares: one blue (1) and one red (2). The output grid seems to retain the 2x2 red square in the same location. The blue square in the input is also a 2x2 square. In the output we see single blue pixels at the four corners of where an expanded square, which is the original plus one row and column added, where the original square was. The same has possibly been done for the red, but since the original is in the center, this can't be confirmed in this first training pair.

**YAML Block (Facts):**


```yaml
objects:
  - type: square
    color: blue (1)
    size: 2x2
    position: (2,2)  # Top-left corner coordinates
  - type: square
    color: red (2)
    size: 2x2
    position: (6,4)  # Top-left corner coordinates
  - type: pixel
    color: blue (1)
    positions_output: [(0,0), (1,1),(8,6), (9,7)]
  - type: pixel
    color: red (2)
  
  - type: grid
    size: 10x10

actions:
  - type: expand_square
    agent: unknown
    input: blue square, red square
    output: corner pixels of where expanded version of the squares would have been.

relationships:
  - input_output: "The output grid appears to show an expanded representation of the original squares in the form of their corner pixels"
```


**Natural Language Program:**

1.  Identify all 2x2 colored squares in the input grid.
2.  For each identified square, imagine expanding it by one cell in all directions (up, down, left, and right). Or in other words, increase each dimension by two, centering the expansion.
3.  In the output grid, set pixels with the color of that square to the top left and lower right corner of where the expanded version would have been.
4. output should be the the union of all these corner pixels.


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
