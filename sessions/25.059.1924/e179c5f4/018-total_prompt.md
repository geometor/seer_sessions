# e179c5f4 • 018 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
1 0 0 0
```

<PIL.Image.Image image mode=RGB size=256x640 at 0x716635B76350>

**output:**
```
8 8 8 1
8 8 1 8
8 1 8 8
1 8 8 8
8 1 8 8
8 8 1 8
8 8 8 1
8 8 1 8
8 1 8 8
1 8 8 8
```

<PIL.Image.Image image mode=RGB size=256x640 at 0x716635BBBED0>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The input is a 10x4 grid, predominantly filled with '0' (white pixels). A single '1' (blue pixel) is present in the bottom-left corner. The output is a 10x4 grid as well. It appears a pattern is generated, involving '8' (azure) and '1' (blue), centered around where original blue pixel located.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    dimensions: [10, 4]
    elements: pixels
    description: Input and output grids

  - type: pixel
    value: 0
    color: white
    description: Background color in the input

  - type: pixel
    value: 1
    color: blue
    description: Seed pixel in the input, result pattern color.

  - type: pixel
    value: 8
    color: azure
    description: Result pattern.

actions:
  - type: locate
    target: blue pixel (1)
    description: Find the coordinates of the blue pixel in the input grid.

  - type: generate_pattern
    seed: located blue pixel
    description: Create the output grid.
    rules:
      - replace the blue seed location with azure
      - blue '1' pixels appear at a cross pattern relative to the original blue '1' pixel location

relationships:
  - input_grid: Contains a single blue pixel among white pixels.
  - output_grid: Contains a cross shape of blue around the seed pixel.
```


**Natural Language Program:**

1.  **Locate the Seed:** Find the (x, y) coordinates of the single blue pixel ('1') within the input grid.
2.  **Initialize Output:** Create an output grid of the same dimensions as the input grid, filled entirely with azure ('8')
3.  **cross pattern:** fill a cross, or plus shape, around the located seed with blue pixels
    - the length of the cross is determined by the grid size
    - for a 10 x 4 grid, there are 5 cells above and below for the vertical line, and 2 to the left, and one to the right forming the cross bar.
4. leave the seed cell as an azure pixel.


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
