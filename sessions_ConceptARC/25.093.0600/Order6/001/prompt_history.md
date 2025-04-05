
## train_1

**input:**
```
0 0 0 0 0 0
0 0 0 0 0 0
5 0 0 0 0 0
4 4 4 0 0 0
4 4 4 0 0 0
4 4 4 0 0 0
2 2 0 0 0 0
2 2 0 0 0 0
3 3 3 3 0 0
3 3 3 3 0 0
3 3 3 3 0 0
3 3 3 3 0 0
```


**output:**
```
0 0 0 0 0 0
0 0 0 0 0 0
5 0 0 0 0 0
2 2 0 0 0 0
2 2 0 0 0 0
4 4 4 0 0 0
4 4 4 0 0 0
4 4 4 0 0 0
3 3 3 3 0 0
3 3 3 3 0 0
3 3 3 3 0 0
3 3 3 3 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7
1 1 1 1 0 0 0 0 0 0
1 1 1 1 0 0 0 0 0 0
1 1 1 1 0 0 0 0 0 0
4 4 4 4 4 4 4 4 0 0
4 4 4 4 4 4 4 4 0 0
4 4 4 4 4 4 4 4 0 0
6 6 6 6 6 6 0 0 0 0
6 6 6 6 6 6 0 0 0 0
6 6 6 6 6 6 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
1 1 1 1 0 0 0 0 0 0
1 1 1 1 0 0 0 0 0 0
1 1 1 1 0 0 0 0 0 0
6 6 6 6 6 6 0 0 0 0
6 6 6 6 6 6 0 0 0 0
6 6 6 6 6 6 0 0 0 0
4 4 4 4 4 4 4 4 0 0
4 4 4 4 4 4 4 4 0 0
4 4 4 4 4 4 4 4 0 0
7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7
```

Okay, let's break down the transformation logic for this task.

**Perception of the elements:**

1.  **Input/Output Format:** Both input and output are 2D grids (matrices) of single digits.
2.  **Content:** The grids contain a background digit (0) and several solid rectangular blocks, each composed of a single non-zero digit (e.g., a block of 4s, a block of 3s).
3.  **Transformation:** The core transformation involves rearranging the vertical positions of these non-zero blocks. The blocks themselves (their digit, shape, and internal structure) remain unchanged. Their horizontal positions (leftmost column) also appear unchanged relative to the grid width.
4.  **Reordering Pattern:** The vertical rearrangement is not random. In `train_1`, the blocks seem to be re-stacked based on their height (1x1 block 5, then 2x2 block 2, then 3x3 block 4, then 4x4 block 3). In `train_2`, all blocks have the same height (3 rows), and the reordering seems based on their width (3x4 block 1, then 3x6 block 6, then 3x8 block 4, then 3x10 block 7). This suggests a primary sort by height and a secondary sort by width.
5.  **Anchoring:** The entire stack of reordered blocks seems to be positioned vertically such that the bottom edge of the lowest block in the final stack aligns with the bottom-most extent of *any* block in the original input grid. The sorted blocks are then stacked contiguously upwards from this bottom anchor.

**YAML Facts:**


```yaml
Grid:
  type: object
  properties:
    dimensions: [rows, columns]
    cells: list[list[int]]
    background_value: 0

Block:
  type: object
  properties:
    value: int (non-zero digit)
    shape: [height, width]
    location:
      top_row: int
      left_col: int
      bottom_row: int
  relationships:
    - composed_of: same digit
    - contained_in: Grid

Transformation:
  action: rearrange_blocks
  input: Grid
  output: Grid
  steps:
    - identify_blocks: Find all contiguous rectangular non-zero Blocks in the input Grid.
    - calculate_properties: Determine height, width, and top-left corner for each Block.
    - determine_sort_order: Sort Blocks first by ascending height, then by ascending width.
    - find_anchor: Identify the maximum row index occupied by any Block in the input Grid (anchor_bottom_row).
    - reconstruct_grid:
        - Create an empty output Grid of the same dimensions.
        - Place the sorted Blocks vertically stacked.
        - Start placing from the bottom: the last block in the sorted list has its bottom row at anchor_bottom_row.
        - Each subsequent block (moving up the stack) is placed immediately above the previous one.
        - Maintain the original left_col for each Block.
        - Fill remaining cells with the background_value.
```


**Natural Language Program:**

1.  Initialize an empty output grid with the same dimensions as the input grid, filled with the background digit (0).
2.  Scan the input grid to identify all distinct, contiguous, rectangular blocks composed of the same non-zero digit. For each block found, record its digit value, its height, its width, and the column index of its leftmost edge (`left_col`).
3.  Determine the overall bottom-most row index (`anchor_bottom_row`) occupied by any non-zero cell in the input grid.
4.  Create a list of the identified blocks.
5.  Sort this list of blocks primarily in ascending order based on their height. If two blocks have the same height, sort them secondarily in ascending order based on their width.
6.  Iterate through the *sorted* list of blocks, starting from the *last* block (the one with the greatest height/width) and moving towards the *first* block. Maintain a `current_bottom_row` variable, initially set to the `anchor_bottom_row`.
7.  For the current block being processed:
    a. Calculate its required `top_row` as `current_bottom_row - height + 1`.
    b. Place the block (using its digit value) into the output grid, spanning from `top_row` to `current_bottom_row` vertically, and starting horizontally at its original `left_col` for its calculated `width`.
    c. Update `current_bottom_row` to `top_row - 1` to prepare for placing the next block immediately above the current one.
8.  After processing all blocks, the output grid is complete.
