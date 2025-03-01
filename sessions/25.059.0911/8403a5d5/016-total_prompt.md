# 8403a5d5 • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7D67CBF4F950>

**output:**
```
0 0 0 0 4 5 4 0 4 5
0 0 0 0 4 0 4 0 4 0
0 0 0 0 4 0 4 0 4 0
0 0 0 0 4 0 4 0 4 0
0 0 0 0 4 0 4 0 4 0
0 0 0 0 4 0 4 0 4 0
0 0 0 0 4 0 4 0 4 0
0 0 0 0 4 0 4 0 4 0
0 0 0 0 4 0 4 0 4 0
0 0 0 0 4 0 4 5 4 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7D67CBDADED0>
Okay, let's analyze this input-output example pair.

**Perception of Elements:**

The input is a 10x10 grid of mostly 0s (white), with a single 4 (yellow) pixel near the bottom. The output is also a 10x10 grid. The single yellow pixel in the input seems to have become the seed for a pattern in the output. The output grid maintains the original yellow pixel and adds new pixels, primarily yellow (4) and some gray (5). The gray pixels appear at specific locations within the emerging pattern. The overall structure is a grid.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    dimensions: 10x10
    elements: pixels
    
  - type: pixel
    values: [0, 4, 5]
    colors:
        0: white
        4: yellow
        5: gray

actions:
  - type: seed_expansion
    seed_object: yellow_pixel
    rules: [ replace, adjacent_placement, alternating colors]

relationships:
    - input: single_yellow_pixel
    - output: pattern_of_yellow_and_gray_pixels
    - constraint: expansion_from_seed
    - constraint: size does not change

```


**Natural Language Program:**

1.  **Identify the Seed:** Locate the single yellow (4) pixel in the input grid.
2.  **Vertical and Horizontal Lines:**  Create vertical and horizontal lines of yellow (4) pixels passing through the seed pixel, extending to the edges of the grid.
3. **Alternating Fill:** Fill the remaining cells with alternating 4 and 0 such that cells adjacent to 4 are either 4 or 0 and never 5.
4.  **Corner Replacement:** In the four corners of resulting checkerboard of 4s and 0s, replace the 0 with 5, if a 4 exist there, the values stays a 4.

In simpler terms: Create a cross of yellow pixels centered on the initial yellow pixel. Then, fill the remaining grid in an alternating checkerboard, and turn corners pixels into gray.

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
