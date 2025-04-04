# 6-0520fde7 • 002 • example_1 - CODE

---

**input**
```
1 0 0 5 0 1 0
0 1 0 5 1 1 1
1 0 0 5 0 0 0
```

![Image](000-example_1_input.png)


**output**
```
0 0 0
0 2 0
0 0 0
```

![Image](000-example_1_output.png)

Okay, let's analyze the transformation from the input grid to the output grid.

**YAML Block: Observations**

```yaml
input_grid:
  size: 3x7
  objects:
    - color: 1
      positions: [(0, 0), (1, 1), (1, 5), (1, 6), (2, 0)]
      shape: irregular
    - color: 5
      positions: [(0, 3), (1, 3), (2, 3)]
      shape: vertical line
    - color: 0
      positions: background, filling the rest
      shape: background

output_grid:
  size: 3x3
  objects:
    - color: 2
      positions: [(1,1)]
      shape: single cell
    - color: 0
      positions: background
      shape: Background
```

**Natural Language Program: Transformation Rule**

1.  **Identify Objects:** In the input grid, we have three types of objects based on color: blue (1), gray (5), and the background white (0).

2.  **Focus on a Specific Object:** The key object of transformation seems to be where color 5 (gray) is.

3.  **Detect the Gray object position:** Gray appears in a vertical line shape. The transformation will replace the gray color with a new color, 2 (red).

4.  **Define the output size:** The new color 2 (red) appears in the new output grid that has a size of 3x3.

5. **Output:** Output a 3x3 grid of the same height of the input, all zeros except the center cell which has color 2 (red).

**Transformation Summary**

The transformation takes specific object from the input, detects its size, and replaces it by a new object color. The output grid is all zeros (background color) except for a single red (color 2) cell in the center.

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
{ natural language description of the transformation rule }
"""

{ imports }

def transform(input_grid):
    # initialize output_grid

    # change output pixels 

    return output_grid

```
