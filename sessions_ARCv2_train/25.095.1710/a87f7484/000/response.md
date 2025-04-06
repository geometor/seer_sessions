*   **Perception of the Elements:**
    *   The input is a grid (matrix) of single-digit integers.
    *   The input grid dimensions vary but seem constrained: either 3 rows and multiple columns (>=3), or multiple rows (>=3) and 3 columns.
    *   The input grid appears to be composed of smaller, distinct 3x3 "patterns" or "blocks".
    *   These 3x3 blocks are characterized by a specific non-zero digit appearing multiple times within the 3x3 area, often with zeros as padding or background.
    *   The blocks within the input are arranged either horizontally (when the input has 3 rows) or vertically (when the input has 3 columns). They seem to tile the input grid without overlap in their core 3x3 space.
    *   The output is always a single 3x3 grid.
    *   The output grid is identical to one of the 3x3 blocks present in the input grid.
    *   The core task is to identify all the 3x3 blocks within the input and then apply a selection criterion to choose exactly one of them as the output.

*   **Facts:**
    
```yaml
    objects:
      - name: input_grid
        properties:
          - type: 2D array of integers
          - rows: R
          - columns: C
          - contains: multiple 3x3 blocks
          - block_arrangement: determined by shape (horizontal if R=3, C>3; vertical if C=3, R>3)
      - name: block
        properties:
          - type: 3x3 2D array of integers
          - source: extracted from input_grid
          - elements: integer values from 0-9
          - non_zero_count: count of elements greater than 0
      - name: output_grid
        properties:
          - type: 3x3 2D array of integers
          - relationship: identical to one specific block from input_grid
    
    actions:
      - name: determine_arrangement
        inputs: input_grid dimensions (R, C)
        outputs: block_arrangement (horizontal or vertical)
      - name: extract_blocks
        inputs: input_grid, block_arrangement
        outputs: list of block objects
        description: |
          If horizontal, iterate through columns taking 3x3 slices every 3 columns.
          If vertical, iterate through rows taking 3x3 slices every 3 rows.
      - name: count_non_zeros
        inputs: block
        outputs: non_zero_count for the block
      - name: select_output_block
        inputs: list of blocks with their non_zero_counts
        outputs: the single block with the maximum non_zero_count
        description: Find the block that has the highest number of non-zero cells compared to all other extracted blocks.
    
    relationships:
      - input_grid is tiled by non-overlapping 3x3 blocks.
      - output_grid is the block from input_grid with the maximal count of non-zero elements.
    ```


*   **Natural Language Program:**
    1.  Examine the dimensions (number of rows R, number of columns C) of the input grid.
    2.  Determine the arrangement of 3x3 blocks:
        *   If R=3 and C>3, the blocks are arranged horizontally.
        *   If C=3 and R>3, the blocks are arranged vertically.
    3.  Initialize an empty list to store the extracted 3x3 blocks.
    4.  Extract all 3x3 blocks based on the determined arrangement:
        *   If horizontal, iterate through the columns in steps of 3. For each step `k` (starting from 0), extract the 3x3 subgrid corresponding to columns `3k` to `3k+2`. Add this block to the list.
        *   If vertical, iterate through the rows in steps of 3. For each step `k` (starting from 0), extract the 3x3 subgrid corresponding to rows `3k` to `3k+2`. Add this block to the list.
    5.  For each extracted block in the list, calculate the count of its elements that are greater than zero (non-zero count).
    6.  Identify the block from the list that has the highest non-zero count. Assume there is a unique block with the maximum count based on the examples.
    7.  The output grid is this identified block (the one with the maximum number of non-zero elements).