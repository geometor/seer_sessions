# feca6190 • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 0 2 0 0
```

<PIL.Image.Image image mode=RGB size=320x64 at 0x7CE41B95CC50>

**output:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 2
0 0 0 2 0
0 0 2 0 0
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x7CE41B95CBD0>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves transforming a 1x5 grid (input) into a 5x5 grid (output). The input grid contains a single non-zero element (red, value 2) at the center, surrounded by zeros (white). The output grid is an expansion of this, with the single red pixel from the input becoming a diagonal line of red pixels in the output, stretching from the bottom left to the top right. All other pixels in the output are white.

**YAML Block (Facts):**


```yaml
task_name: train_2
input:
  type: grid
  dimensions: 1x5
  elements:
    - color: white
      value: 0
      count: 4
    - color: red
      value: 2
      count: 1
      position: [0,2]
output:
  type: grid
  dimensions: 5x5
  elements:
    - color: white
      value: 0
      count: 22
    - color: red
      value: 2
      count: 3
      positions: [[2,4], [3,3], [4,2]]
transformation:
  type: expansion and diagonal replication
  input_element: red pixel (value 2)
  output_pattern: diagonal line from bottom-left to top-right
```


**Natural Language Program:**

1.  **Identify the colored pixel:** Find the single non-zero (red, value 2) pixel in the 1x5 input grid.
2.  **Create output grid:**  Create a 5x5 output grid filled with zeros (white).
3. **Expand and replicate**: Create a diagonal of red (with the same original non-zero value) pixels on the 5x5 output grid. The diagonal should go from the bottom left to the top right. The amount of red pixels will correspond to the initial input width, each input cell expanded to one output red pixel.
4. **Result:** The result is a 5x5 grid with a diagonal line of red pixels from bottom-left to top-right, and all other pixels are white.


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
