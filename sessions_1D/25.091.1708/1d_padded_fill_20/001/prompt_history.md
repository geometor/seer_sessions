
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 7 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 3 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 3 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
5 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Perception**

The input grids consist primarily of white pixels (0), with a few scattered non-white pixels. In each example, the non-white pixels appear in pairs within specific rows. Each pair within a row consists of two pixels of the *same* non-white color (orange (7) in train_1, green (3) in train_2, gray (5) in train_3).

The corresponding output grids show that the space *between* these pairs of same-colored pixels in each row has been filled with that same color, effectively drawing a horizontal line segment connecting the original pair. The transformation operates independently on each row. Rows that do not contain exactly two pixels of the same non-white color remain unchanged (although this case isn't explicitly shown, it's implied by the structure).

**Facts**


```yaml
elements:
  - type: grid
    properties:
      - background_color: white (0)
      - contains: sparse colored pixels
  - type: object
    description: Colored pixels acting as endpoints.
    properties:
      - color: non-white (3, 5, 7 in examples)
      - quantity_per_row: exactly two (in relevant rows)
      - arrangement: horizontally aligned within the same row
      - relationship: form pairs of the same color
  - type: action
    description: Filling the space between endpoint pairs.
    input: a pair of same-colored pixels in a row
    output: a horizontal line segment of that color connecting the pair
    scope: operates independently on each row
  - type: result
    description: Output grid where pairs are connected.
    properties:
      - contains: horizontal line segments of non-white colors
      - segment_color: matches the color of the endpoint pair it connects
      - segment_location: spans the columns between (and including) the original endpoint pair within their row
```


**Natural Language Program**

1.  Initialize the output grid as a copy of the input grid.
2.  Iterate through each row of the input grid.
3.  For the current row, identify all non-white pixels and their column indices.
4.  Check if there are exactly two non-white pixels in this row *and* if they both have the same color.
5.  If the condition in step 4 is met:
    a.  Determine the color of these two pixels (let's call it `fill_color`).
    b.  Determine the column indices of these two pixels (let's call them `col1` and `col2`).
    c.  Find the minimum column index (`min_col`) and the maximum column index (`max_col`) from `col1` and `col2`.
    d.  In the corresponding row of the *output* grid, change the color of all pixels from column `min_col` to `max_col` (inclusive) to `fill_color`.
6.  If the condition in step 4 is not met, the row in the output grid remains unchanged from the input grid (it was already copied in step 1).
7.  After processing all rows, the modified grid is the final output.
