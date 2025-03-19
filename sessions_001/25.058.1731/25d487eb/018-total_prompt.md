# 25d487eb • 018 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 2 3 3 0 0 0 0 0
0 0 0 3 3 3 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=768x960 at 0x7C36044BF7D0>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 2 3 3 0 0 0 0 0
0 0 0 3 3 3 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=768x960 at 0x7C3604475ED0>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a grid of colored pixels. The primary colors involved seem to be white (0), green (3), and red (2). The input grid contains a cluster of green and red pixels, while the rest of the grid is white. The output grid retains the initial cluster of green and red pixels but adds a vertical column of red pixels extending downwards from the initial red pixel.

**YAML Block (Facts):**


```yaml
objects:
  - name: green_cluster
    type: contiguous_pixels
    color: green
    shape: irregular
    initial_position: (2,2) # Top-left corner of the cluster

  - name: red_pixel
    type: single_pixel
    color: red
    initial_position: (2,4)

  - name: red_column
    type: contiguous_pixels
    color: red
    shape: vertical_line
    start_position: (2,4) # Same as red_pixel's initial position
    end_position: (14,4)   # Bottom of the grid
    
  - name: white_background
    type: contiguous_pixels
    color: "white"
    shape: "grid"
    
actions:
  - type: extend
    object: red_column
    from: red_pixel
    direction: down
    to_edge: true

relationships:
  - type: adjacent
    object1: green_cluster
    object2: red_pixel
    direction: red_pixel is to the right of green_cluster

```


**Natural Language Program:**

1.  **Identify Objects:** Locate the contiguous cluster of green (3) pixels and the single red (2) pixel within that cluster.
2.  **Extend Red:** From the location of the original red pixel, create a vertical column of red pixels extending downwards.
3.  **Reach Boundary:** Continue the red column until it reaches the bottom edge of the grid.
4.  **Preserve other objects:** Keep the green cluster in place. All the white pixels not part of the column remain unchanged.

In essence, the transformation rule is to find the red pixel within the green cluster and extend it downwards to the bottom edge of the grid, forming a red column, all other elements of the grid remain unchanged.

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
