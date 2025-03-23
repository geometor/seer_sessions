
## train_1

**input:**
```
3 3 8
3 7 0
5 0 0
```


**output:**
```
0 0 5
0 7 3
8 3 3
```


## train_2

**input:**
```
5 5 2
1 0 0
0 0 0
```


**output:**
```
0 0 0
0 0 1
2 5 5
```

Okay, here's my analysis of the provided input-output examples, formatted as a report:

**Perception of Elements:**

The task involves a transformation of a 2D grid of single-digit integers (representing colors) to another 2D grid of the same dimensions. The transformation doesn't involve introducing new colors/digits; instead, it seems to re-arrange the existing ones. The most prominent feature is that the input grid is rotated and flipped and the output grid's rows are sorted numerically from largest to smallest.

**YAML Block - Facts:**


```yaml
facts:
  - observation: "Input and output grids have the same dimensions."
  - observation: "The digits in the input grid are preserved in the output grid."
  - object: "Grid"
    properties:
      - dimensions: "rows x columns"
      - elements: "single-digit integers (0-9)"
    actions:
      - "rotated clockwise by 90 degrees"
      - "rows are then mirrored (flipped vertically)"
      - "rows are sorted by max element values"
  - relationship: "Input digits map directly to output digits (no new digits introduced)."

```


**Natural Language Program:**

1.  **Rotate:** Rotate the input grid 90 degrees clockwise.
2.  **Mirror:** Mirror/Flip the rotated grid vertically (i.e., swap the first and last rows, the second and second-to-last rows, etc.).
3.  **Sort rows:** Sort the rows in decreasing order based on the largest value in each row.


