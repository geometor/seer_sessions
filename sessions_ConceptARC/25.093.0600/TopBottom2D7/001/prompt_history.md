
## train_1

**input:**
```
1 1 1 1 1 1 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 3
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
1 1 1 1 1 1
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0
0 0 0 1 1 1 1 1
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
3 3 3
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 1 1 1 1 0 0 0
0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
1 1 1 1
```


## train_4

**input:**
```
0 0 0 3 3 3 0 0
0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0
0 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
3 3 3
3 3 3
```


## train_5

**input:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
1
```

Okay, let's analyze the provided examples to understand the transformation rule.

**Perception of the Elements:**

*   **Input:** An 8x8 grid containing integers 0, 1, and 3. Zero appears to be a background color. The non-zero numbers (1 and 3) form contiguous blocks, either horizontally, vertically, or as single cells. There can be multiple blocks of 1s and multiple blocks of 3s within the same input grid.
*   **Output:** A potentially smaller grid containing only the cells from *one type* of block (either all the 1s or all the 3s) present in the input. The spatial arrangement of the selected blocks relative to each other seems preserved, cropped to their bounding box.
*   **Transformation:** The core task is to select *which* number (1 or 3) should be preserved in the output, and then extract all blocks of that selected number from the input grid.

**Identifying the Selection Criterion:**

Comparing the input and output across the examples, the selection seems based on position:

1.  **train_1:** The block of '1's starts at row 0. The block of '3's starts at row 4. The output contains the '1's block (the top-most block).
2.  **train_2:** The block of '3's starts at row 2. The block of '1's starts at row 3. The output contains the '3's block (the top-most block).
3.  **train_3:** The block of '1's starts at row 3. The block of '3's starts at row 5. The output contains the '1's block (the top-most block).
4.  **train_4:** A block of '3's starts at row 0. Another block of '3's starts at row 1. Blocks of '1's start at rows 4 and 5. The output contains both blocks of '3's (belonging to the top-most block type).
5.  **train_5:** The block of '1' starts at row 2. The block of '3' starts at row 5. The output contains the '1' block (the top-most block).

The rule appears to be: find the non-zero block(s) that appear highest up in the grid (minimum row index). If there's a tie for the highest row index (e.g., multiple blocks start on the same top-most row), the left-most block (minimum column index among those tied) determines the number to select. Once the number (1 or 3) is selected based on this top-left-most block, *all* blocks of that number from the input are included in the output.

**YAML Facts:**


```yaml
task_elements:
  - object: InputGrid
    properties:
      - type: grid
      - dimensions: 8x8
      - cell_values: [0, 1, 3]
      - background_value: 0
      - contains: NonZeroBlocks
  - object: NonZeroBlock
    properties:
      - type: contiguous group of cells
      - value: [1, 3]
      - location: defined by cell coordinates (row, column)
      - bounding_box: defines spatial extent
      - top_row_index: minimum row index of any cell in the block
      - left_col_index: minimum column index of any cell in the block
  - object: OutputGrid
    properties:
      - type: grid
      - dimensions: variable (cropped)
      - cell_values: [1] or [3] (mutually exclusive per example)
      - derived_from: a subset of NonZeroBlocks from InputGrid

relationships:
  - type: selection
    subject: NonZeroBlock value (1 or 3)
    rule: >
      Identify the block(s) with the minimum top_row_index.
      If multiple blocks share the minimum top_row_index,
      select the one among them with the minimum left_col_index.
      The value of this top-left-most block determines the selected value.
  - type: extraction
    subject: OutputGrid
    source: InputGrid
    rule: >
      Include all NonZeroBlocks from the InputGrid whose value matches
      the selected value. Preserve their relative spatial arrangement.
      Crop the output to the bounding box containing all selected blocks.
```


**Natural Language Program:**

1.  Identify all distinct contiguous blocks of non-zero numbers (1s and 3s) in the input grid.
2.  For each identified block, determine its value (1 or 3) and find the coordinates of its top-most, left-most cell.
3.  Find the minimum row index among all these top-left coordinates.
4.  Consider only the blocks whose top-left cell has this minimum row index.
5.  Among these blocks, find the minimum column index of their top-left cells.
6.  The block located at the overall minimum row index and the subsequent minimum column index determines the "target number" (either 1 or 3).
7.  Select *all* blocks from the input grid that consist of this target number.
8.  Construct the output grid containing only the cells belonging to these selected blocks, preserving their values and relative positions, cropped to their combined bounding box.
