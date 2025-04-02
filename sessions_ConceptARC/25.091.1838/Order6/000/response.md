*   **Perception**:
    *   The input and output grids have the same dimensions.
    *   The background color is white (0) and remains unchanged.
    *   The inputs contain distinct horizontal rectangular blocks of solid colors.
    *   Each block has a specific color, height (number of rows), and width (number of columns).
    *   In the output grids, these same blocks appear but are rearranged vertically.
    *   The blocks retain their original color, height, and width.
    *   Comparing the input and output blocks in both examples suggests a sorting mechanism.
    *   In `train_1`, the blocks are Gray (width 1), Yellow (width 3), Red (width 2), Green (width 4). In the output, they appear in the order Gray (1), Red (2), Yellow (3), Green (4).
    *   In `train_2`, the blocks are Orange (width 10), Blue (width 4), Yellow (width 8), Magenta (width 6). In the output, they appear in the order Blue (4), Magenta (6), Yellow (8), Orange (10).
    *   The vertical rearrangement seems to be based on sorting the blocks by their width in ascending order.
    *   The blocks are stacked vertically in the output grid, starting from the topmost row occupied by any block in the input grid.

*   **Facts (YAML)**:
    
```yaml
    task_type: object_manipulation
    grid_properties:
      - dimensions_preserved: True
      - background_color: 0 # white
      - background_preserved: True
    objects:
      - type: horizontal_rectangular_block
        definition: A contiguous area of pixels with the same non-background color, extending horizontally.
        properties:
          - color: The color index (1-9) of the block's pixels.
          - height: The number of rows the block occupies.
          - width: The number of columns the block occupies.
          - top_row: The row index of the block's topmost row in the input grid.
          - left_column: The column index of the block's leftmost column (appears to always be 0 in examples).
        attributes_preserved:
          - color
          - height
          - width
          - left_column
        attributes_modified:
          - top_row
    actions:
      - action: identify_blocks
        description: Find all distinct horizontal rectangular blocks of non-background color in the input grid.
        inputs: input_grid
        outputs: list_of_blocks (each with color, height, width, top_row, left_column)
      - action: sort_blocks
        description: Sort the identified blocks based on their width.
        input: list_of_blocks
        parameter: width
        order: ascending
        output: sorted_list_of_blocks
      - action: reconstruct_grid
        description: Create the output grid by placing the sorted blocks vertically, preserving their original height, width, color, and horizontal position, starting from the minimum top_row of the original blocks.
        inputs: sorted_list_of_blocks, original_grid_dimensions, original_min_top_row, background_color
        output: output_grid
    relationships:
      - relation: vertical_ordering
        input_basis: original vertical position (top_row)
        output_basis: block width (ascending order)
    ```


*   **Natural Language Program**:
    1.  Initialize an empty list to store information about identified blocks.
    2.  Scan the input grid to find all distinct horizontal rectangular blocks of non-white pixels. For each block found:
        a.  Determine its color, height (number of rows), width (number of columns), and the row index of its top edge. Assume the leftmost column is 0 based on examples.
        b.  Store this information (color, height, width, original top row) as a record for the block.
    3.  Find the minimum top row index among all identified blocks in the input grid. This will be the starting row for placing blocks in the output.
    4.  Sort the list of block records based on their width in ascending order.
    5.  Create a new output grid with the same dimensions as the input grid, filled entirely with the white background color (0).
    6.  Initialize a variable `current_row` to the minimum top row index found in step 3.
    7.  Iterate through the sorted list of block records:
        a.  For the current block record, retrieve its color, height, and width.
        b.  Place the block onto the output grid. The block will occupy rows from `current_row` to `current_row + height - 1`, and columns from 0 to `width - 1`, using the block's color.
        c.  Update `current_row` by adding the height of the block just placed (`current_row = current_row + height`).
    8.  Return the completed output grid.