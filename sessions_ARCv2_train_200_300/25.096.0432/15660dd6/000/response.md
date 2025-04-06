**Perception of Task Elements:**

1.  **Input Structure:** The input is a grid of digits. It appears to be structured into smaller subgrids or "blocks". These blocks are separated by borders composed of the digit '8'. The digit '1' often acts as a background filler within these blocks.
2.  **Block Identification:** Each block contains a distinct pattern or "shape" made of a digit other than '1' or '8'.
3.  **Row Identifiers:** The first digit in the rows that are part of a horizontal sequence of blocks seems significant. It acts as an identifier or label for the blocks in that row. For example, in `train_1`, the rows starting with '5' contain blocks, the rows starting with '9' contain blocks, and the rows starting with '0' contain blocks.
4.  **Shape Content:** Inside each block (excluding the '1' background and surrounding '8' border), there is a shape formed by a specific digit (e.g., '2', '3', '4', '5', '6', '7').
5.  **Output Structure:** The output is also a grid of digits, smaller than the input. It consists of a horizontal arrangement of blocks, separated by columns of '8's.
6.  **Transformation Logic:** The core transformation involves selecting specific blocks from the input grid based on a rule and arranging their internal shapes into the output grid.
7.  **Selection Rule:** For each column of blocks in the input grid, the block containing the shape with the *highest numerical digit value* is selected.
8.  **Output Block Construction:** The output grid is formed by taking the shapes from the selected input blocks. For each selected shape, its pattern is placed into the output grid. The background/surrounding area for that shape in the output block is filled with the *row identifier* digit (from the first column of the input row where the selected block originated). The blocks in the output are separated by columns of '8's. The size of the shape copied to the output matches the inner dimensions of the input block.

**Facts:**


```yaml
objects:
  - name: input_grid
    properties:
      - type: grid of digits
      - contains: blocks, borders
  - name: output_grid
    properties:
      - type: grid of digits
      - smaller_than: input_grid
      - contains: selected_shapes, borders
  - name: block
    properties:
      - type: subgrid within input_grid
      - contains: inner_area, surrounding_border (digit 8)
      - associated_with: row_identifier
  - name: inner_area
    properties:
      - type: region within a block
      - contains: background (digit 1), shape
  - name: shape
    properties:
      - type: pattern of digits within inner_area
      - composed_of: shape_digit (not 1 or 8)
  - name: row_identifier
    properties:
      - type: digit
      - location: first column of the rows defining a horizontal sequence of blocks in the input_grid
      - associated_with: all blocks in its row
  - name: border
    properties:
      - type: lines of digits
      - value: 8
      - separates: blocks in input_grid, shapes in output_grid

actions:
  - name: parse_input
    actor: system
    inputs: input_grid
    outputs: identified_blocks (with shape, shape_digit, row_identifier)
    description: Divide the input grid into blocks based on '8' borders and identify the row identifier and inner shape for each block.
  - name: select_blocks
    actor: system
    inputs: identified_blocks (grouped by column)
    outputs: selected_block_info (shape, row_identifier) for each column
    description: For each column of input blocks, find the block whose shape_digit has the maximum numerical value.
  - name: construct_output
    actor: system
    inputs: selected_block_info (ordered by input column)
    outputs: output_grid
    description: Create the output grid by placing the selected shapes horizontally, filling the background of each shape's block with its corresponding row_identifier, and separating blocks with columns of '8's.

relationships:
  - type: selection_criterion
    subject: block
    object: shape_digit
    detail: The block with the maximum shape_digit value within a column is selected.
  - type: representation
    subject: output_block
    object: selected_input_block
    detail: The output block contains the shape of the selected input block, with the background determined by the input block's row_identifier.
```


**Natural Language Program:**

1.  **Identify Blocks:** Scan the input grid to locate rectangular blocks of data. These blocks are separated horizontally and vertically by lines of the digit '8'. Identify the inner area of each block (typically filled with '1's and a shape digit) and the digit ('8') forming its immediate border.
2.  **Extract Block Information:** For each identified block:
    *   Determine its `row_identifier`: Find the digit in the first column of the input grid corresponding to the rows the block occupies.
    *   Determine its `shape_digit`: Identify the digit (other than '1' or '8') that forms the pattern within the block's inner area.
    *   Extract the `shape`: Capture the pattern formed by the `shape_digit` within the inner area (e.g., a 5x5 or 6x6 grid representing the shape).
    *   Note the block's column index (0-based) in the grid of blocks.
3.  **Group by Column:** Group the extracted block information (shape, shape\_digit, row\_identifier) based on their column index in the input grid of blocks.
4.  **Select Winning Block per Column:** For each column group:
    *   Compare the `shape_digit` values of all blocks in that column.
    *   Select the block information (shape, row\_identifier) corresponding to the block with the numerically highest `shape_digit`.
5.  **Construct Output Grid:**
    *   Initialize an empty output grid.
    *   Iterate through the selected block information, ordered by their original column index.
    *   For each selected item (shape `S`, row\_identifier `R`):
        *   Create an output block with the same dimensions as the extracted shape `S`.
        *   Fill the output block: Place the pattern of `S` into the block using its original `shape_digit`. Fill all other positions within the block with the `row_identifier` digit `R`.
        *   Append this output block to the right side of the current output grid.
        *   If this is not the last selected block, append a vertical column of '8's (with the same height as the output blocks) as a separator to the right of the appended block.
6.  **Finalize:** The resulting grid is the final output.