# 1-3aa6fb7a • 002 • example_1 - CODE

---

**input**
```
0 0 0 0 0 0 0
0 8 0 0 0 0 0
0 8 8 0 0 0 0
0 0 0 0 8 8 0
0 0 0 0 0 8 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

![Image](000-example_1_input.png)


**output**
```
0 0 0 0 0 0 0
0 8 1 0 0 0 0
0 8 8 0 0 0 0
0 0 0 0 8 8 0
0 0 0 0 1 8 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

![Image](000-example_1_output.png)

Okay, let's analyze the transformation between the input and output grids.

**YAML Observation:**

```yaml
input_grid:
  size: 7x7
  objects:
    - color: 8 (azure)
      positions: [(1,1), (2,1), (2,2), (3,4), (3,5), (4,5)]
      shape: Two separate 2x1 rectangles and two single cells.
    - color: 0 (white)
      positions: All other cells
      shape: Background

output_grid:
  size: 7x7
  objects:
    - color: 8 (azure)
      positions: [(1,1), (2,1), (2,2), (3,4), (3,5), (4,5)]
      shape: Two separate 2x1 rectangles and two single cells.
    - color: 1 (blue)
      positions: [(1,2), (4,4)]
      shape: Two single cells.
    - color: 0 (white)
      positions: All other cells
      shape: Background
```

**Natural Language Program:**

1.  **Identify Objects:** In the input grid, we have two types of objects: azure (8) colored objects and the white (0) background. The azure objects appear as two 2x1 vertical rectangles and two individual cells.

2.  **Detect Changes**: Compare each cell of the output grid to the input grid.

3. **Observe Transformations**:
    * The azure (8) objects from the input grid remain unchanged in the output grid.
    * Inspect the cells to the immediate right of each azure object. If an azure object is found, and the adjacent cell on the right is background color (white/0), then this cell turns to color blue (1).

4.  **Apply the Rule:**
  - The cell at (1, 2) is to the right of the cell(1,1), and is color 0, therefore, it turns to 1 (blue).
  - The cell at (4, 4) is to the right of the cell(4,5) and is color 0, therefore, it turns to 1 (blue).

**Transformation Rule (In Natural Language):**

The azure (8) objects in the input grid remain unchanged. For each azure object, examine the cell directly to its right. If the cell is background color (white/0), change it to blue (1). Otherwise, leave it unchanged.

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
