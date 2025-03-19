# ff805c23 • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 3 3 3 3 0 0 2 2 2 0 0 0 0 2 2 2 0 1 1 1 1 1 0
3 3 3 3 3 0 2 2 0 2 2 0 0 2 2 0 2 2 1 1 1 1 1 3
3 3 3 0 0 3 2 0 0 2 0 0 0 0 2 0 0 2 1 1 1 1 1 3
3 3 0 3 3 3 2 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1 3
3 3 0 3 3 3 0 2 0 2 2 2 2 2 2 0 2 0 1 1 1 1 1 3
0 0 3 3 3 3 0 0 0 2 2 2 2 2 2 0 0 0 3 3 3 3 0 0
0 2 2 2 0 0 2 0 0 2 2 2 2 2 2 0 0 2 0 0 2 2 2 0
2 2 0 2 2 0 0 2 2 0 2 2 2 2 0 2 2 0 0 2 2 0 2 2
2 0 0 2 0 0 0 2 2 0 0 2 2 0 0 2 2 0 0 0 2 0 0 2
2 2 2 2 2 2 2 0 0 2 2 2 2 2 2 0 0 2 2 2 2 2 2 2
0 2 0 2 2 2 2 2 0 2 0 2 2 0 2 0 2 2 2 2 2 0 2 0
0 0 0 2 2 2 2 2 2 2 2 0 0 2 2 2 2 2 2 2 2 0 0 0
0 0 0 2 2 2 2 2 2 2 2 0 0 2 2 2 2 2 2 2 2 0 0 0
0 2 0 2 2 2 2 2 0 2 0 2 2 0 2 0 2 2 2 2 2 0 2 0
2 2 2 2 2 2 2 0 0 2 2 2 2 2 2 0 0 2 2 2 2 2 2 2
2 0 0 2 0 0 0 2 2 0 0 2 2 0 0 2 2 0 0 0 2 0 0 2
2 2 0 2 2 0 0 2 2 0 2 2 2 2 0 2 2 0 0 2 2 0 2 2
0 2 2 2 0 0 2 0 0 2 2 2 2 2 2 0 0 2 0 0 2 2 2 0
0 0 3 3 3 3 0 0 0 2 2 2 2 2 2 0 0 0 3 3 3 3 0 0
3 3 0 3 3 3 0 2 0 2 2 2 2 2 2 0 2 0 3 3 3 0 3 3
3 3 0 3 3 3 2 2 2 2 2 2 2 2 2 2 2 2 3 3 3 0 3 3
3 3 3 0 0 3 2 0 0 2 0 0 0 0 2 0 0 2 3 0 0 3 3 3
3 3 3 3 3 0 2 2 0 2 2 0 0 2 2 0 2 2 0 3 3 3 3 3
0 3 3 3 3 0 0 2 2 2 0 0 0 0 2 2 2 0 0 3 3 3 3 0
```

<PIL.Image.Image image mode=RGB size=1536x1536 at 0x716635B763D0>

**output:**
```
0 3 3 3 3
0 3 3 3 3
3 0 0 3 3
3 3 3 0 3
3 3 3 0 3
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x716635B761D0>
Okay, let's analyze this ARC-AGI task example.

**Perception of Elements:**

The input is a large grid (24x24) composed of pixels of different colors (represented by digits 0-9). The output is a much smaller grid (5x5). The colors in the output seem to be a subset of those in the input, specifically colors 0 (white) and 3 (green) appear prominently, with color 2 being removed. The most prominent change is the significant reduction in size and simplification of the shapes. The output grid captures the upper left corner area, and the shapes of color '3' in the input appear to translate to the smaller output grid.

**YAML Block (Facts):**


```yaml
task_description:
  task_id: train_1
  input:
    grid_size: 24x24
    colors: [0, 1, 2, 3]
    objects:
      - type: irregular_shapes
        colors: [3, 2, 1]
        description: Large connected regions of colors 3, 2, and 1 embedded within a background of color 0
      - type: background
        color: 0

  output:
    grid_size: 5x5
    colors: [0, 3]
    objects:
     - type: irregular shapes
       colors: [3]
       description: shape from the upper left corner

  transformation:
    type: size_reduction
    corner: upper_left
    color_filtering:
      kept: [0, 3]
      removed: [1, 2]

```


**Natural Language Program:**

1.  **Focus on the Upper-Left Corner:** The transformation extracts a 5x5 subgrid from the upper-left corner of the input grid.
2.  **Color Filter:**  All pixels that are *not* color 0 (white) or 3 (green) are removed or replaced. In this case, all colors other than white and green are eliminated, effectively isolating only the upper left green shape and surrounding white pixels.

In essence, the transformation isolates a specific region (top-left) and filters based on color, keeping only white and green. The output represents a simplified, cropped, and color-filtered version of the input's top-left corner.

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
