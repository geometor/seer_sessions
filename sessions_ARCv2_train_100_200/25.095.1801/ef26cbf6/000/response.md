**Perception of the Elements:**

1.  **Grid Structure:** Both input and output are numerical grids.
2.  **Separators (Value 4):** The number '4' plays a crucial role as a separator.
    *   **Horizontal Separators:** Rows composed entirely of '4's divide the grid into distinct horizontal "Blocks".
    *   **Vertical Separators:** Columns containing '4's (often aligned with the horizontal separators) implicitly define vertical "Regions" within the blocks.
3.  **Blocks:** These are sub-grids located between the horizontal separator rows (or before the first/after the last separator). The core transformation logic appears to operate differently depending on the properties of the *first* block.
4.  **Characteristic Numbers:** Within each block (or sometimes region), certain non-zero numbers (that are not '4') seem important. These act as identifiers or replacement values. Examples are '7', '3', '8' in `train_1` and '3', '2', '6' in `train_2`.
5.  **Placeholder (Value 1):** The number '1' acts as a placeholder in the input grid. Its presence indicates a location where a replacement needs to occur.
6.  **Transformation Logic:** The core task is to replace the placeholder '1's with appropriate Characteristic Numbers. The method for determining the correct Characteristic Number depends on a condition related to the first block.
    *   **Mode 1 (Block-local replacement):** If the first block contains exactly one unique Characteristic Number, then *each* block finds its *own* unique Characteristic Number, and uses that number to replace the '1's *within that same block*. (`train_1` follows this mode).
    *   **Mode 2 (First-block reference):** If the first block contains zero or more than one unique Characteristic Number, then the first block remains unchanged. For *subsequent* blocks, the '1's are replaced by Characteristic Numbers found in the *first* block, based on matching vertical regions. (`train_2` follows this mode).
7.  **Other Values (Value 0):** The number '0' appears to be a background or empty value, generally remaining unchanged.

**YAML Facts:**


```yaml
Objects:
  - Grid: Represents the entire input or output data structure.
    Properties:
      - rows: Number of rows.
      - columns: Number of columns.
      - cells: Collection of Cell objects.
  - Block: A horizontal sub-section of the Grid, separated by SeparatorRows.
    Properties:
      - start_row: Starting row index.
      - end_row: Ending row index.
      - characteristic_numbers: Set of unique non-zero, non-4 numbers within the Block.
  - Cell: An individual element within the Grid/Block.
    Properties:
      - row: Row index.
      - column: Column index.
      - value: The number contained in the cell (0, 1, 4, or other).
  - SeparatorRow: A row consisting entirely of the value 4.
    Properties:
      - row_index: The index of the separator row.
  - VerticalRegion: A vertical sub-section within a Block, defined by SeparatorColumns (columns containing 4s).
    Properties:
      - start_col: Starting column index.
      - end_col: Ending column index.
      - source_characteristic_number: The characteristic number found in the corresponding region of the first block (relevant for Mode 2).
  - Placeholder: A specific cell value (1) indicating a target for replacement.
  - CharacteristicNumber: A non-zero, non-4 value used for identification or replacement.

Relationships:
  - Grid `contains` Blocks.
  - SeparatorRows `separate` Blocks within a Grid.
  - Columns containing 4s `define` VerticalRegions within Blocks.
  - Cells `belong_to` a Block and potentially a VerticalRegion.
  - Blocks `have` CharacteristicNumbers.
  - Placeholders `are_replaced_by` CharacteristicNumbers based on transformation rules.

Actions:
  - split_grid_into_blocks: Using SeparatorRows.
  - find_characteristic_numbers: Within a specified Block or VerticalRegion.
  - count_unique_characteristic_numbers: For the first Block.
  - identify_vertical_regions: Based on columns containing 4s.
  - determine_transformation_mode: Based on the count of unique characteristic numbers in the first Block.
  - replace_placeholders: Applying the rules of the determined mode.
  - copy_cell_value: For cells that are not placeholders or part of the transformation.
  - reconstruct_grid: Combining processed Blocks and SeparatorRows.
```


**Natural Language Program:**

1.  **Initialization:** Read the input Grid.
2.  **Identify Blocks:** Scan the Grid row by row. Identify rows composed entirely of the number '4'; these are SeparatorRows. Use these rows to divide the Grid into horizontal Blocks. Note the first block (Block 1).
3.  **Analyze First Block:** Find all unique non-zero, non-'4' numbers within Block 1. Count how many such unique numbers exist.
4.  **Determine Mode:**
    *   **If** the count of unique non-zero, non-'4' numbers in Block 1 is exactly one: **Execute Mode 1**.
    *   **Else** (the count is zero or greater than one): **Execute Mode 2**.
5.  **Execute Mode 1 (First block has one unique characteristic number):**
    *   For *each* Block (including the first one):
        *   Find the single unique non-zero, non-'4' number within *this* Block (let it be `block_char_num`).
        *   Iterate through each Cell in *this* Block.
        *   If the Cell's value is '1' (Placeholder), change its value to `block_char_num`.
        *   Keep all other Cell values (0, 4, the original `block_char_num`) unchanged.
6.  **Execute Mode 2 (First block has zero or >1 unique characteristic numbers):**
    *   **Process First Block:** Leave Block 1 completely unchanged.
    *   **Identify Vertical Regions & Reference Numbers:** Determine the vertical column boundaries defined by columns containing '4's. For each resulting Vertical Region, find the unique non-zero, non-'4' number located within that region *in Block 1*. Store these as reference numbers for each region.
    *   **Process Subsequent Blocks:** For *each* Block *after* the first one:
        *   Iterate through each Cell in the current Block.
        *   If the Cell's value is '1' (Placeholder):
            *   Determine which Vertical Region the Cell's column belongs to.
            *   Find the stored reference number associated with that Vertical Region (obtained from Block 1).
            *   Change the Cell's value to this reference number.
        *   Keep all other Cell values (0, 4, etc.) unchanged.
7.  **Reconstruction:** Assemble the processed Blocks and the original SeparatorRows back into the final output Grid.