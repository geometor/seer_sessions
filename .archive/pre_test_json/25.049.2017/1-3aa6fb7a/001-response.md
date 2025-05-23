# 1-3aa6fb7a • 001 • example_1 - NLP

---
Okay, let's analyze the transformation between the input and output grids.

**YAML Block Summary**

```yaml
observations:
  input_grid:
    objects:
      - color: 8
        shape: irregular
        positions: [[1,1], [2,1], [2,2], [4,4], [4,5], [5,4]]
    size: [7, 7]
  output_grid:
    objects:
      - color: 8
        shape: irregular
        positions: [[1,1], [2,1], [2,2], [4,4], [4,5], [5,4]]
      - color: 1
        shape: single_cell
        positions: [[1,2], [5,4]]
    size: [7, 7]
```

**Natural Language Program**

Here's a step-by-step description of the transformation:

1.  **Identify Objects:** In the input grid, we have several objects of color `8` (azure). There are no objects of color different that `0` or `8`.

2.  **Preserve Some, Change Some:**
    The object `8` remains at the same positions, there are 2 pixels of color `8` that changes to color `1`.
    The color of two individual `8` cells are changed to `1` (blue).
    The changed `8` are at positions next to color `8`.

3. **Identify Changing Cells Position:** The cells that are changed are:
    -   The single azure cell in the top left object, adjacent to another azure cell.
    -   One azure cell in the bottom rigth object, adjacent to another azure cell.

**Transformation Rule (In Natural Language)**

The rule can be summarized as follows:

Locate all of `8` colored pixels that forms a group (at least 2). For each group, find the pixel that have another pixel in the group adjacent to it. For all this cases, change color `8` by color `1`. Keep the rest of the grid equal.


