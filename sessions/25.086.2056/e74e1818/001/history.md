
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 1 0 0
0 0 0 1 1 0 1 1 0 0 0
0 0 0 8 8 8 8 8 0 0 0
0 0 0 5 0 5 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 5 5 5 5 0 0 0
0 0 0 0 2 2 2 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0
0 0 0 3 3 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 1 0 1 1 0 0 0
0 0 1 1 1 1 1 1 1 0 0
0 0 0 8 8 8 8 8 0 0 0
0 0 0 5 5 5 5 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 5 0 5 0 0 0
0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 2 2 2 0 0 0 0
0 0 0 3 3 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2 2 0 0 0
0 0 0 0 2 0 2 0 2 0 0 0 0
0 0 0 0 0 2 0 2 0 0 0 0 0
0 0 0 3 0 0 3 0 0 3 0 0 0
0 0 0 0 3 3 3 3 3 0 0 0 0
0 0 0 0 1 1 1 1 1 0 0 0 0
0 0 0 0 1 0 0 0 1 0 0 0 0
0 0 0 0 1 1 1 1 1 0 0 0 0
0 0 0 0 4 4 0 4 4 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 2 0 0 0 0 0
0 0 0 0 2 0 2 0 2 0 0 0 0
0 0 0 2 2 2 2 2 2 2 0 0 0
0 0 0 0 3 3 3 3 3 0 0 0 0
0 0 0 3 0 0 3 0 0 3 0 0 0
0 0 0 0 1 1 1 1 1 0 0 0 0
0 0 0 0 1 0 0 0 1 0 0 0 0
0 0 0 0 1 1 1 1 1 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 4 4 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0
0 0 9 9 9 0 0
0 9 0 9 0 9 0
0 0 4 4 4 0 0
0 3 3 3 3 3 0
0 0 0 3 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0
0 9 0 9 0 9 0
0 0 9 9 9 0 0
0 0 4 4 4 0 0
0 0 0 3 0 0 0
0 3 3 3 3 3 0
0 0 0 0 0 0 0
```

Okay, let's break down this task.

**Perception**

1.  **Input/Output Structure:** Both input and output are grids of pixels represented by integer color values. The grids maintain their dimensions.
2.  **Color Focus:** The transformation seems primarily concerned with the arrangement of non-white pixels (colors 1-9). White pixels (color 0) act as background or separators.
3.  **Row Operations:** The changes between input and output occur at the row level. Entire rows are being rearranged, but the content within each row remains unchanged.
4.  **Color Grouping:** Rows containing the same non-white color appear grouped together contiguously in the input. For example, in `train_1`, rows 1 and 2 both feature blue, rows 4, 5, and 6 feature gray, and rows 7 and 8 feature red.
5.  **Transformation Pattern:** Within each contiguous block of rows defined by a single non-white color, the order of the rows is reversed in the output grid.
    *   In `train_1`, the blue rows (1, 2) become (2, 1). The gray rows (4, 5, 6) become (6, 5, 4). The red rows (7, 8) become (8, 7).
    *   In `train_2`, the red rows (1, 2, 3) become (3, 2, 1). The green rows (4, 5) become (5, 4), etc.
    *   In `train_3`, the maroon rows (1, 2) become (2, 1). The green rows (4, 5) become (5, 4).
6.  **Single-Row Blocks:** If a color block consists of only one row (like the azure row in `train_1` or the yellow row in `train_3`), reversing it results in the same row, so it appears unchanged.
7.  **White Rows:** Rows containing only white pixels are not part of these colored blocks and remain in their original relative positions, acting as separators between the blocks.

**Facts**


```yaml
facts:
  - grid_dimensions: Input and output grids have the same height and width.
  - elements:
      - type: Pixel
        properties:
          - color: Integer value 0-9 (0=white, 1-9=non-white)
      - type: Row
        properties:
          - index: Vertical position in the grid.
          - content: Sequence of pixels.
          - composition: Can be all white, or contain white and a single non-white color.
      - type: Row Block
        properties:
          - contiguity: Composed of vertically adjacent rows.
          - color_uniformity: All rows in the block share the same single non-white color (along with potentially white pixels).
          - boundary: Bounded above and below by either the grid edge or rows with different compositions (all white or different non-white color).
          - rows: The list of rows belonging to the block.
          - index_range: The start and end row index occupied by the block.
  - actions:
      - identify_blocks: Scan the input grid row by row to find contiguous blocks of rows sharing the same single non-white color.
      - reverse_rows: Within each identified block, reverse the order of the rows.
      - reconstruct_grid: Assemble the output grid by placing the (potentially reversed) blocks and the unchanged all-white rows into their corresponding positions.
  - relationships:
      - The output grid is derived solely from rearranging rows of the input grid.
      - The rearrangement is determined by grouping rows based on shared non-white color and reversing the order within those groups.
```


**Natural Language Program**

1.  Create a new grid, the `output_grid`, with the same dimensions as the `input_grid`, initially filled with a placeholder or copied from the input.
2.  Iterate through the rows of the `input_grid` using an index `current_row_index`, starting at 0.
3.  At each `current_row_index`:
    a. Examine the row at `input_grid[current_row_index]`.
    b. Find the single non-white color present in the row. If no non-white color exists (the row is all white), increment `current_row_index` by 1 and proceed to the next iteration (step 3).
    c. If a non-white color `C` is found, identify the vertical block of contiguous rows starting from `current_row_index` where each row contains *only* white pixels and pixels of color `C`. Let this block end at `end_row_index`.
    d. Extract the sequence of rows from the `input_grid` from `current_row_index` to `end_row_index`.
    e. Reverse the order of this sequence of rows.
    f. Place the reversed sequence of rows into the `output_grid` starting at the row index `current_row_index`.
    g. Update `current_row_index` to `end_row_index + 1`.
4.  Once all rows of the `input_grid` have been processed (`current_row_index` reaches the grid height), return the `output_grid`.
