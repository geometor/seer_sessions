
## train_1

**input:**
```
0 0 0 0 0 0
2 8 2 8 2 8
2 8 2 8 2 8
0 0 0 0 0 0
0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
2 8 2 8 2 8 2 8 2 8 2 8
2 8 2 8 2 8 2 8 2 8 2 8
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
2 3 3 2 3 3 2
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 3 3 2 3 3 2 3 3 2 3 3 2 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
1 2 2 1 2 2 1 2
2 1 2 2 1 2 2 1
0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 2 2 1 2 2 1 2 2 1 2 2 1 2 2 1
2 1 2 2 1 2 2 1 2 2 1 2 2 1 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, I'm ready to analyze the provided input-output examples and discern the transformation rule. Here's my report:

**Perception of Task Elements:**

The task involves 2D grids of single-digit integers (0-9), representing different colors. The transformation appears to operate on rows of the input grid. The primary operation seems to be an expansion or duplication of the non-zero rows, specifically, the rows are doubled, and padding is applied.

**YAML Block - Facts:**


```yaml
facts:
  - object: input_grid
    type: 2D array
    properties:
      - dimensions: variable (rows x columns)
      - values: integers (0-9)
  - object: output_grid
    type: 2D array
    properties:
      - dimensions: derived from input_grid
      - values: integers (0-9)
  - action: row_expansion
    description: Doubles the width of each non-zero row.
    properties:
      - input: row (list of integers)
      - output: expanded row (list of integers)
  - relationship: output_dimensions
    description: The output grid's width is double+padding the width of non zero rows.
    details:  "padding is added to keep the width consistent across all rows, rows that are all zero have double width"
  - relationship: row_mapping
    description: Each non-zero row in the input_grid maps to an expanded row in the output_grid. All zero value rows remain the same, but double width.
```


**Natural Language Program:**

1.  **Iterate** through each row of the input grid.
2.  **Check** if the row contains only zeros.
3.  **If** the row contains only zeros, create a new row in output with double with, also all zeros.
4. **If** contains non-zero values, **expand** it by repeating each element.
5.  **Create Output**: create a new row in the output grid that is the expanded
    row.
6.  The output grid's width is double the width of the original non-zero rows.
7.  Padding with zeroes is inserted around the non-zero rows to maintain a consistent grid width.


